import json
from typing import Union, List, Any, Dict, TypedDict, Optional
import requests
from sidetrek.cli_commands.helpers import get_webapp_public_api_base_url


def get_flyte_exec_id(bentoml_model_tag: str) -> str:
    webapp_api_base_url = get_webapp_public_api_base_url()
    flyte_exec_id_res = requests.get(f"{webapp_api_base_url}/bentoml-public/models/execution-id?bentomlModelTag={bentoml_model_tag}")
    flyte_exec_id_res.raise_for_status()
    flyte_exec_id = flyte_exec_id_res.json()
    return flyte_exec_id["data"]
    # except requests.exceptions.HTTPError as errh:
    #     print(f"{errh.response.status_code} {errh.response.text}")
    # except requests.exceptions.RequestException as err:
    #     print("Something went wrong: ", err)
