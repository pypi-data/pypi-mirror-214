# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wavpool',
 'wavpool.data_generators',
 'wavpool.models',
 'wavpool.training',
 'wavpool.utils']

package_data = \
{'': ['*'], 'wavpool': ['.pytest_cache/*', '.pytest_cache/v/cache/*']}

install_requires = \
['PyWavelets>=1.4.1,<2.0.0',
 'bayesian-optimization>=1.4.2,<2.0.0',
 'jupyter>=1.0.0,<2.0.0',
 'kymatio>=0.3.0,<0.4.0',
 'numpy>=1.24.2,<2.0.0',
 'pandas>=1.5.3,<2.0.0',
 'torch>=1.13.1,<2.0.0',
 'torcheval>=0.0.6,<0.0.7',
 'torchvision>=0.14.1,<0.15.0']

setup_kwargs = {
    'name': 'wavpool',
    'version': '0.1.0',
    'description': 'A network block with built in spacial and scale decomposition.',
    'long_description': 'None',
    'author': 'M. Voetberg',
    'author_email': 'maggiev@fnal.gov',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
