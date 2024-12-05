"""This module provide a base to use requests for api"""

from typing import Any, Literal

import requests

from mindsight_auth_api.helpers.exceptions import BadRequestException, ServerErrorException
from mindsight_auth_api.settings import (
    API_TOKEN,
    TIMEOUT,
    API_SERVER,
    API_COMPANY,
    API_VERSION
)
from mindsight_auth_api.utils.aux_functions import (
    generate_url,
    remove_none_fields
)


class BaseRequests:
    """Aux class to communicate with mindsight api"""

    def __init__(
        self,
        api_server: str = None,
        api_version: str = None,
        api_company: str = None
    ) -> None:
        self.__token = API_TOKEN
        self.api_server = (
            API_SERVER
            if not api_server else api_server
        )
        self.api_company = (
            API_COMPANY
            if not api_company else api_company
        )
        self.api_version = API_VERSION if not api_version else api_version
        self.headers = None
        self.base_path = "/"
        self.timeout: int = TIMEOUT

    def __authorization_header(self) -> dict:
        return {
            "Authorization": f"Token {self.__token}",
            "Content-Type": "application/json",
        }

    def __check_response(self, response: requests.Response):
        content_text = response.text
        try:
            response.raise_for_status()

        except requests.HTTPError as http_error:

            if response.status_code == 400:
                raise BadRequestException(message=content_text) from http_error

            if response.status_code == 500:
                raise ServerErrorException(message=content_text) from http_error

            raise requests.HTTPError(http_error) from http_error

        except Exception as exc:
            raise exc

    def __request_helper(
        self,
        path: str,
        method: Literal["get", "post", "put", "patch", "delete"],
        headers: dict = None,
        query_parameters: dict = None,
        data: Any = None,
        json: Any = None,
    ):
        if not headers:
            headers = {}

        request_url = generate_url(base_path=self.base_path, path=path)
        self.headers = {**self.__authorization_header(), **headers}

        response = None
        method = method.lower()

        if method == "get":
            query_parameters["ordering"] = "id"
            response = requests.get(
                url=request_url,
                headers=self.headers,
                params=query_parameters,
                data=data,
                timeout=self.timeout,
            )

        elif method == "post":
            response = requests.post(
                url=request_url,
                headers=self.headers,
                params=query_parameters,
                data=data,
                json=json,
                timeout=self.timeout,
            )

        elif method == "put":
            response = requests.put(
                url=request_url,
                headers=self.headers,
                params=query_parameters,
                data=data,
                json=json,
                timeout=self.timeout,
            )

        elif method == "patch":
            response = requests.patch(
                url=request_url,
                headers=self.headers,
                params=query_parameters,
                data=data,
                json=json,
                timeout=self.timeout,
            )

        elif method == "delete":
            response = requests.delete(
                url=request_url,
                headers=self.headers,
                params=query_parameters,
                data=data,
                json=json,
                timeout=self.timeout,
            )

        # Check response
        self.__check_response(response)
        if response.status_code == 204:
            return response
        response_json = response.json()

        return response_json

    def get(
        self,
        path: str,
        headers: dict = None,
        parameters: dict = None,
    ) -> Any:
        """Use GET method on Rest API"""
        return self.__request_helper(
            path=path, method="get", headers=headers, query_parameters=parameters
        )

    def post(
        self,
        path: str,
        headers: dict = None,
        parameters: dict = None,
        data: Any = None,
        json: Any = None,
    ) -> Any:
        """Use POST method on Rest API"""
        return self.__request_helper(
            path=path,
            method="post",
            headers=headers,
            query_parameters=parameters,
            data=data,
            json=json,
        )

    def put(
        self,
        path: str,
        headers: dict = None,
        parameters: dict = None,
        data: Any = None,
        json: Any = None,
    ):
        """Use PUT method on Rest API"""
        return self.__request_helper(
            path=path,
            method="put",
            headers=headers,
            query_parameters=parameters,
            data=data,
            json=json,
        )

    def patch(
        self,
        path: str,
        headers: dict = None,
        parameters: dict = None,
        data: Any = None,
        json: Any = None,
    ):
        """Use PATCH method on Rest API"""
        return self.__request_helper(
            path=path,
            method="patch",
            headers=headers,
            query_parameters=parameters,
            data=remove_none_fields(data) if data else None,
            json=remove_none_fields(json) if json else None,
        )

    def delete(
        self,
        path: str,
        headers: dict = None,
        parameters: dict = None,
        data: Any = None,
    ):
        """Use DELETE method on Rest API"""
        return self.__request_helper(
            path=path,
            method="delete",
            headers=headers,
            query_parameters=parameters,
            data=data,
        )
