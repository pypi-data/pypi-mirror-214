# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bornrule', 'bornrule.sql', 'bornrule.torch']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.5', 'pandas>=1.1.5', 'scikit-learn>=0.24.2', 'scipy>=1.5.4']

setup_kwargs = {
    'name': 'bornrule',
    'version': '0.2.1',
    'description': "Classification with Born's rule",
    'long_description': "This package implements the classifier proposed in the paper [Text Classification with Born's Rule](https://proceedings.neurips.cc/paper_files/paper/2022/hash/c88d0c9bea6230b518ce71268c8e49e0-Abstract-Conference.html). All code is available at the [GitHub repository](https://github.com/eguidotti/bornrule). The documentation is available [here](https://bornrule.eguidotti.com).\n",
    'author': 'Emanuele Guidotti',
    'author_email': 'emanuele.guidotti@unine.ch',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/eguidotti/bornrule',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
