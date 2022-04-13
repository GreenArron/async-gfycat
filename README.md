Async Gfycat
=========

An async Python wrapper for the [Gfycat API](https://gfycat.com/api).

based on [py-gfycat](https://github.com/ankeshanand/py-gfycat) a sync wrapper 
(api endpoints of py-gfycat are outdated as of 0.2.2)

<!-- shields -->
[![PyPi Package Version](https://img.shields.io/pypi/v/async-gfycat.svg)](https://pypi.python.org/pypi/async-gfycat)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/async-gfycat.svg)](https://pypi.python.org/pypi/async-gfycat)

<!-- shields -->

Installation
---
```bash
    pip install -U async-gfycat
```

Gfycat API Key
---
Go to https://developers.gfycat.com/signup/#/apiform and sign up for an API key if you don't already have one.

You need the Client ID and Client Secret to use for initializing the Python client.


Getting Started
---
```python
    from async_gfycat.client import GfycatClient

    client = GfycatClient(clientid, secret)

    # Example request
    await client.upload_from_file('willsmith.gif', title='willsmith slap')
```

you can also use username and password authentication with

```python
client = GfycatClient(clientid, secret, username, password)
```



Error Handling
--------------

* GfycatClientError - General error handler, access message and status code and the response dict with

```python
from gfycat.error import GfycatClientError
from pprint import pprint 

try
    ...
except GfycatClientError as e
    print(e.error_message)
    print(e.status_code)
    pprint(e.response_data)

```

GfycatClient Class Methods
----------------------

**Uploads**

-  ``upload_from_url(url)``
-  ``upload_from_file(filepath)``

> Warning: using ``check_upload()`` immediately after uploading a file may 
result in a NotFoundo response, in that case waiting a moment will fix the issue, this is an api issue not a client one

**Query a GFY for URLs and more information**

-  ``query_gfy(gfyname)``

**Check if an upload has been converted**

-  ``check_upload(link)``
  
  all methods return coros and need to be awaited

