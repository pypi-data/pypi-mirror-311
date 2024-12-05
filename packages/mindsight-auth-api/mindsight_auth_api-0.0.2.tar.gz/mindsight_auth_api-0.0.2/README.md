# mindsight-auth-api
[![PyPI Latest Release](https://img.shields.io/pypi/v/mindsight-auth-api.svg)](https://pypi.org/project/mindsight-auth-api/)

Use mindsight auth functionalities in your python application.
## Instalation
```sh
pip install mindsight-auth-api
```

# Configuration
## Environment variables
To use mindsight-auth-api, you need to set two environment variables:
```dotenv
# ---DOTENV EXAMPLE---

MINDSIGHT_AUTH_API_TOKEN= # Token to authenticate
MINDSIGHT_AUTH_API_COMPANY=your-company
MINDSIGHT_AUTH_API_SERVER=your.server # Example auth.mindsight.com.br
MINDSIGHT_AUTH_API_VERSION=v1 # Default value is 'v1'
```
# Usage Example
You can use mindsight-auth-api in order to create, update and delete records.

## List registers
You can use get methods to list registers of system table. See the following example:
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