from importlib.metadata import version

__version__ = version ('star-persephone') 

import persephone.kernels

import persephone.kernels.rotation

import persephone.grids

import persephone.grids.templates

from .eigenfunctions import *

from .plot_gyre import *

global Rsun
global Msun
global gravity_constant

Rsun = 6.9634e8
Msun = 1.9847e30
gravity_constant = 6.67428e-11
