# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['britishize']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'britishize',
    'version': '0.1.0',
    'description': 'Write poorer english',
    'long_description': 'Write proper english\n',
    'author': 'Antonio Feregrino',
    'author_email': 'antonio.feregrino@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
