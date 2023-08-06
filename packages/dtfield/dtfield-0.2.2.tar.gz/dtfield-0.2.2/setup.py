# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dtfield', 'dtfield.parse']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'Unidecode>=1.3.6,<2.0.0',
 'anyio>=3.7.0,<4.0.0',
 'dtbase>=0.0.4,<0.0.5',
 'itsdangerous>=2.1.2,<3.0.0',
 'python-multipart>=0.0.6,<0.0.7',
 'typing-extensions>=4.6.3,<5.0.0',
 'uvicorn>=0.22.0,<0.23.0']

setup_kwargs = {
    'name': 'dtfield',
    'version': '0.2.2',
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
