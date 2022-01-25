# Description

Fold is a application development framework that focuses on configuration-defined plugins. 

# Dependencies

- Python >=3.10
- loguru
- pydantic

# Installation

## Pip

Download a wheel from [releases]. Install the wheel using

```bash
pip install <path to wheel>
```

## Poetry

Add this package to your project using

```
poetry add <url to gz release>
```

## Source

This project requires poetry for project management and its build system. Install poetry using

```
pip install poetry
```

Clone the project and open the terminal in the project root directory. Install the dependencies and build the wheel using

```
poetry install
poetry build
```

The build can be found in the `dist` folder. Install the wheel using

```
pip install <path to wheel>
```

# Usage

Fold objects can be classified as one of 3 types:

- Plugin
- PluginManager
- BaseConfig

Plugins provide some utility service while PluginManagers act as a gateway controller to plugins. These objects expect a configuration to be passed into them. The configuration spec is defined by the BaseConfig.

## Config

All configuration objects are built on top of pydantic models. 

Suppose we want to define our config spec as follows:

```yaml
# config.yml
---
log:
  sink: stdout
outputs:
  - stdout
  - name: file
    path: /tmp/output
```

Create the config model like so

```python
from typing import List

from pydantic import validator

from fold.core import BaseConfig, Content
from fold.plugins.logger import LogManager
from fold.plugins.outputs import OutputManager

class Config(BaseConfig):
    log: LogManager
    outputs: OutputManager

    @validator('log')
    def log(cls, value):
        return LogManager.parseConfig(value)
    
    @validator('outputs')
    def output(cls, value):
        return OutputManager.parseConfig(value)

path = "config.yml"
config = Config.fromPath(path)  # load and validate the config

print(config.dict())  # export the config as a dict
# {
#     "log": {
#         "sink": "<_io.TextIOWrapper name='<stdout>' mode='w' encoding='utf-8'>"
#     }
#     "outputs": {[
#         {
#             "name": "stdout"
#         },
#         {
#             "name": "file",
#             "path": "/tmp/output"
#         }
#     ]}
# }

```

The `Config` class defined above says the following:

- The `version` key is required and must be a `str`
- The `log` key is required and must be a `Content` type or `LogHandlerConfig` type
- The `outputs` key is required and must be a `Content` type or a list of `OutputHandlerConfig`
- The `log` key is validate

# Contibuting

Create a [pull request][pr]. A development guide can be found in the documentation.
# Support

Open an issue on [github][issues].

[releases]: https://github.com/modora/fold/releases
[issues]: https://github.com/modora/fold/issues
[pr]: https://github.com/modora/fold/pulls
