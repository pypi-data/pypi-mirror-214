# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['django_handleref', 'django_handleref.rest']

package_data = \
{'': ['*'],
 'django_handleref': ['templates/handleref/*',
                      'templates/handleref/grappelli/*']}

setup_kwargs = {
    'name': 'django-handleref',
    'version': '2.0.0',
    'description': 'django object tracking',
    'long_description': '# django-handleref\n\n[![PyPI](https://img.shields.io/pypi/v/django-handleref.svg?maxAge=3600)](https://pypi.python.org/pypi/django-handleref)\n[![PyPI](https://img.shields.io/pypi/pyversions/django-handleref.svg?maxAge=600)](https://pypi.python.org/pypi/django-handleref)\n[![Tests](https://github.com/20c/django-handleref/workflows/tests/badge.svg)](https://github.com/20c/django-handleref)\n[![Codecov](https://img.shields.io/codecov/c/github/20c/django-handleref/master.svg?maxAge=3600)](https://codecov.io/github/20c/django-handleref)\n\nTrack when an object was created or changed and allow querying based on time and versioning (w/ `django-reversion` support)\n\n### License\n\nCopyright 2015-2023 20C, LLC\n\nLicensed under the Apache License, Version 2.0 (the "License");\nyou may not use this software except in compliance with the License.\nYou may obtain a copy of the License at\n\n   http://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing, software\ndistributed under the License is distributed on an "AS IS" BASIS,\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\nSee the License for the specific language governing permissions and\nlimitations under the License.\n',
    'author': '20C',
    'author_email': 'code@20c.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/20c/django-handleref',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
