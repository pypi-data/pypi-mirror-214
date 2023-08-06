# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mlcvzoo_mmocr']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20',
 'mlcvzoo_base>=5,<6',
 'mlcvzoo_mmdetection>=6,<7',
 'mmocr>=1.0,<2.0',
 'nptyping>=2.0',
 'numpy>=1.19.2,!=1.19.5',
 'opencv-contrib-python>=4.5,!=4.5.5.64,!=4.6.0.66',
 'opencv-python>=4.5,!=4.5.5.64,!=4.6.0.66',
 'related-mltoolbox>=1,<2',
 'torch>=1.9,!=2.0.1',
 'torchvision>=0.10',
 'yaml-config-builder>=8,<9']

extras_require = \
{':platform_machine == "x86_64"': ['pycocotools>=2.0.2']}

setup_kwargs = {
    'name': 'mlcvzoo-mmocr',
    'version': '6.0.0',
    'description': 'MLCVZoo MMOCR Package',
    'long_description': '# MLCVZoo MMOCR\n\nThe MLCVZoo is an SDK for simplifying the usage of various (machine learning driven)\ncomputer vision algorithms. The package **mlcvzoo_mmocr** is the wrapper module for\nthe [mmocr framework](https://github.com/open-mmlab/mmocr).\n\nFurther information about the MLCVZoo can be found [here](../README.md).\n\n## Install\n`\npip install mlcvzoo-mmocr\n`\n\n## Technology stack\n\n- Python\n',
    'author': 'Maximilian Otten',
    'author_email': 'maximilian.otten@iml.fraunhofer.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://git.openlogisticsfoundation.org/silicon-economy/base/ml-toolbox/mlcvzoo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
