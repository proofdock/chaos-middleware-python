# Copyright 2020, Proofdock Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Pluggable chaos engineering application for Django projects"""

from setuptools import setup, find_namespace_packages

exec(open('pdchaos/application/version.py').read())

setup(
    name='proofdock-chaos-middleware-django',
    version=__version__,  # noqa
    author='Proofdock Authors',
    author_email='support@proofdock.io',
    classifiers=[
        'Intended Audience :: Developers',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description='Practice chaos engineering with Python Django projects',
    include_package_data=True,
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    extras_require={},
    license='Apache-2.0',
    python_requires='>=3.5.*',
    packages=find_namespace_packages(include='pdchaos.*'),
    install_requires=[
        'django',
        'proofdock-chaos-middleware-python',
    ],
    url='https://github.com/proofdock/chaos-middleware-python/tree/master/src/contrib-django',
)
