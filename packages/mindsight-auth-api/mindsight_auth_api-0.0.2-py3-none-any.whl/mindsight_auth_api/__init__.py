from mindsight_auth_api.src.auth import Users


class MindsightAuthApi:
    """This class represents an interface to access the methods
    available in this library.

    Usage example:
        ```python
        # Using this library to retrieve all users records
        import os
        os.environ["MINDSIGHT_AUTH_API_TOKEN"] = "token"
        os.environ["MINDSIGHT_AUTH_API_COMPANY"] = "your_company"
        os.environ["MINDSIGHT_AUTH_API_SERVER"] = "your.server"
        os.environ["MINDSIGHT_AUTH_API_VERSION"] = "v1"             # Default value "v1"

        from mindsight_auth_api import MindsightAuthApi


        users = MindsightAuthApi.users()

        data = users.get_list_users().get_all().results
        ```
    """

    @classmethod
    def users(cls) -> Users:
        return Users()
