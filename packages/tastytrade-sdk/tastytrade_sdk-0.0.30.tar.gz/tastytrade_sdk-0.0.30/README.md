[![Read the Docs (version)](https://img.shields.io/readthedocs/tastytrade-sdk/latest)](https://tastytrade-sdk.readthedocs.io/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/tastytrade-sdk)](https://pypi.org/project/tastytrade-sdk/)
[![PyPI - License](https://img.shields.io/pypi/l/tastytrade-sdk)](LICENSE)
[![Code style: pylint](https://img.shields.io/badge/Pylint-10.00/10-green)](https://pypi.org/project/pylint/)

# tastytrade-sdk-python

A python wrapper around the [tastytrade open API](https://developer.tastytrade.com/)

## Getting Started

### Install
```shell
pip install tastytrade-sdk
```

### Use It
```python
from tastytrade_sdk import Tastytrade

tastytrade = Tastytrade()

tastytrade.authentication.login(
    username='jane.doe@email.com',
    password='password'
)

tastytrade.instruments.get_active_equities()
```


## Read the Docs
https://tastytrade-sdk.readthedocs.io/