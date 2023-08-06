import os
import importlib
import json
import time
import threading
from pathlib import Path
import shutil
import urllib.parse
import io
from typing import Union, List, Any, Dict, TypedDict, Optional
from zipfile import ZipFile
import asyncio
import aiohttp
import typer
from rich import print
import requests
from sidetrek.cli_commands.constants import APP_NAME, GENERATED_LOCAL_SIDETREK_DIRNAME, USER_REPO_SRC_DIRNAME


class FetchInput(TypedDict):
    url: str
    method: str
    data: Optional[Any]
    headers: Optional[Dict[str, Any]]


async def fetch(session: aiohttp.ClientSession, fetch_input: FetchInput) -> Dict[Any, Any]:
    """
    Execute an http call async
    - session: aiohttp context for making the http call
    - url: URL to call
    """
    url = fetch_input.get("url")
    method = fetch_input.get("method")
    data = fetch_input.get("data", {})
    headers = fetch_input.get("headers", {})

    if method == "get":
        async with session.get(url, headers=headers) as response:
            resp = await response.json()
            return resp
    if method == "delete":
        async with session.delete(url, headers=headers) as response:
            resp = await response.json()
            return resp
    if method == "post":
        async with session.post(url, data=data, headers=headers) as response:
            resp = await response.json()
            return resp
    if method == "put":
        async with session.put(url, data=data, headers=headers) as response:
            resp = await response.json()
            return resp


async def fetch_all(fetch_inputs: List[FetchInput]) -> List[Dict[Any, Any]]:
    """
    Gather many HTTP call made async in parallel
    """
    async with aiohttp.ClientSession() as session:
        tasks = []
        for fetch_input in fetch_inputs:
            tasks.append(fetch(session, fetch_input))
        res_list = await asyncio.gather(*tasks, return_exceptions=True)
        return res_list


def get_node_env():
    if os.environ.get("NODE_ENV") == "development":
        return "development"
    elif os.environ.get("NODE_ENV") == "staging":
        return "staging"
    else:
        return "production"


def version_callback(value: bool):
    if value:
        version = importlib.metadata.version("sidetrek")
        print(f"Sidetrek CLI version: {version}")
        raise typer.Exit()


def print_timer(seconds: int = 1):
    start_time = time.time()

    def loop():
        while True:
            time.sleep(seconds)
            current_time = time.time()
            elapsed_time = current_time - start_time
            print(f"\r{elapsed_time} seconds...")

    threading.Thread(target=loop).start()


def get_auth_api_base_url():
    node_env = get_node_env()
    if node_env == "development":
        return f"http://localhost:4002/api/v1"
    elif node_env == "staging":
        return f"https://auth-staging.sidetrek.com/api/v1"
    else:
        return f"https://auth.sidetrek.com/api/v1"


def get_user_machine_node_api_base_url(user_id):
    node_env = get_node_env()
    if node_env == "development":
        return f"http://localhost:4008/p/api/v1"
    elif node_env == "staging":
        return f"https://user-machines.sidetrek.com/{user_id}/node/p/api/v1"
    else:
        return f"https://user-machines.sidetrek.com/{user_id}/node/p/api/v1"


def get_webapp_api_base_url():
    node_env = get_node_env()
    if node_env == "development":
        return f"http://localhost:4001/p/app/api/v1"
    elif node_env == "staging":
        return f"https://app-staging.sidetrek.com/p/app/api/v1"
    else:
        return f"https://app.sidetrek.com/p/app/api/v1"


def get_webapp_public_api_base_url():
    node_env = get_node_env()
    if node_env == "development":
        return f"http://app-dev-svc.sidetrek.com/app/api/v1"
    elif node_env == "staging":
        return f"https://app-staging.sidetrek.com/app/api/v1"
    else:
        return f"https://app.sidetrek.com/app/api/v1"


def get_generated_local_sidetrek_dir_path() -> Path:
    app_dir = typer.get_app_dir(APP_NAME)
    generated_local_sidetrek_dir_path = Path(app_dir) / GENERATED_LOCAL_SIDETREK_DIRNAME
    Path(generated_local_sidetrek_dir_path).mkdir(parents=True, exist_ok=True)
    return generated_local_sidetrek_dir_path


# def get_generated_project_dir_path() -> Path:
#     generated_local_sidetrek_dir_path = get_generated_local_sidetrek_dir_path()
#     generated_project_dir_path = Path(generated_local_sidetrek_dir_path) / GENERATED_PROJECT_DIRNAME
#     Path(generated_project_dir_path).mkdir(parents=True, exist_ok=True)
#     return generated_project_dir_path


def get_generated_workflow_name(workflow_id: str) -> str:
    """
    This is the name of the workflow function (i.e. fn def under @workflow)
    """
    return f"wf_{workflow_id}"


def get_workflow_file_path(workflow_id: int) -> Path:
    generated_local_sidetrek_dir_path = get_generated_local_sidetrek_dir_path()
    return Path(f"{generated_local_sidetrek_dir_path}/{USER_REPO_SRC_DIRNAME}/wf_{workflow_id}.py")


def raise_fail_to_authenticate():
    print("[red]Failed to authenticate.[/red]")
    print("Please login first - run: '[blue]sidetrek login[/blue]'\n")
    raise typer.Exit()


def get_credentials() -> Union[dict, None]:
    """
    Get credentials from the saved file (from login)

    If credentials don't exist, raise an except with error message asking to login first
    """
    app_dir = typer.get_app_dir(APP_NAME)
    creds_path: Path = Path(app_dir) / ".credentials"

    creds_exists = Path(creds_path).is_file()

    if not creds_exists:
        raise_fail_to_authenticate()

    with open(creds_path, "r") as f:
        creds = json.load(f)
        return creds


def get_credentials_header_str() -> str:
    creds = get_credentials()
    creds_header_str = "; ".join([str(x) + "=" + str(y) for x, y in creds.items()])
    return creds_header_str


def get_token() -> str:
    try:
        creds_header_str = get_credentials_header_str()
        auth_api_base_url = get_auth_api_base_url()
        refresh_session_res = requests.get(f"{auth_api_base_url}/auth/refresh-session", headers={"Cookie": creds_header_str})
        refresh_session = refresh_session_res.json()
        id_token = refresh_session["idToken"]
        return id_token
    except requests.exceptions.HTTPError as errh:
        print(f"{errh.response.status_code} {errh.response.text}")
        raise typer.Exit()
    except requests.exceptions.RequestException as err:
        print("Something went wrong: ", err)
        raise typer.Exit()


def get_headers() -> dict:
    token = get_token()
    return {"content-type": "application/json", "authorization": f"Bearer {token}"}


def get_auth_user() -> Union[dict, None]:
    try:
        # Retrieve the currently authenticated user from Cognito by using saved refresh token
        creds_header_str = get_credentials_header_str()
        auth_api_base_url = get_auth_api_base_url()
        auth_user_res = requests.get(f"{auth_api_base_url}/auth/current-user", headers={"Cookie": creds_header_str})
        auth_user_res.raise_for_status()
        return auth_user_res.json()
    except requests.exceptions.HTTPError as errh:
        print(f"{errh.response.status_code} {errh.response.text}")
        raise typer.Exit()
    except requests.exceptions.RequestException as err:
        print("Something went wrong: ", err)
        raise typer.Exit()


def get_current_user() -> Union[dict, None]:
    try:
        auth_user = get_auth_user()

        # Retrieve user from webapp db
        webapp_api_base_url = get_webapp_api_base_url()
        current_user_res = requests.get(f"{webapp_api_base_url}/users", params={"email": auth_user["email"]}, headers=get_headers())
        current_user = current_user_res.json()
        return current_user["data"]
    except requests.exceptions.HTTPError as errh:
        print(f"{errh.response.status_code} {errh.response.text}")
        raise typer.Exit()
    except requests.exceptions.RequestException as err:
        print("Something went wrong: ", err)
        raise typer.Exit()


def get_aws_creds() -> Union[dict, None]:
    try:
        # Retrieve aws credentials from cognito identity pool
        creds_header_str = get_credentials_header_str()
        auth_api_base_url = get_auth_api_base_url()
        aws_creds_res = requests.get(f"{auth_api_base_url}/auth/aws-credentials", headers={"Cookie": creds_header_str})
        aws_creds_res.raise_for_status()
        aws_creds = aws_creds_res.json()
        return aws_creds["data"]
    except requests.exceptions.HTTPError as errh:
        print(f"{errh.response.status_code} {errh.response.text}")
        raise typer.Exit()
    except requests.exceptions.RequestException as err:
        print("Something went wrong: ", err)
        raise typer.Exit()


def get_workflow_draft_version(workflow_id: int) -> Union[dict, None]:
    try:
        webapp_api_base_url = get_webapp_api_base_url()
        include = {"organization": True, "project": True, "domain": True, "workflow": True}
        include_json_str = json.dumps(include)
        workflow_version_res = requests.get(f"{webapp_api_base_url}/workflow-versions?isDraft=true&workflowId={workflow_id}&include={include_json_str}", headers=get_headers())
        workflow_version_res.raise_for_status()
        workflow_version = workflow_version_res.json()
        return workflow_version["data"]
    except requests.exceptions.HTTPError as errh:
        print(f"{errh.response.status_code} {errh.response.text}")
        raise typer.Exit()
    except requests.exceptions.RequestException as err:
        print("Something went wrong: ", err)
        raise typer.Exit()


async def get_dataset_collaborator_roles(dataset_ids: List[str]) -> Union[dict, None]:
    webapp_api_base_url = get_webapp_api_base_url()
    ds_collab_role_fetch_inputs = [
        {"method": "get", "url": f"{webapp_api_base_url}/datasets/{dataset_id}/collaborators/role", "headers": get_headers()} for dataset_id in dataset_ids
    ]
    ds_collab_roles_res = await fetch_all(ds_collab_role_fetch_inputs)
    # print(f"ds_collab_roles_res={ds_collab_roles_res}")

    # Check for error responses
    error_msgs = [f"[red]x [white]{x['errors'][0].get('detail')}" for x in ds_collab_roles_res if "errors" in x]
    if len(error_msgs) > 0:
        print(*error_msgs, sep="\n")
        raise typer.Exit()

    ds_collab_roles = [x["data"] for x in ds_collab_roles_res]
    return ds_collab_roles


def download_generated_flyte_workflow(user_id: str, workflow_version: dict) -> Path:
    """
    Gets the generated flyte workflow from pycodegen in the user machine and download it to a local dir

    Returns the path to the generated wf file
    """
    # First generate the flyte workflow in user machine and save it
    workflow = workflow_version["workflow"]
    generate_flyte_workflow(user_id, workflow_version)

    # Download the generated repo dir as a zip and unzip it to a local generated project dir
    try:
        generated_local_sidetrek_dir_path = get_generated_local_sidetrek_dir_path()
        user_machine_api_base_url = get_user_machine_node_api_base_url(user_id)
        encoded_repo_full_name = urllib.parse.quote(workflow["repoFullName"], safe="")
        repo_res = requests.get(f"{user_machine_api_base_url}/repos/download/{encoded_repo_full_name}", headers=get_headers())
        repo_res.raise_for_status()
        zip_file = ZipFile(io.BytesIO(repo_res.content))

        # First delete the generated project dir to reset...
        shutil.rmtree(generated_local_sidetrek_dir_path)

        # ...and then recreate the project dir and then unzip
        zip_file.extractall(generated_local_sidetrek_dir_path)

        # Return the generated wf file path
        generated_wf_file_path = get_workflow_file_path(workflow["id"])
        return generated_wf_file_path
    except requests.exceptions.HTTPError as errh:
        print(f"{errh.response.status_code} {errh.response.text}")
        raise typer.Exit()
    except requests.exceptions.RequestException as err:
        print("Something went wrong: ", err)
        raise typer.Exit()


def generate_flyte_workflow(user_id: str, workflow_version: dict) -> None:
    workflow = workflow_version["workflow"]
    ui_obj = json.loads(workflow_version["ui"])

    payload = json.dumps(
        {
            "organizationId": workflow_version["organizationId"],
            "projectId": workflow_version["projectId"],
            "workflow": {
                "id": workflow["id"],
                "versionId": workflow_version["id"],
                "repoFullName": workflow["repoFullName"],
                # "decoratorArgs": ""
            },
            "nodes": ui_obj["nodes"],
            "edges": ui_obj["edges"],
            # "mlflow": {
            #     "experiment_id": "",
            #     "tags": "",
            # }
        }
    )

    try:
        user_machine_api_base_url = get_user_machine_node_api_base_url(user_id)
        flyte_workflow_file_res = requests.post(f"{user_machine_api_base_url}/python/flyte-workflow-file/save", data=payload, headers=get_headers())
        flyte_workflow_file_res.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print(f"{errh.response.status_code} {errh.response.text}")
        raise typer.Exit()
    except requests.exceptions.RequestException as err:
        print("Something went wrong: ", err)
        raise typer.Exit()


def parse_pylint_errors(pylint_res: str, error_code: str):
    # Split into lines and filter out headers, footers, etc
    lines = [line for line in pylint_res.split("\n") if ".py" in line]
    print(f"lines={lines}")
    error_code_to_filter = error_code if error_code else "E"
    print(f"error_code_to_filter={error_code_to_filter}")
    # Ignore "E0401", which are import errors since this relates to relative paths :(
    errors = [{"code": line.split(": ")[1], "target": line.split("'")[1]} for line in lines if error_code_to_filter in line["code"] and line["code"] != "E0401"]
    return errors


def prepend_missing_imports(code: str, missing_imports: list[str]):
    if not missing_imports:
        return

    modules_to_add = [f"import {module_name}\n" for module_name in missing_imports]
    return "".join(modules_to_add) + code
