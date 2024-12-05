"""This module provide methods to work with users entity"""

from datetime import datetime
from typing import Literal

from mindsight_auth_api.helpers.models import (
    ApiEndpoint,
    ApiPaginationResponse,
)
from mindsight_auth_api.settings import (
    API_ENDPOINT_USERS,
    DATETIME_FORMAT
)


class Users(ApiEndpoint):
    """This class abstract mindsight auth api endpoints
    """

    def __init__(self) -> None:
        super().__init__(API_ENDPOINT_USERS)

    def get_list_users(
        self,
        expand: Literal["system_access_config", "uuid"] = None,
    ) -> ApiPaginationResponse:
        """Get list of users from mindsight auth

        Args:
            expand: A search term.
        """

        path = "/"
        parameters = {
            "expand": expand,
            "page_size": self.page_size,
        }
        return ApiPaginationResponse(
            **self._base_requests.get(path=path, parameters=parameters),
            headers=self._base_requests.headers,
        )

    def get_retrieve_user(
        self,
        id: int,
        expand: Literal["system_access_config", "uuid"] = None,
    ) -> dict:
        """Get retrieve user

        Args:
            id (int, Mandatory): Id of user to retrieve
            expand (str, Optional): Possible to expand these felds in the response: system_access_config, uuid
        """
        path = f"/{id}/"

        parameters = {
            "expand": expand,
        }
        return self._base_requests.get(
            path=path,
            parameters=parameters,
        )

    def post_create_user(
        self,
        username: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None,
        is_superuser: bool = False,
        date_joined: datetime = datetime.now(),
    ):
        """Create new user

        Args:
            username (str, Mandatory): Username with 254 characters or fewer.
                Letters, digits and @/./+/-/_ only
            email (str, Optional): User email with 254 characters or fewer
            first_name (str, Optional): User first name with 100 characters or fewer
            last_name (str, Optional): User last name with 150 characters or fewer
            is_superuser (bool, Optional): Super user permission
            date_joined (datetime, Optional): Datetime of user joined
        """
        path = "/"
        data = {
            "username": username,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "is_superuser": is_superuser,
            "date_joined": date_joined.strftime(DATETIME_FORMAT)
            if date_joined
            else None,
        }

        return self._base_requests.post(path=path, json=data)

    def patch_update_user(
        self,
        id: int,
        username: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None,
        is_superuser: bool = None,
        date_joined: datetime = None,
    ) -> dict:
        """Edit partial user register

        Args:
            id (int, Mandatory): A unique integer value identifying this user.
            username (str, Mandatory): Username with 254 characters or fewer.
                Letters, digits and @/./+/-/_ only
            email (str, Optional): User email with 254 characters or fewer
            first_name (str, Optional): User first name with 100 characters or fewer
            last_name (str, Optional): User last name with 150 characters or fewer
            is_superuser (bool, Optional): Super user permission
            is_staff (bool, Optional): Access to admin site
            is_active (bool, Optional): Access to front site
            last_login (datetime, Optional): Datetime of last login
            date_joined (datetime, Optional): Datetime of user joined
        """
        path = f"/{id}/"
        data = {
            "username": username,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "is_superuser": is_superuser,
            "date_joined": date_joined.strftime(DATETIME_FORMAT)
            if date_joined
            else None,
        }
        return self._base_requests.patch(path=path, json=data)

    def put_full_update_user(
        self,
        id: int,
        username: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None,
        is_superuser: bool = False,
        date_joined: datetime = None,
    ) -> dict:
        """Edit full user register

        Args:
            id (int, Mandatory): A unique integer value identifying this user.
            username (str, Mandatory): Username with 254 characters or fewer.
                Letters, digits and @/./+/-/_ only
            email (str, Optional): User email with 254 characters or fewer
            first_name (str, Optional): User first name with 100 characters or fewer
            last_name (str, Optional): User last name with 150 characters or fewer
            is_superuser (bool, Optional): Super user permission
            is_staff (bool, Optional): Access to admin site
            is_active (bool, Optional): Access to front site
            last_login (datetime, Optional): Datetime of last login
            date_joined (datetime, Optional): Datetime of user joined
        """
        path = f"/{id}/"
        data = {
            "username": username,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "is_superuser": is_superuser,
            "date_joined": date_joined.strftime(DATETIME_FORMAT)
            if date_joined
            else None,
        }
        return self._base_requests.put(path=path, data=data)

    def delete_destroy_user(self, id: int):
        """Delete user

        Args:
            id (int, Mandatory): User id
            search (str, Optional): Search term
        """
        path = f"/{id}/"
        return self._base_requests.delete(path=path)

    def update_or_create_user(
        self,
        username: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None,
        is_active: bool = False,
    ):
        """Create new area

        Args:
            username (str, Mandatory): Username with 254 characters or fewer.
                Letters, digits and @/./+/-/_ only
            email (str, Optional): User email with 254 characters or fewer
            first_name (str, Optional): User first name with 100 characters or fewer
            last_name (str, Optional): User last name with 150 characters or fewer
            is_active (bool, Optional): Designates whether this user should be treated as active.
        """
        path = "/"
        data = {
            "username": username,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "is_active": is_active
        }

        return self._base_requests.post(path=path, json=data)
