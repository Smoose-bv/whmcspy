# WHMCSpy

WHMCSpy is a Python interface to the WHMCS REST API.

[![PyPI version](https://badge.fury.io/py/whmcspy.svg)](https://badge.fury.io/py/whmcspy)
[![Documentation Status](https://readthedocs.org/projects/whmcspy/badge/?version=latest)](https://whmcspy.readthedocs.io/en/latest/?badge=latest)

## Usage

Create a WHMCS interface with the API URL and credentials and use it to
call the API.

```python
import whmcspy

whmcs = whmcspy.WHMCS(
    'https://example.com/whmcs/includes/api.php',
    'identifier',
    'secret')
whmcs.accept_order(2)
```
