import os
import sys
import json
import time
import threading
from pathlib import Path
import asyncio
from functools import wraps
import typer
import subprocess
from time import sleep
from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn
from sidetrek.cli_commands.helpers import (
    get_current_user,
    get_aws_creds,
    get_generated_local_sidetrek_dir_path,
    get_generated_workflow_name,
    download_generated_flyte_workflow,
    get_workflow_draft_version,
    get_dataset_collaborator_roles,
    print_timer,
)


# Make typer async
class AsyncTyper(typer.Typer):
    def async_command(self, *args, **kwargs):
        def decorator(async_func):
            @wraps(async_func)
            def sync_func(*_args, **_kwargs):
                return asyncio.run(async_func(*_args, **_kwargs))

            self.command(*args, **kwargs)(sync_func)
            return async_func

        return decorator


app = AsyncTyper()


@app.async_command()
async def run(workflow_id: int = typer.Option(...), workflow_args: str = "{}"):
    """
    Execute the workflow locally (e.g. for testing).

    * You can retrieve the --workflow-id (e.g. 42) from Sidetrek app.
    * Workflow version used it always `draft` for this command
    * --workflow-args is a stringified JSON of your workflow arguments (e.g. '{"learning_rate"=0.1, "epochs"=5}').
    """
    start_time = time.time()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        print("generated_local_sidetrek_dir_path", get_generated_local_sidetrek_dir_path())

        # Get current user
        auth_step = progress.add_task(description="Authenticating...", total=None)
        current_user = get_current_user()
        # print(f"current_user={current_user}")

        # Get temporary aws credentials and set it as env var for execution (grants temporary local s3 access for datasets)
        aws_creds = get_aws_creds()
        if aws_creds is None:
            raise Exception("Failed to get aws credentials")
        aws_env = {**os.environ, "AWS_ACCESS_KEY_ID": aws_creds["AccessKeyId"], "AWS_SECRET_ACCESS_KEY": aws_creds["SecretKey"], "AWS_SESSION_TOKEN": aws_creds["SessionToken"]}

        progress.remove_task(auth_step)
        time_elapsed = round(time.time() - start_time, 2)
        print(f"[green]✔️ [white]Authenticated [cyan]({time_elapsed}s)")

        # Always use the draft version for testing
        wf_generation_step = progress.add_task(description="Generating the workflow...", total=None)
        workflow_version = get_workflow_draft_version(workflow_id=workflow_id)
        # print(f"workflow_version={workflow_version}")

        # Check dataset auth - i.e. make sure this user has access to the dataset they're trying to access
        wf_ui = json.loads(workflow_version["ui"])
        dataset_ids = [node.get("data", {}).get("datasetId") for node in wf_ui["nodes"] if node["type"] == "dataset"]
        ds_collab_roles = await get_dataset_collaborator_roles(dataset_ids)  # Will throw 401 and exit if the user is not a collaborator in any of the datasets
        # print(f"ds_collab_roles={ds_collab_roles}")

        # Generate the workflow file
        wf_file_path = download_generated_flyte_workflow(user_id=current_user["id"], workflow_version=workflow_version)
        generated_wf_name = get_generated_workflow_name(workflow_id)
        progress.remove_task(wf_generation_step)
        time_elapsed = round(time.time() - start_time, 2)
        print(f"[green]✔️ [white]Workflow generated [cyan]({time_elapsed}s) - {wf_file_path.as_posix()}")

        wf_execution_step = progress.add_task(description="Executing the workflow...", total=None)
        # print(" ".join(["pyflyte", "run", wf_file_path.as_posix(), generated_wf_name, "--_wf_args", workflow_args]))
        with subprocess.Popen(
            ["pyflyte", "run", wf_file_path, generated_wf_name, "--_wf_args", workflow_args],
            cwd=get_generated_local_sidetrek_dir_path(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True,
            env=aws_env,
        ) as process:
            for line in process.stdout:
                print(line, end="")

            _, error = process.communicate()

            if process.returncode != 0:
                time_elapsed = round(time.time() - start_time, 2)
                print(f"[light_coral]{error}")
                print(f"[red]✕ [white]Workflow execution failed [cyan]({time_elapsed}s)")
                raise typer.Exit()

            progress.remove_task(wf_execution_step)
            time_elapsed = round(time.time() - start_time, 2)
            print(f"[green]✔️ [white]Workflow execution completed 🎉 [cyan]({time_elapsed}s)")
