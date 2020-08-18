# Proofdock chaos middleware for Flask

![CI](https://github.com/proofdock/chaos-middleware-python/workflows/CI/badge.svg?branch=master)
[![Python versions](https://img.shields.io/pypi/pyversions/proofdock-chaos-middleware-flask.svg)](https://www.python.org/)

Practice chaos engineering on the Flask framework. This project is a Flask contribution to the `proofdock-chaos-middleware-python` project.

## Project description

This project is part of Proofdock's [**Chaos Platform**][proofdock] that supports you to **attack your service application with turbulent and unexpected conditions** in order to improve its resiliency.

For more information visit our official [website][proofdock] or [documentation][proofdock_docs]. Feel free to ask for support for this package on [GitHub][proofdock_support].

## Install

This package requires Python 3.5+

```
$ pip install -U proofdock-chaos-middleware-flask
```

## Usage

Read the [**documentation**][proofdock_middleware_docs] to understand the usage of the chaos middleware project.

## Configuration

The chaos middleware for Flask takes the following **input variables**:

| Variable | Description |
| ---      | ---         |
| `CHAOS_MIDDLEWARE_APPLICATION_NAME` | The service application's name |
| `CHAOS_MIDDLEWARE_APPLICATION_ENVIRONMENT` | The service application's deployed environment |
| `CHAOS_MIDDLEWARE_API_TOKEN` | The API token to connect to Proofdock's Chaos API |

The **configuration** exemplified as **code**:

```python
from flask import Flask, jsonify
from pdchaos.middleware.contrib.flask.flask_middleware import FlaskMiddleware

app = Flask(__name__)
app.config['CHAOS_MIDDLEWARE_APPLICATION_NAME'] = 'example-application-name'
app.config['CHAOS_MIDDLEWARE_APPLICATION_ENV'] = 'example-environment'
app.config['CHAOS_MIDDLEWARE_PROOFDOCK_API_TOKEN'] = 'eyJ0eXAi...05'

middleware = FlaskMiddleware(app)

# Your business logic here

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()

```

## References

- [Proofdock chaos middleware][proofdock_middleware_repo]

[proofdock]: https://proofdock.io/
[proofdock_docs]: https://docs.proofdock.io/
[proofdock_support]: https://github.com/proofdock/chaos-support/
[proofdock_middleware_repo]: https://github.com/proofdock/chaos-middleware-python
[proofdock_middleware_docs]: https://docs.proofdock.io/chaos/middleware