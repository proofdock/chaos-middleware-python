# Proofdock chaos middleware

![CI](https://github.com/proofdock/chaos-middleware-python/workflows/CI/badge.svg?branch=master)
[![Python versions](https://img.shields.io/pypi/pyversions/proofdock-chaos-middleware-flask.svg)](https://www.python.org/)

Practice chaos engineering on any Python application. This project is the `core` of the `proofdock-chaos-middleware-python` project.

## Project description

This project is part of Proofdock's [**Chaos Platform**][proofdock] that supports you to **attack your service application with turbulent and unexpected conditions** in order to improve its resiliency.

## Install

This package requires Python 3.5+

```
$ pip install -U proofdock-chaos-middleware-python
```

## Usage

Read the [**documentation**][proofdock_middleware_docs] to understand the usage of the chaos middleware project.

## Configuration

The chaos middleware takes the following **input variables**:

| Variable | Description |
| ---      | ---         |
| `CHAOS_MIDDLEWARE_APPLICATION_NAME` | The service application's name |
| `CHAOS_MIDDLEWARE_APPLICATION_ENV` | The service application's deployed environment |
| `CHAOS_MIDDLEWARE_PROOFDOCK_API_TOKEN` | The API token to connect to Proofdock's Chaos API |

Integrations with custom frameworks or your custom application requires some integration efforts. It is best to look at **code examples** from our `src/contrib-*` modules in our [GitHub repository][proofdock_middleware_repo].


## References

- [Proofdock chaos middleware][proofdock_middleware_repo]

[proofdock]: https://proofdock.io/
[proofdock_docs]: https://docs.proofdock.io/
[proofdock_support]: https://github.com/proofdock/chaos-support/
[proofdock_middleware_repo]: https://github.com/proofdock/chaos-middleware-python
[proofdock_middleware_docs]: https://docs.proofdock.io/chaos/middleware