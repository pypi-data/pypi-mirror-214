# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pec_model_master',
 'pec_model_master.pec_pipelines',
 'pec_model_master.pec_pipelines.feature_engineering']

package_data = \
{'': ['*'], 'pec_model_master.pec_pipelines': ['model/*']}

install_requires = \
['catboost==1.1.1',
 'category-encoders>=2.6.1,<3.0.0',
 'numpy>=1.25.0,<2.0.0',
 'pandas>=2.0.2,<3.0.0',
 'requests>=2.31.0,<3.0.0',
 'scikit-learn>=1.2.2,<2.0.0']

setup_kwargs = {
    'name': 'pec-model-master',
    'version': '1.0.0',
    'description': '',
    'long_description': None,
    'author': 'irene.casas',
    'author_email': 'irene.casas@aplazame.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
