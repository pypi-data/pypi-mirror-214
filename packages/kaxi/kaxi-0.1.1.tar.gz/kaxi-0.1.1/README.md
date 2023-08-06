# kaxi

<p align="center">
    <em>Run pipelines similar to github actions</em>
</p>

<div align="center">

[![Package version](https://img.shields.io/pypi/v/kaxi?color=%2334D058&label=pypi%20package)](https://pypi.org/project/kaxi/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/gabrielguarisa/kaxi/releases)
[![License](https://img.shields.io/github/license/gabrielguarisa/kaxi)](https://github.com/gabrielguarisa/kaxi/blob/main/LICENSE)

</div>

## Installation

```bash
pip install kaxi
```

## Usage

You can run a pipeline by running the following command:

```bash
kaxi <pipeline_file>.yaml
```

Or you can programmatically run a pipeline by running the following command:

```python
from kaxi import Runner

runner = Runner(your_pipeline)
runner.execute()
```

## Pipeline file

A pipeline file is a yaml file that contains a list of steps to execute. Each step is a dictionary with the following keys:

- `uses`: The callable to execute (e.g. `pandas.read_csv`)
- `name` (optional): The name of the step
- `with` (optional): A dictionary of arguments to pass to the callable

If you want to use arguments without the respective name, you can use the `args` key inside the `with` dictionary.

### Example

```yaml
verbose: true

steps:
  - uses: os.path.isfile
    name: file_exists
    with:
      path: example.yaml

  - uses: kaxi.log.info
    with:
      args:
        - ${file_exists}
```

### Environment variables

You can use environment variables in your pipeline file by using the `${ENV_VAR}` syntax.

To define environment variables, you can set them inside the `enviroment` key:

```yaml
environment:
  ENV_VAR: value
```

Another way to use environment variables is to use the ouput of a step as an environment variable, this can be done by using the `name` of the step inside the `${}` syntax:

```yaml
steps:
  - uses: os.path.isfile
    name: file_exists
    with:
      path: example.yaml

  - uses: kaxi.log.info
    with:
      args:
        - ${file_exists}
```