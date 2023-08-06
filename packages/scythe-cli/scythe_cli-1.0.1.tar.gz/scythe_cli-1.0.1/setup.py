# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scythe_cli',
 'scythe_cli.application',
 'scythe_cli.ui',
 'scythe_cli.ui.widgets']

package_data = \
{'': ['*'], 'scythe_cli.ui': ['styles/*']}

install_requires = \
['arc-cli>=8.4.0,<9.0.0',
 'httpx>=0.24.0,<0.25.0',
 'keyring>=23.13.1,<24.0.0',
 'msgspec>=0.15.1,<0.16.0',
 'requests>=2.25.1,<3.0.0',
 'textual>=0.27.0,<0.28.0',
 'xdg>=5.1.1,<6.0.0']

entry_points = \
{'console_scripts': ['scythe = scythe_cli.application.application:scythe']}

setup_kwargs = {
    'name': 'scythe-cli',
    'version': '1.0.1',
    'description': 'A Harvest is always better with a good tool',
    'long_description': '',
    'author': 'Sean Collings',
    'author_email': 'seanrcollings@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/seanrcollings/scythe',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
