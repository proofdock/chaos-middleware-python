## Contribute

If you wish to contribute more functions to this package, you are more than
welcome to do so. Please, fork this project, make your changes following the
usual [PEP 8][pep8] code style, sprinkling with tests and submit a PR for
review.

[pep8]: https://pycodestyle.readthedocs.io/en/latest/

The Proofdock projects require all contributors to sign a
[Developer Certificate of Origin][dco] on each commit they would like to merge
into the master branch of the repository. Please, make sure you can abide by
the rules of the DCO before submitting a PR.

[dco]: https://github.com/probot/dco#how-it-works

### Develop

Developing on this project requires you to set up a development environment:

1. We strongly encourage you to [set up a virtual environment][venv].
2. Install the dev dependencies in your development environment. The dev dependencies instruct pip to install the testing package `pytest`, the code style checker `flake8` and other development-related packages:
   ```console
   $ pip install -r requirements-dev.txt
   ```
3. Deploy the project source in [Development Mode][setuptools_development_mode]. This deployment is done in such a way that changes to the project source are immediately available in your development environment, without needing to run a build or install step after each change:
   ```console
   $ python setup.py develop
   ```
4. In case you want to use the chaos middleware project in your service application in "Development Mode":
   ```
   pip install -e /path/to/chaos-middleware-python/src/core
   pip install -e /path/to/chaos-middleware-python/src/contrib-flask
   pip install -e /path/to/chaos-middleware-python/src/contrib-*
   ```


[venv]: https://docs.python.org/3/library/venv.html
[setuptools_development_mode]: https://setuptools.readthedocs.io/en/latest/setuptools.html#id41


### Verify

* Verify your **tests** are green by running `$ pytest` from the project's root folder
* Validate your **code style and formatting rules** by running `$ flake8 src/` from the project's root folder