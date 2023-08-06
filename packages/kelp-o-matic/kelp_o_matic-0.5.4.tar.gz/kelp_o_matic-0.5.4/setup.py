# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kelp_o_matic', 'kelp_o_matic.data', 'kelp_o_matic.geotiff_io']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.24.2,<2.0.0',
 'rasterio>=1.3.7,<2.0.0',
 'torch>=2.0.0,!=2.0.1',
 'torchvision>=0.15.0,<0.16.0',
 'tqdm>=4.65.0,<5.0.0',
 'typer>=0.9.0,<0.10.0']

entry_points = \
{'console_scripts': ['kom = kelp_o_matic.cli:cli']}

setup_kwargs = {
    'name': 'kelp-o-matic',
    'version': '0.5.4',
    'description': 'Hakai Segment Tool for GeoTiff RPAS Imagery',
    'long_description': '<div align="center" style="overflow: hidden; display: flex; justify-content:center; gap:10px;">\n<a href="https://github.com/HakaiInstitute/kelp-o-matic/actions/workflows/unit-test.yml">\n    <img alt="🧪 Unit Tests" src="https://github.com/HakaiInstitute/kelp-o-matic/actions/workflows/unit-test.yml/badge.svg" height="20px" />\n</a>\n\n<a href="https://github.com/HakaiInstitute/kelp-o-matic/blob/main/LICENSE.txt">\n    <img alt="License" src="https://anaconda.org/conda-forge/kelp-o-matic/badges/license.svg" height="20px" />\n</a>\n\n<a href="https://anaconda.org/conda-forge/kelp-o-matic">\n    <img alt="Version" src="https://anaconda.org/conda-forge/kelp-o-matic/badges/version.svg" height="20px" />\n</a>\n\n<a href="https://zenodo.org/badge/latestdoi/462897183">\n    <img alt="DOI" src="https://zenodo.org/badge/462897183.svg" height="20px" />\n</a>\n</div>\n\n<p align="center">\n    <img src="./docs/images/kelp_o_matic_smaller.gif" alt="Kelp-O-Matic" />\n</p>\n\n<p align="center">\n    <i>Kelp Segmentation Tools for Aerial Imagery</i>\n</p>\n\n<h1 align="center">\n    <a href="https://kelp-o-matic.readthedocs.io">&#9758; Read the Docs &#9756;</a>\n</h1>\n',
    'author': 'Taylor Denouden',
    'author_email': 'taylor.denouden@hakai.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
