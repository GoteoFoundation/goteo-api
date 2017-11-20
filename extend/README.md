EXTEND
======

You can use this directory to place private packages extending the API.

Tell the API to load your own packages in the `config.py` by adding it to the `MODULES` var:

`config.py`:

```python

# Extend the API functionality by enabling additional modules/plugins
MODULES = {
    # reports endpoints
    'goteoapi_reports.controllers',
    # digests endpoints
    'goteoapi_digests.controllers',
    # Some custom plugin:
    'extend.your_plugin.your_front_controller'
}

```
