"""This file contains the helper functions for the Iris package."""
# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #

import functools
import gzip
import io
import json
import tarfile
from logging import getLogger
from pathlib import Path
from typing import Callable, Optional

import docker
import jmespath
import requests
import wget
from rich.console import Console
from rich.progress import Progress
from rich.table import Table
from tqdm import tqdm
from tqdm.utils import CallbackIOWrapper

from iris.sdk.exception import DownloadLinkNotFoundError

from .conf_manager import conf_mgr

logger = getLogger("iris.utils")

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                         Utils                                                        #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

# ------------------------------  Helper Function for Iris Pull, Upload and Download   ------------------------------ #


def make_targz(local_folder_path: str):
    """Create a tar.gz archive of the local folder - make this deterministic / exclude timestamp info from gz header.

    Args:
        local_folder_path: The folder to be converted to a tar.gz

    Returns: A buffer containing binary of the folder as a tar.gz file

    """
    tar_buffer = io.BytesIO()
    block_size = 4096
    # Add files to a tarfile, and then by-chunk to a tar.gz file.
    with tarfile.open(fileobj=tar_buffer, mode="w") as tar:
        tar.add(
            local_folder_path,
            arcname=".",
            filter=lambda x: None if "pytorch_model.bin" in x.name else x,
        )
    # Exclude pytorch_model.bin if present, as safetensors should be uploaded instead.
    with gzip.GzipFile(
        filename="",  # do not emit filename into the output gzip file
        mode="wb",
        fileobj=tar_buffer,
        mtime=0,
    ) as myzip:
        for chunk in iter(lambda: tar_buffer.read(block_size), b""):
            myzip.write(chunk)

    return tar_buffer


def copy_local_folder_to_image(container, local_folder_path: str, image_folder_path: str) -> None:
    """Helper function to copy a local folder into a container."""
    tar_buffer = io.BytesIO()
    with tarfile.open(fileobj=tar_buffer, mode="w") as tar:
        tar.add(local_folder_path, arcname=".")
    tar_buffer.seek(0)

    # Copy the tar archive into the container
    container.put_archive(image_folder_path, tar_buffer)


def show_progress(line, progress, tasks):  # sourcery skip: avoid-builtin-shadow
    """Show task progress for docker pull command (red for download, green for extract)."""
    print(line["status"])
    if line["status"] == "Downloading":
        id = f'[red][Download {line["id"]}]'
    elif line["status"] == "Extracting":
        id = f'[green][Extract  {line["id"]}]'
    else:
        # skip other statuses
        return

    if id not in tasks.keys():
        tasks[id] = progress.add_task(f"{id}", total=line["progressDetail"]["total"])
    else:
        progress.update(tasks[id], completed=line["progressDetail"]["current"])


def download_model(
    download_url: str,
    model_name: str,
    path: str = "model_storage",
    json_output: bool = False,
):
    """Helper function for iris download to download model to local machine giving download url.

    Args:
        download_url (str): url to download the model
        model_name (str): name of the model
        path (str, optional): path for model storage . Defaults to "model_storage".
        json_output (bool, optional): Whether to output the progress in json format. Defaults to False.

    Raises:
        DownloadLinkNotFoundError: Download link expired error
    """
    # download the tar file
    try:
        if json_output:
            tarfile_path = wget.download(download_url, path, bar=None)
            try:
                json.loads(tarfile_path)
            except json.JSONDecodeError:
                pass
        else:
            tarfile_path = wget.download(download_url, path)
    except Exception as e:
        raise DownloadLinkNotFoundError from e

    # Extract the tar file to a folder on the local file system
    with tarfile.open(tarfile_path) as tar:
        tar.extractall(path=f"model_storage/{model_name}/models")

    # delete the tar file
    Path(tarfile_path).unlink()


def pull_image(
    model_folder_path: str,
    container_name: str,
    job_tag: str,
    task_name: str,
    baseline_model_name: str,
    baseline: bool,
    json_output: bool = False,
):
    """Pull image.

    This function handles the logic of pulling the base image and creating a new image with
    the model files copied into it.

    Args:
        model_folder_path: The path to the model folder
        container_name: The name of the container
        job_tag: The tag of the job
        task_name: The name of the task
        baseline_model_name: The name of the baseline model
        baseline: Whether the model is the baseline model
        json_output: Whether to output the progress in json format

    """
    temp_container_name = f"temp-{container_name}"

    env_var = {
        "TASK_NAME": task_name,
        "BASELINE_MODEL_NAME": baseline_model_name,
        "BASELINE": str(baseline),
    }

    tasks = {}
    with Progress() as progress:
        # docker pull the base image
        client = docker.from_env()
        resp = client.api.pull(conf_mgr.BASE_IMAGE, stream=True, decode=True)
        for line in resp:
            if not json_output:
                show_progress(line, progress, tasks)

    # Create a new temp container
    container = client.containers.create(image=conf_mgr.BASE_IMAGE, name=temp_container_name, environment=env_var)

    copy_local_folder_to_image(container, model_folder_path, "/usr/local/triton/models/")

    # Commit the container to a new image
    container.commit(repository=container_name)

    client.images.get(container_name).tag(f"{container_name}:{job_tag}")

    # Remove the original tag
    client.images.remove(container_name)
    # Remove the temp container
    container.remove()


def dump(response, query: Optional[str] = None):
    """load, a response, optionally apply a query to its returned json, and then pretty print the result."""
    content = response
    if hasattr(response, "json"):
        content = response.json()  # shorthand for json.loads(response.text)
    if query:
        try:
            content = jmespath.search(query, content)
        except jmespath.exceptions.ParseError as e:
            print("Error parsing response")
            raise e

    return json.dumps(
        {"response": content},
        indent=4,
    )


def upload_from_file(tarred: io.BytesIO, dst: str, json_output: bool = False):
    """Upload a file from src (a path on the filesystm) to dst.

    e Args:
         tarred (io.BytesIO): The file to upload. (e.g. a tarred file).
         dst (str): The url of the destination.
         Must be a url to which we have permission to send the src, via PUT.
         json_output (bool, optional): Whether to output the progress in json format. Defaults to False.

    Returns:
         Tuple[str, requests.Response]: A hash of the file, and the response from the put request.
    """
    if json_output:
        tarred.seek(0)
        response = requests.put(dst, data=tarred)
        response.raise_for_status()
        return response
    else:
        with tqdm(
            desc="Uploading",
            total=tarred.getbuffer().nbytes,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
        ) as t:
            tarred.seek(0)
            reader_wrapper = CallbackIOWrapper(t.update, tarred, "read")
            response = requests.put(dst, data=reader_wrapper)
            response.raise_for_status()
            return response


def exception_to_json_error(e: Exception):
    """Convert an exception to a json string with the error message and type."""
    logger.error(e)
    error_dict = {"status": "failed", "error": str(e), "type": type(e).__name__}
    if hasattr(e, "status_code"):
        error_dict["status_code"] = e.status_code
    return json.dumps(error_dict, indent=4)


console = Console()


def json_output_decorator(function):
    """Decorator to print the output as a JSON dump if --json is true; else (rich) print the output."""

    def wrapper(*args, json_output: bool = False, **kwargs):
        result = function(*args, json_output, **kwargs)
        if json_output:  # If json_output flag is present (cf typer options in main.py)
            if isinstance(result, str):  # Print any dump() output directly
                print(result)
            else:  # Print any other output as json string by converting it first
                result_json = dump(result)
                print(result_json)
        else:  # If json_output flag is not present (cf typer options in main.py)
            if isinstance(result, str):
                result_json = result
            else:
                result_json = dump(result)  # Use dump() logic to access full response

            result_dict = json.loads(result_json)  # Unpack response string into dict
            result = result_dict["response"]  # Extract the 'response' item of the status/response dict
            # Once converted, print the respomse using Rich table
            if "experiment" in result or "experiments" in result:
                table = Table(
                    "Name",
                    "Status",
                    "Results",
                    show_header=True,
                    header_style="bold magenta",
                )
                if "experiments" in result:
                    experiments = result["experiments"]
                    # Initialising flat list of all jobs
                    jobs = []
                    for experiment in experiments:
                        if "jobs" in experiment:
                            jobs = experiment["jobs"]

                            if "tasks" in jobs[0]:
                                tasks = jobs[0]["tasks"]
                                # List of job names, statuses, and results
                                names = []
                                statuses = []
                                results = []

                                for task in tasks:
                                    names.append(task["name"])
                                    statuses.append(task["status"])
                                    results.append(task["results"])

                                # Adding rows to table, avoiding duplicates
                                for i in range(len(tasks)):
                                    if i == 0 or tasks[i]["name"] != tasks[i - 1]["name"]:
                                        table.add_row(str(names[i]), str(statuses[i]), str(results[i]))

            elif all(key in item for key in ["name", "status", "message", "results"] for item in result):
                table = Table(
                    "Name",
                    "Status",
                    "Results",
                    show_header=True,
                    header_style="bold magenta",
                )

                for item in result:
                    table.add_row(str(item["name"]), str(item["status"]), str(item["results"]))

            elif "message" in result:  # For status messages (e.g. iris post, iris delete, error handling)
                if "output" not in result:
                    result["output"] = "None"
                table = Table(
                    "Status",
                    "Message",
                    "Output",
                    show_header=True,
                    header_style="bold magenta",
                )
                if "status" in result:
                    table.add_row(
                        str(result["status"]),
                        str(result["message"]),
                        str(result["output"]),
                    )
                else:
                    table.add_row(
                        "", str(result["message"]), str(result["output"])
                    )  # this will never happen but just for testing

            else:
                for key, value in result.items():
                    table = Table(show_header=True, header_style="bold magenta")
                    table.add_column(key)
                    table.add_row(str(value))

            console.print(table)

        return result

    return wrapper


def telemetry_decorator(function: Callable):
    """Decorator to send telemetry data to the metrics server."""

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        # Nickname is only present if the user is logged in, and
        # if the user is _a user_ i.e. not a client credentials flow machine.
        nickname = (
            conf_mgr.current_user["nickname"]
            if conf_mgr.current_user is not None and "nickname" in conf_mgr.current_user
            else None
        )
        # if str(obj) (w/ obj in args) contains any of these strings, it won't be sent
        mask_args = ["Authorization"]

        # any kwargs with these keys won't be sent
        mask_kwargs = []

        url = conf_mgr.metrics_url

        try:
            func = function(*args, **kwargs)

            headers = {"Content-Type": "application/json"}
            headers.update({"Authorization": f"Bearer {conf_mgr.access_token}"})
            payload = {
                "username": nickname,
                "method": function.__name__,
                "args": tuple(str(i) for i in args if all(arg not in str(i) for arg in mask_args)),
                "kwargs": {k: v for k, v in kwargs.items() if all(arg not in k for arg in mask_kwargs)},
                "error": None,
            }
            requests.post(url=url, headers=headers, json=payload)

            return func
        except requests.exceptions.ConnectionError:  # a more understandable message than the default ConnectionError
            ConnectionErrorMsg = json.dumps(
                {
                    "status": "failed",
                    "error": f"Error reaching {url}. Please check your internet connection.",
                    "type": "ConnectionError",
                },
                indent=4,
            )
            logger.error(str(ConnectionErrorMsg))
        except Exception as e:
            try:
                headers = {"Content-Type": "application/json"}
                headers.update({"Authorization": f"Bearer {conf_mgr.access_token}"})
                url = conf_mgr.metrics_url

                payload = {
                    "username": nickname,
                    "method": function.__name__,
                    "args": tuple(str(i) for i in args if all(arg not in str(i) for arg in mask_args)),
                    "kwargs": {k: v for k, v in kwargs.items() if k not in mask_kwargs},
                    "error": str(e),
                }
                requests.post(url=url, headers=headers, json=payload)
            except Exception as exc:
                raise exc

            raise e.with_traceback(None)

    @functools.wraps(function)
    def dummy_wrapper(*args, **kwargs):
        return function(*args, **kwargs)

    return wrapper if conf_mgr.TELEMETRY else dummy_wrapper
