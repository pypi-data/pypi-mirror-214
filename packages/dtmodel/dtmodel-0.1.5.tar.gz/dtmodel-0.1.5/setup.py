# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dtmodel',
 'dtmodel.bases',
 'dtmodel.dtfield',
 'dtmodel.dtfield.parse',
 'dtmodel.enums',
 'dtmodel.models']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'Unidecode>=1.3.6,<2.0.0',
 'anyio>=3.7.0,<4.0.0',
 'bcrypt>=4.0.1,<5.0.0',
 'dtbase>=0.0.5,<0.0.6',
 'itsdangerous>=2.1.2,<3.0.0',
 'python-multipart>=0.0.6,<0.0.7',
 'starlette>=0.28.0,<0.29.0',
 'uvicorn>=0.22.0,<0.23.0']

setup_kwargs = {
    'name': 'dtmodel',
    'version': '0.1.5',
    'description': '',
    'long_description': None,
    'author': 'Daniel Arantes',
    'author_email': 'arantesdv@me.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
