"""This module provide aux functions to distinct proposes"""

from mindsight_auth_api.settings import API_SERVER, API_COMPANY, API_VERSION


def generate_url(
    base_path: str,
    path: str,
    api_server: str = API_SERVER,
    api_company: str = API_COMPANY,
    api_version: str = API_VERSION
) -> str:
    """Aux function to generate a URL in Api format"""
    return f"https://{api_server}/{api_company}/api/{api_version}{base_path}{path}"


def remove_none_fields(data: dict):
    result = {}
    for key, value in data.items():
        if value is not None:
            result[key] = value
    return result
