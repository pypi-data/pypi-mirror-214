# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['langconv', 'langconv.language']

package_data = \
{'': ['*'], 'langconv': ['data/zh/*']}

install_requires = \
['attrs>=23.1.0,<24.0.0', 'iso639-lang>=2.1.0,<3.0.0']

setup_kwargs = {
    'name': 'langconv',
    'version': '0.2.0',
    'description': '',
    'long_description': '',
    'author': 'Dianliang233',
    'author_email': 'dianliang233@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
