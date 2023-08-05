# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['webint_ai', 'webint_ai.templates']

package_data = \
{'': ['*']}

install_requires = \
['markdown>=3.4.1,<4.0.0', 'openai>=0.27.2,<0.28.0', 'webint>=0.0']

entry_points = \
{'webapps': ['ai = webint_ai:app']}

setup_kwargs = {
    'name': 'webint-ai',
    'version': '0.0.4',
    'description': 'interface artificial intelligence',
    'long_description': 'None',
    'author': 'Angelo Gladding',
    'author_email': 'angelo@ragt.ag',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
