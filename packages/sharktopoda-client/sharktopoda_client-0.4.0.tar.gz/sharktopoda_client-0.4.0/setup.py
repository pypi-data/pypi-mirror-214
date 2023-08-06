# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sharktopoda_client']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sharktopoda-client',
    'version': '0.4.0',
    'description': 'Sharktopoda client API, translated to Python',
    'long_description': 'None',
    'author': 'Kevin Barnard',
    'author_email': 'kbarnard@mbari.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
