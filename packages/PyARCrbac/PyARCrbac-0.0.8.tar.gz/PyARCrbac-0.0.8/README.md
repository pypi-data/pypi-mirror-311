# PyARCrbac ![PyPI - Downloads](https://img.shields.io/pypi/dm/pyarcrbac) ![PyPI - Version](https://img.shields.io/pypi/v/pyarcrbac)
PyARCrbac is a Python library that provides functions for retrieving tokens from azure arc-enabled servers using the local metadata service. It can be used to obtain access tokens for Azure resources.
## Installation
```shell
pip3 install pyarcrbac
```
## Usage
Here's an example of how to use PyARCrbac to retrieve an access token:
```python
from pyarcrbac import get_token

token = get_token()
print(token)
```
Make sure you have the necessary permissions and environment variables set up to access the azure metadata service.

## Documentation
The main function in PyARCrbac is get_token(), which retrieves the challenge token from the metadata service. It returns the access token as a JSON object.

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License.

## Contact
For any questions or inquiries, please open an issue.

## Disclaimer
I am not responsible for any damage and/or misuse as a result of using this lib.
