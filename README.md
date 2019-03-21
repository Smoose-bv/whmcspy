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

In general API methods can be called as methods in the WHMCS class. For
available API methods see the [WHMCS API reference](
https://developers.whmcs.com/api-reference/).
Note that the casing of the methods differ from the API actions. While the
API actions are CamelCased the methods are snake_cased.

### Calling unimplemented actions

Not all API actions are implemented as Python methods (they will be
implemented as required, of course pull-requests are accepted). In order to
call actions that are not yet implemented [call()] can be used. Example:

```python
response = whmcs.call(
    'SomeAction',
    param=value,
    list_param=[
        element,
        element2,
    ]
)
```

See the [call()] documentation for more info.

Some actions return batches of results. To iterate over all results multiple
requests need to be done. For this a convenience method is added:
[paginated_call()]
This method is a generator which yields batches. Using keywords additional
params are accepted. Example:

```python
for response in whmcs.paginated_call(
        'GetOrders'):
    for order in response['orders']['order']:
        print(order)
```

[call()]: https://whmcspy.readthedocs.io/en/latest/whmcspy.html#whmcspy.api.WHMCS.call
[paginated_call()]: https://whmcspy.readthedocs.io/en/latest/whmcspy.html#whmcspy.api.WHMCS.paginated_call
