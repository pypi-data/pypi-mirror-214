# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['django_grainy', 'django_grainy.migrations']

package_data = \
{'': ['*'],
 'django_grainy': ['static/grainy/*',
                   'templates/django_grainy/forms/widgets/*']}

install_requires = \
['Django>=3.2,<5',
 'black>=22.3.0,<23.0.0',
 'djangorestframework>=3.0,<4.0',
 'grainy>=1.7.0,<2',
 'six>=1.11.0,<=2.0.0']

entry_points = \
{'markdown.extensions': ['pymdgen = pymdgen.md:Extension']}

setup_kwargs = {
    'name': 'django-grainy',
    'version': '2.0.0',
    'description': 'granular permissions for django',
    'long_description': '# django-grainy\n\n[![PyPI](https://img.shields.io/pypi/v/django-grainy.svg?maxAge=60)](https://pypi.python.org/pypi/django-grainy)\n[![PyPI](https://img.shields.io/pypi/pyversions/django-grainy.svg?maxAge=600)](https://pypi.python.org/pypi/django-grainy)\n[![Codecov](https://img.shields.io/codecov/c/github/20c/django-grainy/master.svg?maxAge=60)](https://codecov.io/github/20c/django-grainy)\n\nGranular permissions for django\n\n## Supported Django Versions\n\n- Django 3.2\n- Django 4.0\n- Django 4.2\n\n## Documentation\n\nhttps://20c.github.io/django-grainy\n\n## License\n\nCopyright 2019-2023 20C, LLC\n\nLicensed under the Apache License, Version 2.0 (the "License");\nyou may not use this softare except in compliance with the License.\nYou may obtain a copy of the License at\n\n   http://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing, software\ndistributed under the License is distributed on an "AS IS" BASIS,\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\nSee the License for the specific language governing permissions and\nlimitations under the License.\n',
    'author': '20C',
    'author_email': 'code@20c.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/20c/django-grainy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
