# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ricomodels',
 'ricomodels.backbones',
 'ricomodels.backbones.mobilenetv2',
 'ricomodels.deeplabv3_plus',
 'ricomodels.seq2seq',
 'ricomodels.tests',
 'ricomodels.unet',
 'ricomodels.utils']

package_data = \
{'': ['*'], 'ricomodels': ['weights/*']}

install_requires = \
['albumentations>=1.4.18,<2.0.0',
 'matplotlib<4.0.0',
 'pycocotools>=2.0.7,<3.0.0',
 'pytest>=8.3.3,<9.0.0',
 'torch>=2.2.0,<3.0.0',
 'torchvision>=0.20.1,<0.21.0',
 'tqdm>=4.66.5,<5.0.0',
 'wandb>=0.18.3,<0.19.0']

setup_kwargs = {
    'name': 'ricomodels',
    'version': '0.2.5',
    'description': "This is Rico's Neural Network models",
    'long_description': "## RicoModels                                                             \n\nThis is a collection of Neural Network Models that I've tried during my Deep Learning Journey.\n\n### ResNet-20\n\nTODO\n\n### UNet",
    'author': 'Rico Jia',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
