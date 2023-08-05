
# Dopt Blocks Python Library

[![pypi](https://img.shields.io/pypi/v/fern-dopt-blocks.svg)](https://pypi.python.org/pypi/fern-dopt-blocks)
[![fern shield](https://img.shields.io/badge/%F0%9F%8C%BF-SDK%20generated%20by%20Fern-brightgreen)](https://github.com/fern-api/fern)

## Documentation

API documentation is available [here](https://www.dopt.docs.buidlwithfern.com)

## Installation

Add this dependency to your project's build file:

```bash
pip install fern-dopt-blocks
# or
poetry add fern-dopt-blocks
```

## Usage

```python
from dopt.client import DoptBlocks

client = DoptBlocks(api_key="YOUR_API_KEY)
response = client.find_blocks(
  uid="xqC0wpZgoaYXbAPk8W0sk",
  user_identifier="example-user-idenitifer",
  version=3
);

print(response)
```

## Async Client

```python
import asyncio
from dopt.client import AsyncDoptBlocks

async_client = AsyncDoptBlocks(api_key="YOUR_API_KEY)

async def get_blocks() -> None:
    response = async_client.find_blocks(
      uid="xqC0wpZgoaYXbAPk8W0sk",
      user_identifier="example-user-idenitifer",
      version=3
    );
    print(response)

asyncio.run(get_blocks())
```

## Beta status

This SDK is in beta, and there may be breaking changes between versions without a major version update. Therefore, we recommend pinning the package version to a specific version in your pyproject.toml file. This way, you can install the same version each time without breaking changes unless you are intentionally looking for the latest version.

## Contributing

While we value open-source contributions to this SDK, this library is generated programmatically. Additions made directly to this library would have to be moved over to our generation code, otherwise they would be overwritten upon the next generated release. Feel free to open a PR as a proof of concept, but know that we will not be able to merge it as-is. We suggest opening an issue first to discuss with us!

On the other hand, contributions to the README are always very welcome!
