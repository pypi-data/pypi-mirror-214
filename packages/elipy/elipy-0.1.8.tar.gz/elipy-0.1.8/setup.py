# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['elipy', 'elipy.core']

package_data = \
{'': ['*']}

install_requires = \
['mpi4py>=3.1.4,<4.0.0',
 'netCDF4>=1.5.7,<2.0.0',
 'numba>=0.56.4,<0.57.0',
 'numpy>=1.23.5,<2.0.0',
 'scipy>=1.9.3,<2.0.0']

setup_kwargs = {
    'name': 'elipy',
    'version': '0.1.8',
    'description': 'Post-processing tool for Abinit >= 9.8.1 aiming to calculate energy-resolved Eliashberg function',
    'long_description': "# Elipy\n\nPost-processing tool for ABINIT >= 9.8.1 aiming for calculation of energy-resolved Eliashberg function\n\n## Description\n\nSince version 9.8.1 ABINIT provides easy-to-use methods within EPH package for the calculation of electron-phonon matrix elements on rectangular k- and q-point grids (optdriver 7, eph_task 11). The present package is a tool for calculation of electron-energy-resolved Eliashberg function on arbitrary electron and phonon grids. \n\n$$\n\\alpha^2 F(\\epsilon,\\epsilon',\\omega)=\\frac{1}{N_\\mathbf{k}N_\\mathbf{q}}\\sum_{\\mathbf{k}\\mathbf{q}mn\\nu}\\left|g_{mn\\nu}(\\mathbf{k},\\mathbf{q})\\right|^2\\delta(\\epsilon_{\\mathbf{k}n}-\\epsilon)\\delta(\\epsilon_{\\mathbf{k+q}m}-\\epsilon')\\delta(\\omega_{\\mathbf{q}\\nu}-\\omega)\n$$\n\nThe above-written definition does not include electron density of states at Fermi level. One needs to divide $\\alpha^2 F$ over $N_F$ to get physically meaningful results. \n\nProject uses mpi4py for many-core parallelization and Numba for acceleration of procedures dealing with iteration over numpy arrays.\n\nElipy is insipired by [ElectronPhononCoupling](https://github.com/GkAntonius/ElectronPhononCoupling) and [Abipy](https://github.com/abinit/abipy) projects, and uses some of their utility functions. Apologies for code copy-pasting, it allows to keep dependency list as short as possible.  \n\n### Limitations\n\n* only Gaussian smearing summation for delta functions\n* no account for spin of electron states\n\n## Getting Started\n\n### Dependencies\n\n* Numpy\n* Scipy\n* netCDF4\n* Numba\n* mpi4py\n\nThe actual versions of required packages are stored in pyproject.toml file.\n\n### Installation\n\n```\npip install elipy\n```\nALternatively, one can build code with [Poetry](https://python-poetry.org) package manager:\n\n```\ngit clone https://github.com/Radioteddy/elipy.git\ncd elipy\npoetry install\n```\n### Executing program\n\n* Use mpirun, mpiexec, srun,... for program execution\n```\nmpiexec -n X python filename.py > out 2> err\n```\n\n## Authors\n\n[Fedor Akhmetov](https://github.com/Radioteddy)\n\n## Version History\n\n* 0.1.8\n    * collective communication for matrix elements replaced by p2p one\n* 0.1.7\n    * electron and phonon eigenvalues are taken from GSTORE\n* 0.1.6\n    * minor bugfixes and improvements\n* 0.1.5\n    * Working Release\n* 0.1.0\n    * Initial Release\n\n## Acknowledgments\n* [ElectronPhononCoupling](https://github.com/GkAntonius/ElectronPhononCoupling)\n* [Abipy](https://github.com/abinit/abipy)\n",
    'author': 'Fedor Akhmetov',
    'author_email': 'f.akhmetov@utwente.nl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
