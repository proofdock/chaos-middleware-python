# Copyright 2019, Proofdock Authors
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
from setuptools import find_packages, setup

setup(
    name='proofdock-chaos-middleware-flask',
    version='0.1.0.dev3',  # noqa
    author='Proofdock Authors',
    author_email='support@proofdock.io',
    classifiers=[
        'Intended Audience :: Developers',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description='A chaos engineering framework for Flask applications',
    include_package_data=True,
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    install_requires=[
        'flask >= 0.12.3, < 2.0.0',
        'proofdock-chaos-middleware-python >= 0.1.dev0, < 1.0.0',
    ],
    extras_require={},
    license='Apache-2.0',
    packages=find_packages(exclude=('examples', 'tests',)),
    python_requires='>=3.5.*',
    namespace_packages=[],
    url='https://github.com/proofdock/chaos-middleware-python/tree/master/contrib/pdchaos-ext-flask',  # noqa: E501
    zip_safe=False,
)
