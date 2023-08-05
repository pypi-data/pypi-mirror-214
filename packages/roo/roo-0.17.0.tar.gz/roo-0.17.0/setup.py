# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['roo',
 'roo.caches',
 'roo.cli',
 'roo.cli.add',
 'roo.cli.cache',
 'roo.cli.environment',
 'roo.cli.export',
 'roo.cli.init',
 'roo.cli.install',
 'roo.cli.lock',
 'roo.cli.package',
 'roo.cli.rswitch',
 'roo.cli.run',
 'roo.deptree',
 'roo.exporters',
 'roo.exporters.lock',
 'roo.files',
 'roo.parsers',
 'roo.semver',
 'roo.sources']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.13,<4.0.0',
 'atomicwrites>=1.4,<2.0',
 'beautifulsoup4>=4.8.2,<5.0.0',
 'click>=7.0,<8.0',
 'packaging>=20.1,<21.0',
 'requests>=2.22.0,<3.0.0',
 'rich>=11.0.0,<12.0.0',
 'toml>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['roo = roo.cli.__main__:main']}

setup_kwargs = {
    'name': 'roo',
    'version': '0.17.0',
    'description': 'A package manager to handle R environments',
    'long_description': "# Roo - manages environments and dependencies in R\n\n[![Maturity Level](https://img.shields.io/badge/Maturity%20Level-Under%20Development-orange)](https://img.shields.io/badge/Maturity%20Level-Under%20Development-orange)\n\n# Description\n\nRoo is a python program that handles R dependencies and R environments,\nensuring environment reproducibility that satisfy dependency constraints.\nIf you are familiar with python poetry or pip it aims at being the same.\nWhile apparently similar to packrat or renv, Roo is way more powerful.\n\nAs a data scientist using e.g. RStudio you are unlikely to benefit from Roo,\nbut if you need to create production R code, it's a much safer choice to\ndefine a consistent and reliable environment of dependencies. It also provides\nfunctionalities that helps in maintaining different environments at the same time.\n\n# Installation\n\nRoo is written in python and requires python 3.8 or above.\nIt runs on any platform, and it can be installed from pypi with:\n\n    pip install roo\n\nDependencies will be installed automatically.\n\n# Documentation\n\n- [Rationale](docs/rationale.md)\n- [Basic Usage](docs/usage.md)\n- [Advanced Usage](docs/advanced.md)\n- [Troubleshooting](docs/troubleshooting.md)\n",
    'author': 'Stefano Borini',
    'author_email': 'stefano.borini@astrazeneca.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AstraZeneca/roo',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
