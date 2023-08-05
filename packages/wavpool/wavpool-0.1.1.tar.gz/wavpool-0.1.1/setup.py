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
    'version': '0.1.1',
    'description': 'A network block with built in spacial and scale decomposition.',
    'long_description': "\n\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n[![PyPI version](https://img.shields.io/pypi/v/wavpool)](https://pypi.org/project/wavpool/)\n[![arXiv](https://img.shields.io/badge/arXiv-1234.56789-b31b1b.svg)](https://arxiv.org/abs/1234.56789)\n\n# WavPool\n\nA network block with built in spacial and scale decomposition.\n\n\n>    Modern deep neural networks comprise many operational layers, such as dense or convolutional layers, which are often collected into blocks. In this work, we introduce a new, wavelet-transform-based network architecture that we call the multi-resolution perceptron: by adding a pooling layer, we create a new network block, the WavPool. The first step of the multi-resolution perceptron is transforming the data into its multi-resolution decomposition form by convolving the input data with filters of fixed coefficients but increasing size. Following image processing techniques, we are able to make scale and spatial information simultaneously accessible to the network without increasing the size of the data vector. WavPool outperforms a similar multilayer perceptron while using fewer parameters, and outperforms a comparable convolutional neural network by over 10% on accuracy on CIFAR-10.\n\n\nThis codebase contains the experimental work supporting the paper. It is to be used additional material for replication.\n\n## Installation\n\nOur project can be installed with pip [from pypi](https://pypi.org/project/wavpool/) using: \n\n```\npip install wavpool\n```\n\nThis project is build with python `poetry`. And is our perfered method to install from source.\n\nCommands are as follows:\n\n```\npip install poetry\npoetry shell\npoetry init\npoetry install\n```\n\nTo install all the dependencies required for this project.\n\n\nWe also supply distribution files (found in \\dist), or you may use the provided pyproject.toml to install with your method of choice.\n\n## Contents\n\n### Data Generators\nThe pytorch data generator objects for the experiments done in this paper.\nWrapped to work with the training framework, but functionally unmodified.\nWe include CIFAR-10 (`cifar_generator.py`), Fashion MNIST (`fashion_mnist_generator.py`), and MNIST (`mnist_generator.py`).\n\n### Training\nTraining loops used in the experiments.\n\n`finetune_networks.py` generates a set of parameters optimial for a network/task combination.\n\n`train_model.py` Executes the training loop for a network/task/parameter combination.\n\n### Models\n\n`wavpool.py` Our implimentation of the novel WavPool block\n\n`vanillaCNN.py` Standard two layer CNN containing 2D Convolutions, batch norms, and a dense output\n\n`vanillaMLP.py` Standard two hidden layer MLP\n\n`wavelet_layer.py` The `MicroWav` MLR analysis layer\n\n`wavMLP.py` Single `MicroWav` layer network with an additional dense layer and output. Not included in the paper.\n\n\n### Notebooks\n\nVisualizations of experiments with plotting code for plots included in the paper, and code to produce weights.\n\n### `run_experiments.py`\n\nTakes a configuration and trains an model.\nCurrent execution shows the optimization and subsquentical training and testing for a WavPool over CIFAR-10, Fashion MNIST and MNIST.\n\n### Acknowledgement \n\nWe acknowledge the Deep Skies Lab as a community of multi-domain experts and collaborators who've facilitated an environment of open discussion, idea-generation, and collaboration. This community was important for the development of this project.\nWe thank Aleksandra Ciprijanovic, Andrew Hearin, and Shubhendu Trivedi for comments on the manuscript.\nThis manuscript has been authored by Fermi Research Alliance, LLC under Contract No.~DE-AC02-07CH11359 with the U.S.~Department of Energy, Office of Science, Office of High Energy Physics.\n\n\n`FERMILAB-CONF-23-278-CSAID`\n\n### Citation \n",
    'author': 'M. Voetberg',
    'author_email': 'maggiev@fnal.gov',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/deepskies/DeepWavNN',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
