# Chaos Middleware for Python

![CI](https://github.com/proofdock/chaos-middleware-python/workflows/CI/badge.svg?branch=master)
![Coverage](https://codecov.io/gh/proofdock/chaos-middleware-python/branch/master/graph/badge.svg)
[![Python versions](https://img.shields.io/pypi/pyversions/proofdock-chaos-middleware-python.svg)](https://www.python.org/)

The ``Chaos Middleware`` lets you practice chaos engineering on the **application level** by injecting **delays** and **faults** to simulate turbulent conditions. By specifying routes, the ``Chaos Middleware`` enables you to **minimize the blast radius** and keep the focus on the interesting parts of your application.

## Project description

This project is part of Proofdock's [**Chaos Platform**][proofdock] that lets you **simulate application outages and errors** in order to improve your system's resiliency.

## Integrations

Chaos Middleware supports integration with popular web frameworks:
- [Flask][flask_integration]
- [Django][django_integration]

## References

- [Chaos Middleware repository][proofdock_middleware_repo]
- [Support][proofdock_support]

[proofdock]: https://proofdock.io/
[proofdock_support]: https://github.com/proofdock/chaos-support/
[proofdock_middleware_repo]: https://github.com/proofdock/chaos-middleware-python
[flask_integration]: ./src/contrib-flask
[django_integration]: ./src/contrib-django
