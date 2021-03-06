# Django integration

![CI](https://github.com/proofdock/chaos-middleware-python/workflows/CI/badge.svg?branch=master)
[![Python versions](https://img.shields.io/pypi/pyversions/proofdock-chaos-middleware-django.svg)](https://www.python.org/)

## Installation

This package requires Python 3.5+

```
$ pip install -U proofdock-chaos-middleware-django
```

## Usage

The chaos middleware takes the following **input variables**:

| Variable | Description |
| ---      | ---         |
| `CHAOS_MIDDLEWARE_APPLICATION_NAME` | The service application's name |
| `CHAOS_MIDDLEWARE_APPLICATION_ENV` | The service application's deployed environment |
| `CHAOS_MIDDLEWARE_PROOFDOCK_API_TOKEN` | The API token to connect to Proofdock's Chaos API |

The **configuration** exemplified as **code**:

```python
# file: settings.py
MIDDLEWARE = [
    '..'
    'pdchaos.middleware.contrib.django.django_middleware.DjangoMiddleware',
    '..'
]

# other settings ...

CHAOS_MIDDLEWARE = {
    'CHAOS_MIDDLEWARE_APPLICATION_NAME': 'example-application-name',
    'CHAOS_MIDDLEWARE_APPLICATION_ENV': 'example-environment',
    'CHAOS_MIDDLEWARE_PROOFDOCK_API_TOKEN': 'eyJ0eXAi...05'
}
```

Start your Django application and create an attack using **HTTP request header** or **control panel**. Read more about attacks [here][attack_usage].


[attack_usage]: https://docs.proofdock.io/chaos/middleware/about/#usage
