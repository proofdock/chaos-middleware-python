# Chaos Middleware Python integration

![CI](https://github.com/proofdock/chaos-middleware-python/workflows/CI/badge.svg?branch=master)
[![Python versions](https://img.shields.io/pypi/pyversions/proofdock-chaos-middleware-flask.svg)](https://www.python.org/)

## Install

This package requires Python 3.5+

```
$ pip install -U proofdock-chaos-middleware-python
```

## Usage

The chaos middleware takes the following **input variables**:

| Variable | Description |
| ---      | ---         |
| `CHAOS_MIDDLEWARE_APPLICATION_NAME` | The service application's name |
| `CHAOS_MIDDLEWARE_APPLICATION_ENV` | The service application's deployed environment |
| `CHAOS_MIDDLEWARE_PROOFDOCK_API_TOKEN` | The API token to connect to Proofdock's Chaos API |

Integrations with custom frameworks or your custom application requires some integration efforts. It is best to look at **code examples** from our `src/contrib-*` modules in our [GitHub repository][proofdock_middleware_repo].


## References

- [Chaos Middleware documentation][proofdock_middleware_docs]
- [Chaos Middleware repository][proofdock_middleware_repo]
- [Support][proofdock_support]
- [Proofdock website][proofdock]

[proofdock]: https://proofdock.io/
[proofdock_support]: https://github.com/proofdock/chaos-support/
[proofdock_middleware_docs]: https://docs.proofdock.io/chaos/middleware/about/
[proofdock_middleware_repo]: https://github.com/proofdock/chaos-middleware-python
