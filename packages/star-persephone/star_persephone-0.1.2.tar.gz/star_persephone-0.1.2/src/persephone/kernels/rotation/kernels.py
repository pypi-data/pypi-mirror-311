import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import trapz
from scipy.special import lpmv, factorial

def broadcast_on_theta (a, theta_res) :
  '''
  Broadcast radial array to a second latitudinal 
  dimension.
  '''
  broadcasted = np.broadcast_to (a.reshape (*a.shape, -1), 
                                    (*a.shape, theta_res))
  return broadcasted

def create_grids (r, rho, xi_r, xi_h, theta_res=90,
                  theta_0=0, theta_1=180) :
  '''
  Create ``(r, theta)`` grid necessary for the computation
  and expand dimension of eigenfunctions and profiles onto it. 
  '''
  if theta_0==0 :
    theta_0 += 1e-9
  if theta_1==180 :
    theta_1 -= 1e-9
  theta = np.linspace (theta_0*np.pi/180, theta_1*np.pi/180, theta_res)
  r, theta = np.meshgrid (r, theta, indexing='ij')
  mu = np.cos (theta)
  sin_theta = np.sin (theta)
  rho = broadcast_on_theta (rho, theta_res)
  xi_r = broadcast_on_theta (xi_r, theta_res)
  xi_h = broadcast_on_theta (xi_h, theta_res)
  
  return r, theta, mu, sin_theta, rho, xi_r, xi_h

def compute_numerator_general_case (r, rho, theta, xi_r, xi_h, l=1,
                                    m=1, theta_res=90, P_lm=None,
                                    d_P_lm_dtheta=None, unimodular=True,
                                    mu=None, sin_theta=None) :
  '''
  Compute general 2D kernel numerator term 
  after Christensen-Dalsgaard's Lecture Notes
  on Stellar Oscillations Eq. (8.31).

  Note that by default the numerator is normalised
  to be unimodular.

  Parameters
  ----------
  r : ndarray
    Radial coordinates of the eigenfunctions.

  rho : ndarray
    Radial density profile.
  
  xi_r : ndarray
    Mode radial eigenfuction.

  xi_h : ndarray
    Mode horizontal eigenfuction.

  l : int
    Mode spherical degree.
  '''
  if r.ndim==1 :
    # Ensuring we have radial/latitudinal grids
    (r, theta, mu, sin_theta, 
        rho, xi_r, xi_h) = create_grids (r, rho, xi_r, xi_h, theta_res,
                                        theta_0, theta_1)
  if mu is None :
    mu = np.cos (theta)
  if sin_theta is None :
    sin_theta = np.sin (theta)
  if P_lm is None or d_P_lm_dtheta is None :
    P_lm = lpmv (m, l, mu) 
    d_P_lm_dtheta = np.gradient (P_lm, theta[0,:], axis=1)  

  # Computing the different terms
  A = np.abs (xi_r)**2 * P_lm**2 
  B = np.abs (xi_r)**2 * (d_P_lm_dtheta**2 + (m / sin_theta * P_lm)**2)
  C = - P_lm**2 * ((np.conjugate (xi_r)*xi_h).real + (xi_r*np.conjugate (xi_r)).real)
  D = - 2*P_lm * mu / sin_theta * d_P_lm_dtheta * np.abs (xi_h)**2
  numerator = sin_theta * (A + B + C + D) * rho * r**2
  if unimodular :
    norm = trapz (numerator, theta, axis=1)
    norm = trapz (norm, r[:,0])
    numerator /= norm
  else :
    norm = 1

  return numerator, norm

def compute_general_kernel (r, rho, xi_r, xi_h, l=1,
                            m=1, theta_res=90, unimodular=True,
                            theta_0=0, theta_1=180) :
  '''
  Compute general 2D kernel term 
  after Christensen-Dalsgaard's Lecture Notes
  on Stellar Oscillations Eq. (8.31), (8.33),
  and (8.35).

  Note that by default the kernel is normalised
  to be unimodular.

  Parameters
  ----------
  r : ndarray
    Radial coordinates of the eigenfunctions.

  rho : ndarray
    Radial density profile.
  
  xi_r : ndarray
    Mode radial eigenfuction.

  xi_h : ndarray
    Mode horizontal eigenfuction.

  l : int
    Mode spherical degree. Optional, default ``1``.

  m : int
    Mode azimuthal degree. Optional, default ``1``.

  theta_res : int
    Number of grid point in the latitudinal direction.

  unimodular : bool
    Whether to compute a unimodular kernel or not.
    Optional, default ``True``.

  theta_0 : float
    Minimal co-latitude on which to compute the kernel.    

  theta_1 : float
    Maximal co-latitude on which to compute the kernel.    

  Returns
  -------
  tuple
    A tuple of arrays with the 2D-radial grid coordinates, ``r``,
    the 2D-latitudinal grid coordinates, ``theta``, the
    ``beta_nlm`` coefficient and the 2D-kernel, ``K_nlm``. 
  '''
  # Computation in 1D (radial direction)
  prefactor = 2 / (2*(l+1)) * factorial(l+np.abs(m)) / factorial(l-np.abs(m)) 
  to_integrate = (np.abs (xi_r)**2 + l*(l+1)*np.abs (xi_h)**2) * rho * r**2 
  I_nlm = prefactor * trapz (to_integrate, r)

  # Computation in 2D
  (r, theta, mu, sin_theta, 
      rho, xi_r, xi_h) = create_grids (r, rho, xi_r, xi_h, theta_res,
                                       theta_0, theta_1)
  kernel_den = prefactor * (np.abs (xi_r)**2 + l*(l+1)*np.abs (xi_h)**2) * rho * r**2
  P_lm = lpmv (m, l, mu) 
  d_P_lm_dtheta = np.gradient (P_lm, theta[0,:], axis=1)  
  kernel_num, norm = compute_numerator_general_case (r, rho, theta, xi_r, xi_h, l=l,
                                               m=m, theta_res=theta_res, P_lm=P_lm,
                                               d_P_lm_dtheta=d_P_lm_dtheta, unimodular=unimodular,
                                               mu=mu, sin_theta=sin_theta)
  K_nlm = kernel_num / kernel_den
  beta_nlm = norm / I_nlm 
  return r, theta, beta_nlm, K_nlm 

def compute_shellular_kernel (r, rho, xi_r, xi_h, l=1) :
  '''
  Compute beta_nl and K_nl 1D shellular kernels
  terms after Christensen-Dalsgaard's Lecture Notes
  on Stellar Oscillations Eq. (8.42) and Eq. (8.43).

  Parameters
  ----------
  r : ndarray
    Radial coordinates of the eigenfunctions.

  rho : ndarray
    Radial density profile.
  
  xi_r : ndarray
    Mode radial eigenfuction.

  xi_h : ndarray
    Mode horizontal eigenfuction.

  l : int
    Mode spherical degree.
    Optional, default ``1``.

  Returns
  -------
  tuple
    A tuple of arrays with the``beta_nl`` coefficient 
    and the shellular kernel, ``K_nl``. 
  '''
  L = l * (l+1)
  xi_r2 = np.abs (xi_r)**2
  xi_h2 = np.abs (xi_h)**2
  term_1 = (xi_r2+L**2*xi_h2-2*(np.conjugate(xi_r)*xi_h).real-xi_h2)*r**2*rho
  term_2 = (xi_r2+L**2*xi_h2)*r**2*rho
  integral_1 = trapz (term_1, r)
  integral_2 = trapz (term_2, r)
  K_nl = term_1 / integral_1 
  beta_nl = integral_1 / integral_2 

  return beta_nl, K_nl

def compute_shellular_splittings (r, K_nl, Omega, beta_nl, m=1) :
  '''
  Compute rotational splittings in the case
  of a shellular perturbative rotation,
  after Christensen-Dalsgaard's Lecture Notes
  on Stellar Oscillations Eq. (8.41).

  Parameters
  ----------
  r : ndarray
    Radial coordinates.

  K_nl : ndarray
    Radial kernel.

  Omega : ndarray
    Radial rotation profile.

  beta_nl : ndarray
    Prefactor.

  m : int
    Azimuthal number.
    Optional, default ``1``.

  Returns 
  -------
  float
    The shellular rotational splitting.
  '''
  delta_omega_nlm = m*beta_nl*trapz (K_nl*Omega, r)

  return delta_omega_nlm

def compute_splittings (r, theta, K_nlm, Omega, beta_nlm, m=1) :
  '''
  Compute rotational splittings in the general perturbative case,
  after Christensen-Dalsgaard's Lecture Notes on Stellar Oscillations Eq. (8.35).

  Parameters
  ----------
  r : ndarray
    Radial coordinates.

  K_nlm : ndarray
    2D radial/latitudinal kernel.

  Omega : ndarray
    2D radial/latitudinal rotation profile.

  beta_nlm : ndarray
    Prefactor.

  m : int
    Azimuthal number.
    Optional, default ``1``.

  Returns 
  -------
  float
    The rotational splitting.
  '''
  # To work with 2D grids
  if theta.ndim==2 :
    theta = theta[0,:]
  if r.ndim==2 :
    r = r[0,:]
  integrand = trapz (K_nlm*Omega, theta, axis=1)
  integrand = trapz (integrand, r)
  omega_nlm = m*beta_nlm*integrand

  return omega_nlm

def plot_shellular_kernel (r, K_nl, figsize=(6, 6),
                           xlabel=None, ylabel=None, 
                           title=None, **kwargs) :
  """
  Plot shellular kernel.

  Parameters
  ----------
  r : ndarray
    Radial coordinates.

  K_nl : ndarray
    Radial kernel.

  figsize : tuple
    Figure size. Optional, default ``(6,6)``.

  xlabel : str
    x-axis label. Optional, default ``None``.

  ylabel : str
    y-axis label. Optional, default ``None``.

  title : str
    The axes title. Optional, default ``None``.

  Returns
  -------
  matplotlib.pyplot.figure
    The generated figure.
  """
  fig, ax = plt.subplots (1, 1, figsize=figsize)
  
  ax.plot (r, K_nl, **kwargs)
  if xlabel is None :
      xlabel = r"$r/R_\star$"
  if ylabel is None :
      ylabel = r"$K_{n,\ell}$"
  ax.set_xlabel (xlabel)
  ax.set_ylabel (ylabel)
  if title is not None :
    ax.set_title (title)
  return fig

def plot_2D_kernel (r, theta, K_nlm, cmap='cividis',
                    figsize=(3,6), levels=None,
                    contour_colors='black', contour_ls='--',
                    contour_lw=1, vmin=None, vmax=None,
                    shading='nearest', colorbar=False,
                    colorbar_label=None, title=None,
                    add_contour=True, contourf_plot=False,
                    surrounding_lines=True) :
  '''
  Plot 2D kernel. 

  Parameters
  ----------
  r : ndarrray
    2D grid with radial coordinates.

  theta : ndarrray
    2D grid with latitudinal coordinates.

  K_nlm : ndarray
    2D radial/latitudinal kernel.

  cmap : str or Colormap instance
    Color map to use for the kernel.
    Optional, default ``cividis``.

  figsize : tuple
    Figure size. Optional, default ``(3,6)``.

  levels : array-like
    Contour levels. Optional, default ``None``.

  contour_colors : str or Color instance
    Contour color. Optional, default ``black``.

  contour_ls : str
    Contour linestyle. Optional, default ``"--"``.

  contour_lw : str
    Contour linewidth. Optional, default ``1``.

  vmin : float
    Minimal value for the colormap. Optional, default ``None``.

  vmax : float
    Maximal value for the colormap. Optional, default ``None``.

  shading : str
    Shading type. Optional, default ``nearest``.

  colorbar : bool
    Whether to show the colorbar or not. Optional, default ``False``.

  colorbar_label : str
    Color bar label. Optional, default ``None``.

  title : str
    The axes title. Optional, default ``None``.

  add_contour : bool
    If set to ``True``, add contours on the plot.
    Optional, default ``True``.

  contourf_plot : bool.
    If set to ``True``, produce a contour-filled
    plot. Optional, default ``False``.

  surrounding_lines : bool
    If set to ``True``, add surrounding lines to
    the plot. Optional, default ``True``.

  Returns
  -------
  matplotlib.pyplot.figure
    The generated figure.
  '''  
  if colorbar_label is None :
    colorbar_label = r"$K_{n \ell m} (r, \theta)$"

  x = r * np.sin (theta)
  y = r * np.cos (theta)

  fig, ax = plt.subplots (1, 1, figsize=figsize)
  ax.axis ('off')

  if contourf_plot :
    im = ax.contourf (x, y, K_nlm, cmap=cmap, levels=levels)
  else :
    im = ax.pcolormesh (x, y, K_nlm, cmap=cmap, rasterized=True,
                        vmin=vmin, vmax=vmax)
  if add_contour :
    ax.contour (x, y, K_nlm,
                levels=levels, colors=contour_colors, linestyles=contour_ls,
                linewidths=contour_lw)
  # Black lines to give some contours to the model
  if surrounding_lines :
    ax.plot (x[0,:], y[0,:], color='black', lw=1, ls='-')
    ax.plot (x[-1,:], y[-1,:], color='black', lw=1, ls='-')
    ax.plot (x[:,0], y[:,0], color='black', lw=1, ls='-')
    ax.plot (x[:,-1], y[:,-1], color='black', lw=1, ls='-')

  if colorbar :
    cbar = plt.colorbar (im, shrink=0.5)
    cbar.set_label (colorbar_label)
  if title is not None :
    ax.set_title (title)

  return fig
