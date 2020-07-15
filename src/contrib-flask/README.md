# Proofdock chaos middleware for Flask

![CI](https://github.com/proofdock/chaos-middleware-python/workflows/CI/badge.svg?branch=master)
[![Python versions](https://img.shields.io/pypi/pyversions/proofdock-chaos-middleware-flask.svg)](https://www.python.org/)

Practice chaos engineering on the Flask framework. This project is a Flask contribution to the `proofdock-chaos-middleware-python` project.

## Project description

This project is part of the Proofdock Chaos Engineering Platform that helps you to write, run, store and analyze chaos experiments in your Azure DevOps environment.

For more information visit our official [website][proofdock] or [documentation][proofdock_docs]. Feel free to ask for support for this package on [GitHub][proofdock_support].

## Install

This package requires Python 3.5+

```
$ pip install -U proofdock-chaos-middleware-flask
```

## Usage

To be defined ...

## Configuration

Configure your Flask configuration with the following properties:

| Property | Flask configuration | Description |
| ---      | ---                 | ---         |
| `CHAOS_MIDDLEWARE_SERVICE_NAME` | `app.config.setdefault('CHAOS_MIDDLEWARE_SERVICE_NAME', '')` | Set up a service application name for your Flask app |
| `CHAOS_MIDDLEWARE_SERVICE_ENVIRONMENT` | `app.config.setdefault('CHAOS_MIDDLEWARE_SERVICE_ENVIRONMENT', '')` | The environment in which your service application is running |
| `CHAOS_MIDDLEWARE_API_TOKEN` | `app.config.setdefault('CHAOS_MIDDLEWARE_API_TOKEN', '')` | The API token to connect to Proofdock's Chaos API |

## References

- [Proofdock chaos middleware][proofdock_middleware_repo]

[proofdock]: https://proofdock.io/
[proofdock_docs]: https://docs.proofdock.io/
[proofdock_support]: https://github.com/proofdock/chaos-support/
[proofdock_middleware_repo]: https://github.com/proofdock/chaos-middleware-python