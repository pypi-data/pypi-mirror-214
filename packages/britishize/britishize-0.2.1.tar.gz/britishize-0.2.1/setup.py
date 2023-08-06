# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['britishize']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.9.0,<0.10.0']

entry_points = \
{'console_scripts': ['brit = britishize.britishize:main']}

setup_kwargs = {
    'name': 'britishize',
    'version': '0.2.1',
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
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
