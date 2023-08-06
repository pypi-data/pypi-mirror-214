# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['invokees', 'invokees.tasks', 'invokees.tools']

package_data = \
{'': ['*']}

install_requires = \
['black>=23.1.0,<24.0.0',
 'coverage>=7.1.0,<8.0.0',
 'invoke>=2.0.0,<3.0.0',
 'isort>=5.12.0,<6.0.0',
 'mypy>=1.0.1,<2.0.0',
 'pre-commit>=3.1.1,<4.0.0',
 'prysk[pytest-plugin]>=0.13.1,<0.14.0',
 'pytest-cov>=4.0.0,<5.0.0',
 'pytest-xdist>=3.2.0,<4.0.0',
 'pytest>=7.2.1,<8.0.0',
 'rich>=13.3.1,<14.0.0',
 'ruff>=0.0.247',
 'tomlkit>=0.11.6,<0.12.0',
 'types-docutils>=0.19.1.6',
 'types-invoke>=2.0.0.5,<3.0.0.0',
 'types-pygments>=2.14.0.5,<3.0.0.0',
 'types-setuptools>=67.4.0.3,<68.0.0.0']

setup_kwargs = {
    'name': 'invokees',
    'version': '0.3.0',
    'description': 'Common python project tasks',
    'long_description': '',
    'author': 'Nicola Coretti',
    'author_email': 'nico.coretti@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
