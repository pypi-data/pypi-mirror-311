import pygyre as pg
import numpy as np
import matplotlib.pyplot as plt
import persephone
from persephone.kernels import *

"""
A collection of function to plot
GYRE outputs.
"""

def plot_displacement (filename=None, d=None, yscale='linear',
                       figsize=(10,4), show_title=True) :
    """
    Plot ``xi_r`` and ``xi_h`` real part.

    Parameters
    ----------
    filename :
        filename
    yscale :
        yscale
    figsize :
        figsize

    Returns
    -------
    ``matplotlib.figure``
      Figure.
    """
    if d is None and filename is None : 
      raise Exception ("You must provide at least data structure d or filename")
    if d is None :
      d = pg.read_output(filename)
    fig, ax = plt.subplots (1, 1, figsize=figsize)
    if show_title :
      fig.suptitle (filename)
    ax.axhline (0, ls='--', color='darkgrey')
    ax.plot(d['x'], d['xi_r'].real, color='blue', lw=2,
        label=r'$\xi_r$')
    ax.plot(d['x'], d['xi_h'].real, color='darkorange', lw=2,
        label=r'$\xi_h$')
    ax.set_xlabel(r'$r/R_\star$')
    ax.legend ()
    ax.set_yscale (yscale)
    return fig

def plot_modulus_displacement (filename=None, d=None, 
                               l=1, yscale='linear',
                               figsize=(10,4), show_title=True) :
    """
    Plot ``xi_r`` and ``xi_h`` squared modulus.

    Parameters
    ----------
    filename :
        filename
    yscale :
        yscale
    figsize :
        figsize

    Returns
    -------
    ``matplotlib.figure``
      Figure.

    """
    if d is None and filename is None : 
      raise Exception ("You must provide at least data structure d or filename")
    if d is None :
      d = pg.read_output(filename)
    try : 
      l = d.meta["l"]
    except KeyError :
      pass
    fig, ax = plt.subplots (1, 1, figsize=figsize)
    if show_title :
      fig.suptitle (filename)
    ax.axhline (0, ls='--', color='darkgrey')
    ax.plot(d['x'], np.abs (d['xi_r'])**2 + l*(l*1)*np.abs(d['xi_h'])**2, color='blue', lw=2,
        label=r'$|\xi_r|^2 + \ell (\ell + 1) |\xi_h|^2$')
    ax.set_xlabel(r'$r/R_\star$')
    ax.legend ()
    ax.set_yscale (yscale)
    return fig

def plot_rotation_kernel_1d (filename=None, d=None, l=1,
                             show_title=True, ax=None,
                             legend=True, color='blue', ls='-',
                             label='$K_{n,\ell}$', ncols=1, 
                             normalise_max=False) :
    '''
    Plot 1d shellular rotation kernel for a given mode.
    '''
    if d is None and filename is None : 
      raise Exception ("You must provide at least data structure d or filename")
    if d is None :
      d = pg.read_output(filename)
    try : 
      l = d.meta["l"]
    except KeyError :
      pass
    _, K_nl = compute_shellular_kernel (d['x'], d['rho'], 
                                        d['xi_r'], d['xi_h'], l=l)
    
    if ax is None :
      fig, ax = plt.subplots (1, 1, figsize=(10,4))
    else :
      fig = ax.get_figure ()
    if show_title :
      fig.suptitle (filename)
    if normalise_max :
      norm = np.amax (K_nl)
    else :
      norm = 1
    ax.plot(d['x'], K_nl/norm, color=color, lw=2,
        label=label, ls=ls)
    ax.set_xlabel(r'$r/R_\star$')
    if legend :
      ax.legend (ncols=ncols)
    return fig

def plot_kinetic_energy_density (filename=None, d=None, rstar=None, ax=None, 
                                 figsize=(10,4), show_title=True, label='KED',
                                 normalise_max=False, normalise_integral=True,
                                 ncols=1, color='red', legend=True, ls='-', lw=2,
                                 zorder=None) :
    '''
    Plot kinetic energy density for a given mode.
    '''
    if d is None and filename is None : 
      raise Exception ("You must provide at least data structure d or filename")
    if d is None :
      d = pg.read_output(filename)
    if rstar is None :
      rstar = d.meta["R_star"]*1e-2
    ked = persephone.compute_kinetic_energy_density (d['x']*rstar, d['rho']*1e-3, 
                                          d['xi_r']*1e-2, d['xi_h']*1e-2,
                                          l=d.meta["l"], normalise_max=normalise_max,
                                          normalise_integral=normalise_integral)
    if ax is None :
      fig, ax = plt.subplots (1, 1, figsize=(10,4))
    else :
      fig = ax.get_figure ()
    if show_title :
      fig.suptitle (filename)
    ax.plot(d['x'], ked, color=color, lw=lw, ls=ls,
        label=label, zorder=zorder)
    ax.set_xlabel(r'$r/R_\star$')
    if legend :
      ax.legend (ncols=ncols)
    return fig

def get_brunt_vaisala (filename=None, d=None, rstar=None) :
  '''
  Compute Brunt-Vaisala frequency.
  '''
  if d is None and filename is None : 
    raise Exception ("You must provide at least data structure d or filename")
  if d is None :
    d = pg.read_output(filename)
  if rstar is None :
    rstar = d.meta["R_star"]*1e-2
  N2 = persephone.compute_N2 (d['x']*rstar, d["As"], d["M_r"]*1e-3)
  # Clean the nan point that can appear at zero-radius
  N2[np.isnan(N2)] = 0
  # Remove negative values to plot the square of positive regions
  N2[N2<0] = 0
  N = np.sqrt (N2) 
  return d['x'], N

def plot_brunt_vaisala (filename=None, d=None, rstar=None,
                        figsize=(6,4), ylim=(0, 500)) :
  '''
  Compute and plot Brunt-Vaisala frequency.
  '''
  x, N = get_brunt_vaisala (filename=filename, d=d, rstar=rstar)
  fig, ax = plt.subplots (1, 1, figsize=figsize)
  ax.plot (x, N*1e6/(2*np.pi), color='blue', lw=2)
  ax.set_xlabel(r'$r/R_\star$')
  ax.set_ylabel(r'$N$ ($\mu$Hz)')

  ax.set_ylim (ylim)
  return fig
