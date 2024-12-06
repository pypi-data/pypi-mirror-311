# persephone: stellar modelling and asteroseismology

[![Documentation Status](https://readthedocs.org/projects/star-persephone/badge/?version=latest)](https://star-persephone.readthedocs.io/en/latest/?badge=latest)

## What is persephone ?

``persephone`` implements a parallelisable Python interface to compute 
[MESA](https://docs.mesastar.org/en/release-r23.05.1/#) stellar
model grids and run [GYRE](https://gyre.readthedocs.io/en/stable/index.html)
on them. It also provides a set of functions to analyse the computed model, 
among which seismic rotational kernels computations.
In the future, grid fitting and inversion methods are planned to be 
implemented in the module.

## Getting started

### Prerequisites

``persephone`` is written in Python3.
The following Python package are necessary to use it :
- numpy
- scipy
- matplotlib
- h5py
- pathos
- [py\_mesa\_reader](https://github.com/wmwolf/py_mesa_reader) 
- [pygyre](https://github.com/rhdtownsend/pygyre)

Note that for py\_mesa\_reader, you will have to clone the repository 
and install it manually from sources with ``pip``.  

A [MESA](https://docs.mesastar.org/en/release-r23.05.1/installation.html) 
and a [GYRE](https://gyre.readthedocs.io/en/stable/user-guide/quick-start.html) 
installations are necessary to use the ``persephone.grids`` submodule.

### Installation

You can install the packaged versions from PyPI by running

``pip install star-persephone``

You can also directly install the code from source. Clone the 
repository and run 

``pip install .``

``persephone`` does not have a conda-forge packaged version yet
but it is planned to provide one in the future.

### Documentation

An online documentation with tutorials and API is available
on [ReadTheDocs](https://star-persephone.readthedocs.io/en/latest/index.html).

## Author

* **Sylvain N. Breton** - Maintainer - (INAF-OACT, Catania, Italy)

## Acknowledging persephone 

If you use ``persephone`` in your work, please provide a link to
the GitLab repository and the documentation.

You should also provide the proper citations and acknowledgements for
[MESA](https://docs.mesastar.org/en/r15140/using_mesa/best_practices.html#citing-mesa) 
and [GYRE](https://gyre.readthedocs.io/en/stable/user-guide/preliminaries.html#citing-gyre).
