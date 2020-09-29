# Chaos Middleware for Flask

![CI](https://github.com/proofdock/chaos-middleware-python/workflows/CI/badge.svg?branch=master)
[![Python versions](https://img.shields.io/pypi/pyversions/proofdock-chaos-middleware-flask.svg)](https://www.python.org/)

## Installation

This package requires Python 3.5+

```
$ pip install -U proofdock-chaos-middleware-flask
```

## Usage

The chaos middleware for Flask takes the following **input variables**:

| Variable | Description |
| ---      | ---         |
| `CHAOS_MIDDLEWARE_APPLICATION_NAME` | The service application's name |
| `CHAOS_MIDDLEWARE_APPLICATION_ENV` | The service application's deployed environment |
| `CHAOS_MIDDLEWARE_PROOFDOCK_API_TOKEN` | The API token to connect to Proofdock's Chaos API |

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

Start your Flask application and create an attack using **HTTP request header** or **control panel**. Read more about attacks [here][attack_usage].

## References

- [Chaos Middleware repository][proofdock_middleware_repo]
- [Support][proofdock_support]

[proofdock]: https://proofdock.io/
[proofdock_support]: https://github.com/proofdock/chaos-support/
[proofdock_middleware_repo]: https://github.com/proofdock/chaos-middleware-python
[attack_usage]: https://docs.proofdock.io/chaos/middleware/about/#usage