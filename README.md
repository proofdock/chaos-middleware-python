# Chaos Middleware for Python

![CI](https://github.com/proofdock/chaos-middleware-python/workflows/CI/badge.svg?branch=master)
[![Python versions](https://img.shields.io/pypi/pyversions/proofdock-chaos-middleware-python.svg)](https://www.python.org/)

The ``Chaos Middleware`` lets you practice chaos engineering on the application level. Put your system into turbulent conditions with application attacks. Inject delays and faults to simulate disbalances in your system. By specifying routes, the ``Chaos Middleware`` enables you to minimize the blast radius and keep the focus on the interesting parts of your application.

## Project description

This project is part of Proofdock's [**Chaos Platform**][proofdock] that lets you **simulate application outages and errors** in order to improve your system's resiliency.

## Installation & basic usage

This package requires Python 3.5+

1. Install the Chaos Middleware package:
   ```
   $ pip install -U proofdock-chaos-middleware-python
   ```

1. Register your application to the Chaos Middleware:
   ```python
   import uuid
   
   from pdchaos.middleware.core import chaos
   
   chaos_middleware_config = {
     'CHAOS_MIDDLEWARE_APPLICATION_NAME': 'example-application-name',
     'CHAOS_MIDDLEWARE_APPLICATION_ENV': 'example-environment',
     'CHAOS_MIDDLEWARE_PROOFDOCK_API_TOKEN': 'eyJ0eXAi...05',
     'CHAOS_MIDDLEWARE_APPLICATION_ID': str(uuid.uuid4()),
   }
   config = CustomConfig(chaos_middleware_config)
   chaos.register(config)
   ```

1. Attack each request in your application:
   ```python
   import json
   from pdchaos.middleware import core
   from pdchaos.middleware.core import chaos
   
   headers = request.headers
   attack = json.loads(headers.get(core.HEADER_ATTACK)) if (core.HEADER_ATTACK in headers) else None
   attack_ctx = {core.ATTACK_KEY_ROUTE: request.path}
   chaos.attack(attack, attack_ctx)
   ```

## Extension

Chaos Middleware supports integration with popular web frameworks:
- [Flask](https://github.com/proofdock/chaos-middleware-python/tree/master/src/contrib-flask)
- [Django](https://github.com/proofdock/chaos-middleware-python/tree/master/src/contrib-django)

## References

- [Chaos Middleware documentation][proofdock_middleware_docs]
- [Chaos Middleware repository][proofdock_middleware_repo]
- [Support][proofdock_support]
- [Proofdock website][proofdock]

[proofdock]: https://proofdock.io/
[proofdock_support]: https://github.com/proofdock/chaos-support/
[proofdock_middleware_docs]: https://docs.proofdock.io/chaos/middleware/about/
[proofdock_middleware_repo]: https://github.com/proofdock/chaos-middleware-python