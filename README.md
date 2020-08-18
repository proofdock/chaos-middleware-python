# Proofdock chaos middleware for Python

![CI](https://github.com/proofdock/chaos-middleware-python/workflows/CI/badge.svg?branch=master)
[![Python versions](https://img.shields.io/pypi/pyversions/proofdock-chaos-middleware-python.svg)](https://www.python.org/)

Practice chaos engineering with Python applications. This project is a collection of features to inject failures at the application level. Various Python frameworks are supported.

## Project description

This project is part of Proofdock's [**Chaos Platform**][proofdock] that supports you to **attack your service application with turbulent and unexpected conditions** in order to improve its resiliency.


## Install

This package requires Python 3.5+

The chaos middleware project supports various Python web frameworks. We call those **contribution**'s.

* **Reveal all available contributions** under the `src/contrib-*` directories in our [GitHub repository][proofdock_gh_middleware].
* **Exemplified at [Flask][flask]**, installation is that easy:
  ```
  $ pip install -U proofdock-chaos-middleware-flask
  ```

* You miss your framework? Contribute *or* let us know.

* You can't contribute? Install the core package and integrate with your application.
   ```
   $ pip install -U proofdock-chaos-middleware-python
   ```

## Usage

Detailed usage instructions are available at the [Proofdock documentation pages][proofdock_docs_middleware].

## Configuration

* The chaos middleware expects some configuration variables. Those variables ensure that your service application reacts properly on attacks.

* Each contribution has its own way of declaring the configuration values. Respectively head to the contribution packages and read the configuration instructions. You will find those under `src/contrib-*/README.md` in our [GitHub repository][proofdock_gh_middleware] .


## Contact and support

For more information visit our official [website][proofdock] or [documentation][proofdock_docs]. Feel free to ask for support for this package on [GitHub][proofdock_gh_support].


[flask]: https://flask.palletsprojects.com/
[proofdock]: https://proofdock.io/
[proofdock_docs]: https://docs.proofdock.io/
[proofdock_docs_control_panel]: https://docs.proofdock.io/chaos/devops/control-panel
[proofdock_docs_middleware]: https://docs.proofdock.io/chaos/middleware
[proofdock_gh_support]: https://github.com/proofdock/chaos-support/
[proofdock_gh_middleware]: https://github.com/proofdock/chaos-middleware-python