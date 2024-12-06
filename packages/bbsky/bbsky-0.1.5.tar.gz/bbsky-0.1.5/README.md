## Overview
    
[![PyPI](https://img.shields.io/pypi/v/bbsky)](https://pypi.org/project/bbsky/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![python](https://img.shields.io/badge/Python-3.10-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![python](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![python](https://img.shields.io/badge/Python-3.12-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)

`bbsky` provides a high-level Python client for interacting with the Blackbaud Sky API. 
You can use the client to authenticate and make requests to various endpoints provided by the Blackbaud Sky API.
See the Blackbaud Sky API documentation 
[here](https://developer.blackbaud.com/skyapi/) 
for more information on the Sky API itself.

**Important Note:** `bbsky` is a third-party client and is not affiliated with or endorsed by Blackbaud.

## Installation

To install the package, use pip:

```bash
pip install bbsky
```

## Usage

To see all available CLI commands, run:

```bash
bbsky --help
```

### Setting up Blackbaud App Credentials

First you'll need to setup your Blackbaud Sky account and then update your config.
After getting your credentials from Blackbaud, you can use the CLI here to set them up:

```bash
bbsky config --help

# Follow along with the prompts to set your credentials
bbsky config create
```

After that a config file will be created in your home directory at `~/.bbsky/config/config.json`.

### Getting a User Token

To get a user token, you can use the CLI:

```bash
bbsky server start
```

This will start a local server that you can use to authenticate with Blackbaud. 
After authenticating, you'll be prompted to cache the token locally.

If you need to refresh your token, run:
    
```bash
bbsky token refresh
```

### Using the Client

Here's a basic example of how to use the client:

```python
from bbsky import BBSky

sky = BBSky()
results = sky.search_constituents(constituent_quick_find="Smith", limit=5)
print(results)
```

## Development

[![Rye](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/rye/main/artwork/badge.json)](https://rye.astral.sh)


We use [Rye](https://rye.astral.sh/) for managing the development environment.
See the [Rye documentation](https://rye.astral.sh/guide/) for more information on how to use it.


