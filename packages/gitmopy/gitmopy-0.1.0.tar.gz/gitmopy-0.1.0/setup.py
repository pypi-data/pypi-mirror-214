# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gitmopy']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.31,<4.0.0',
 'emoji>=2.5.0,<3.0.0',
 'fuzzysearch>=0.7.3,<0.8.0',
 'inquirerpy>=0.3.4,<0.4.0',
 'pyyaml>=6.0,<7.0',
 'typer[all]>=0.9.0,<0.10.0']

entry_points = \
{'console_scripts': ['gitmopy = gitmopy.cli:app']}

setup_kwargs = {
    'name': 'gitmopy',
    'version': '0.1.0',
    'description': 'A python command-line for gitmoji',
    'long_description': '# gitmopy',
    'author': 'vict0rsch',
    'author_email': 'vsch@pm.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
