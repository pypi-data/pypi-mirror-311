import persephone
import numpy as np
from scipy.integrate import trapz

"""
A set of functions to compute useful
functions from mode eigenfunctions.
"""

def compute_mode_inertia (r, rho, xi_r, xi_h,
                          l=1, normalise=True, 
                          verbose=False) :
  '''
  Compute (optionnally normalised) mode inertia.

  See JCD Eq. 4.48
  '''
  mstar = trapz (4*np.pi*r**2*rho, r) 
  integrand = np.abs (xi_r)**2 + l*(l+1)*np.abs (xi_h)**2 * rho * r**2
  numerator = 4*np.pi * trapz (integrand, r)
  den = mstar * np.abs (xi_r[-1])**2 + l*(l+1)*np.abs (xi_h[-1])**2 
  if normalise :
    inertia = numerator / den
  else :
    inertia = numerator
  if verbose :
    print ("Computed stellar mass is {:.2f} Msun".format (mstar/persephone.Msun))

  return inertia

def compute_kinetic_energy_density (r, rho, xi_r, xi_h, l=1,
                                    normalise_max=False, 
                                    normalise_integral=False) :
  '''
  Compute kinetic energy density (see Provost et al. 2000)
  '''
  ked = rho * r**2 * (np.abs (xi_r)**2 + l*(l+1) * np.abs (xi_h)**2)
  if normalise_max :
    ked /= np.amax (ked)
  if normalise_integral :
    norm = trapz (ked, r/np.amax (r))
    ked /= norm

  return ked

def compute_pressure_integral (r, p, eul_p, gamma, cutoff=1) :
  '''
  Compute pressure contribution integral 
  (see Provost et al. 2000, Eq. 3)
  '''
  integrand = np.abs (eul_p)**2 / (gamma*p) * r**2
  cond = r<cutoff*r[-1]
  I_1 = 4*np.pi * trapz (integrand[cond], r[cond])
  return I_1

def compute_N2 (r, A, mass_profile) :
  '''
  Recompute Brunt-Vaisala frequency from GYRE outputs.
  '''
  # For gravity we use only the norm.
  g = persephone.gravity_constant * mass_profile / r**2
  N2 = g * A / r 
  return N2

def compute_buoyancy_integral (r, A, rho, xi_r, xi_h, 
                               mass_profile, cutoff=0.98) :
  '''
  Compute buoyancy contribution integral 
  (see Provost et al. 2000, Eq. 3)
  
  N2 is recomputed in-situ because of the profile
  outputs availability provided by GYRE. 
  '''
  N2 = compute_N2 (r, A, mass_profile)
  integrand = N2 * rho * (np.abs (xi_r)**2 + np.abs (xi_h)**2) * r**2 
  # removing nan value due to the r division to retrieve N2
  mask = ~np.isnan (integrand)
  cond = r<cutoff*r[-1]
  I_2 = 4*np.pi * trapz (integrand[mask&cond], r[mask&cond])
  return I_2

def compute_approx_frequency (r, A, rho, xi_r, xi_h,
                              mass_profile, p, eul_p,
                              gamma, l=1, cutoff=1) :
  '''
  Compute Provost et al. 2000, Eq. 3
  '''
  I_1 = compute_pressure_integral (r, p, eul_p, gamma,
                                   cutoff=cutoff)
  I_2 = compute_buoyancy_integral (r, A, rho, xi_r, xi_h,
                               mass_profile, cutoff=cutoff)
  inertia = compute_mode_inertia (r, rho, xi_r, xi_h, l=l,
                                  normalise=False)
  return 2*np.pi * np.sqrt ((I_1 + I_2) / inertia)
