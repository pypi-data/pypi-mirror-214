# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tsdf']

package_data = \
{'': ['*']}

install_requires = \
['flatten-json>=0.1.13,<0.2.0',
 'mkdocs-jupyter>=0.22.0,<0.23.0',
 'mkdocs>=1.4.2,<2.0.0',
 'mypy>=1.0.1,<2.0.0',
 'numpy>=1.24.1,<2.0.0']

setup_kwargs = {
    'name': 'tsdf',
    'version': '0.3.0',
    'description': 'A Python library that provides methods for encoding and decoding TSDF (Time Series Data Format) data, which allows you to easily create, manipulate and serialize TSDF files in your Python code.',
    'long_description': '\n![Python package](https://github.com/biomarkersparkinson/tsdf/workflows/Python%20package/badge.svg)\n[![PyPI](https://img.shields.io/pypi/v/tsdf.svg)](https://pypi.python.org/pypi/tsdf/)\n[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7867900.svg)](https://doi.org/10.5281/zenodo.7867900)\n\n# tsdf\n\nA package to load [TSDF data](https://arxiv.org/abs/2211.11294) into Python\n\n## Installation\n\n### Using `pip`\n\nThe package is available in PyPi. It can be installed using:\n\n```bash\n$ pip install tsdf\n```\n\n## Usage\n\nSee our [extended tutorials](https://biomarkersparkinson.github.io/tsdf/).\n\n## Development\n\n### Running tests\n\n```bash\npoetry install\npoetry run pytest\n```\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\nThis package was created by Pablo Rodríguez, Peter Kok and Vedran Kasalica. It is licensed under the terms of the Apache License 2.0 license.\n\n## Credits\n\n- The [TSDF data format](https://arxiv.org/abs/2211.11294) was created by Kasper Claes, Valentina Ticcinelli, Reham Badawy, Yordan P. Raykov, Luc J.W. Evers, Max A. Little.\n- This package was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Peter Kok',
    'author_email': 'p.kok@esciencecenter.nl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/biomarkersParkinson/tsdf',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
