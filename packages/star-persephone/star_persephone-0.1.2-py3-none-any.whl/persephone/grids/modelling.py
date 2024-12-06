import os
import numpy as np
import persephone
import warnings
import pygyre as pg
from importlib.resources import (as_file, files)
from scipy.special import (eval_legendre,
                           legendre)
from scipy.optimize import least_squares
import matplotlib.pyplot as plt

"""
A set of functions dedicated to perform
stellar modelling on a MESA grid. 
"""

def concatenate_id_number (model_id, model_number) :
  """
  Concatenate directory id and model number to have
  a unique identifier for a given grid element. 
  """
  model_id = np.char.add (model_id, np.full (model_id.size, "_"))
  unique_id = np.char.add (model_id, model_number.astype (str)) 
  return unique_id

def check_observables (history, observable_names) :
  """
  Check that observable names are available
  in the history data file. 

  Parameters
  ----------
  history : dict
    History dictionary loaded through the 
    ``get_history_data`` function.

  observable_names : array-like
    List of observables to check.
  """
  for obs_n in observable_names :
    for keys, h_dict in history.items () :
      if not obs_n in h_dict.bulk_names :
        raise Exception ("{} is missing from {} model".format (obs_n, keys))

def chi_square_one_set (h_dict, observables,
                        observable_names, err_observables=None) :
  '''
  Compute chi-square with observables for one set
  of stellar parameters listed in a dictionary.
  It assumes that all the observables actually
  exist in the dictionary.

  Parameters
  ----------
  h_dict : MesaData
    ``MesaData`` object with the elements loaded from the history 
    data file.

  observables : array-like
    Observable to use to compute chi square.

  observable_names : array-like or List
    The corresponding list of observable names.

  err_observables : array-like
    Uncertainties to consider for the observable set.
    If no uncertainties are provided, ``1`` will be set
    for every parameter (not recommended).
    Optional, default ``None``.

  Returns
  -------
  ndarray
    The computed chi-square array.
  '''
  if err_observables is None :
    err_observables = 1
  else :
    err_observables = np.array (err_observables)
  param = np.array ([h_dict.bulk_data[obs_name] for obs_name in observable_names]).T
  chi_square = np.sum ((param - observables)**2 / err_observables**2, axis=1) 
  # Normalisation step to combine this chi_square with other components 
  # such as the chi_square computed on seismic frequencies
  chi_square /= observables.size
  return chi_square
  
def chi_square_identifier (model, h_dict) :
  '''
  Make identifier so each chi-square computed values
  is easily traceable.
  '''
  return (np.full (h_dict.model_number.size, model), 
          h_dict.model_number)
 
def compute_chi_square_grid (history, observables, 
                             observable_names, 
                             err_observables=None) :
  '''
  Compute chi-square with observables for all sets
  of stellar parameters listed as a dictionary 
  (created through the ``get_history_data`` function) 
  from ``history.data`` files of the whole grid.
  '''
  observables = np.array (observables)
  check_observables (history, observable_names)
  model_id, model_number, chi_square = [], [], []
  for model, h_dict in history.items () :
    _id, _number = chi_square_identifier (model, h_dict)
    _chi_sq = chi_square_one_set (h_dict, observables,
                                  observable_names, 
                                  err_observables=err_observables)
    model_id.append (_id)
    model_number.append (_number)
    chi_square.append (_chi_sq)
  model_id = np.concatenate (model_id)
  model_number = np.concatenate (model_number)
  chi_square = np.concatenate (chi_square)
  return model_id, model_number, chi_square
    
def get_mode_parameters (filename) :
  """
  Get mode order, degrees, azimuthal number, 
  frequencies, normalised inertia, and 
  dimensionless energy from a GYRE summary file. 

  Returns 
  -------
  ndarray
    An array of four columns with, in this order,
    order ``n``, degree ``ell``, azimuthal number
    ``m`` and frequency ``nu`` of the mode. 
  """
  s = pg.read_output (filename) 
  if "m" in s.colnames :
    modes = np.c_[s["n_pg"].data, s["l"].data, 
                  s["m"].data, s["freq"].data.real,
                  s["E_norm"].data, s["H"].data]
    return modes
  else :
    warnings.warn ("No azimuthal numbers found, assuming m=0.")
    modes = np.c_[s["n_pg"].data, s["l"].data, 
                  np.zeros (len (s)), s["freq"].data.real,
                  s["E_norm"].data, s["H"].data]
    return modes

def sanity_check_selected_modes (selected_modes, n_mode_obs,
                                 warn=True) :
  """
  Check that the correct number of modes have been selected 
  in the list of modes available in the model.
  """
  if selected_modes.shape[0]!=n_mode_obs :
    if warn :
      warnings.warn ("The number of selected mode does not fit the number of observed modes.")
    status = False
  else :
    status = True
  return status

def fun_least_squares (coeff_b, target, omega) :
  """
  Function to minimise with least square for surface
  correction prescription ``smooth_l0`` and ``PH16``.
  """
  polynom = 0
  # Not sure we can do without this explicit loop,
  # nevertheless it is a small one
  for ii, b in enumerate (coeff_b) :
    polynom += b * eval_legendre (ii, 1/omega) 
  fun = target - polynom
  return fun

def polynomial_fit_legendre (omega, target, k=2) :
  """
  Perform polynomial fit for surface effect correction
  for ``smooth_l0`` option or 
  as described in Eq. (7) of Pérez-Hernández et al. 2016.
  """
  # Initialising with a no surface correction prescription
  coeff_b0 = np.zeros (k)
  # No bounds on the fit for now, see how it behaves
  result = least_squares (fun_least_squares, coeff_b0, 
                          args=(target, omega))
  # Reconstructing fitted polynom
  polynom = np.poly1d ([0])
  for ii in range (k) :
    polynom = np.polyadd (polynom, result.x[ii] * legendre (ii))
  # Should return a poly1d function
  return polynom

def compute_surface_correction (model_modes, obs_modes, 
                                prescription="smooth_l0", 
                                return_corrected_freq=True) :
  """
  Compute surface corrections for modelled modes.

  Parameters
  ----------
  model_modes : ndarray
    GYRE set of modes to correct.

  obs_modes : ndarray
    Observed set of modes.
    Column order is ``n``, ``\ell``, ``m``,
    ``freq`` and ``e_freq``.

  prescription : str
    Correction prescription to consider. 
    ``"smooth_l0"``: subtraction of a simple smooth function 
    considering the difference between observed l0 and model l0 modes.
    ``"PH16"``: prescription from Pérez-Hernández et al. 2016.

  Returns
  -------
  function or tuple 
    If ``return_corrected_freq`` is ``False``, return only the correction
    function. If ``return_corrected_freq`` is ``True``, return a tuple.  The first
    element of the tuple is the correction function. If prescription is
    ``smooth_l0`` or ``PH16``, the correcting function ``S_B (omega)`` is returned.
    The second element of the tuple is the mode array with corrected frequencies.
  """
  corrected_modes = np.copy (model_modes)
  if prescription not in ["smooth_l0", "PH16"] :
    raise Exception ("Unkown surface correction prescription.")
  elif prescription=="smooth_l0" :
    # Selecting only l=0 modes. model_modes.shape[0] and
    # obs_modes.shape[0] should be the same at this step.
    cond = model_modes[:,1]==0
    target = obs_modes[cond,3]-model_modes[cond,3] 
    target /= obs_modes[cond,3]
    # For now we use model modes frequency as x-axis 
    # See if observed modes frequencies would fit better
    correction_fun = polynomial_fit_legendre (model_modes[cond,3], target, k=2)
    correction = obs_modes[:,3] * correction_fun (1/model_modes[:,3]) 
  elif prescription=="PH16" :
    # TODO There is an issue in the way mode energy is
    # accounted for.
    # Selecting only l=0 modes. model_modes.shape[0] and
    # obs_modes.shape[0] should be the same at this step.
    cond = model_modes[:,1]==0
    target = model_modes[cond,5]*(obs_modes[cond,3]-model_modes[cond,3]) 
    target /= obs_modes[cond,3]
    # For now we use model modes frequency as x-axis 
    # See if observed modes frequencies would fit better
    correction_fun = polynomial_fit_legendre (model_modes[cond,3], target, k=2)
    correction = obs_modes[:,3] * correction_fun (1/model_modes[:,3]) / model_modes[:,5]
  if return_corrected_freq :
    corrected_modes[:,3] = model_modes[:,3] + correction 
    return correction_fun, corrected_modes
  else :
    return correction_fun

def select_modes (model_modes, obs_modes) :
  """
  Select the model modes to have an array fitting
  input observed list of modes.

  Parameters
  ----------
  model_modes : ndarray
    GYRE computed modes parameters.

  obs_modes : ndarray
    Observed modes parameters.

  Returns
  -------
  Selected model modes and corresponding observed modes,
  sorted by frequency.
  """
  obs_order, obs_degree = obs_modes[:,0], obs_modes[:,1]
  model_n_l = np.copy (model_modes[:,[0,1]])
  # Using np.ascontiguous array to avoid raising a ValueError
  _, _, indices = intersect2d (np.c_[obs_order, obs_degree],
                               np.ascontiguousarray (model_n_l))
  selected_modes = model_modes[indices,:]
  sort_obs = np.argsort (obs_modes[:,3])
  obs_modes = obs_modes[sort_obs,:]
  sort_selected = np.argsort (selected_modes[:,3])
  selected_modes = selected_modes[sort_selected,:]
  return obs_modes, selected_modes

def _chi_square_freq (model_modes, obs_modes,
                      surface_correction=None) :
  """
  Compute chi_square for mode frequencies of a given
  model depending on the choice of surface correction
  prescription.

  Parameters
  ----------
  model_modes : ndarray
    GYRE set of modes to correct.

  obs_modes : ndarray
    Observed set of modes.
    Column order is ``n``, ``\ell``, ``m``,
    ``freq`` and ``e_freq``.

  surface_correction : str
    Correction prescription to consider for surface 
    effects. No correction will be applied if ``None``.
    Optional, default ``None``.  
    The possible prescriptions to apply are:
    ``"smooth_l0"``: subtraction of a simple smooth function 
    considering the difference between observed l0 and model l0 modes.
    ``"PH16"``: prescription from Pérez-Hernández et al. 2016.
  """ 
  relative_error = obs_modes[:,4] / obs_modes[:,3]
  if surface_correction is None :
    chi_freq = (obs_modes[:,3]-model_modes[:,3])**2
    chi_freq /= (obs_modes[:,3]*relative_error)**2
    chi_freq = chi_freq.sum () / chi_freq.size
  elif surface_correction in ["smooth_l0", "PH16"] :
    _, corrected_modes = compute_surface_correction (model_modes, obs_modes,
                                          prescription=surface_correction)
    num = (obs_modes[:,3]-corrected_modes[:,3])/obs_modes[:,3] 
    chi_freq = (num / relative_error)**2
    # The chi square is divided here by (N_mode - k - 1)
    # with k=2, see Eq. (8) from Pérez-Hernández et al. 2016
    chi_freq = chi_freq.sum () / (chi_freq.size - 3) 
  return chi_freq

def compute_chi_square_freq_profile (gyre_summary, obs_modes,
                                     surface_correction=None) :
  """
  Compute chi square for seismic frequencies for one
  given profile set of frequencies. 

  Parameters
  ----------
  gyre_summary : str or Path instance
    Path to the GYRE summary file related to the model.

  obs_modes : ndarray
    Observed set of modes.
    Column order is ``n``, ``\ell``, ``m``,
    ``freq`` and ``e_freq``.

  surface_correction : str
    Correction prescription to consider for surface 
    effects. No correction will be applied if ``None``.
    Optional, default ``None``.  
    The possible prescriptions to apply are:
    ``"smooth_l0"``: subtraction of a simple smooth function 
    considering the difference between observed l0 and model l0 modes.
    ``"PH16"``: prescription from Pérez-Hernández et al. 2016.
  """
  model_modes = get_mode_parameters (gyre_summary)
  obs_modes, model_modes = select_modes (model_modes, obs_modes) 
  status = sanity_check_selected_modes (model_modes, obs_modes.shape[0],
                                        warn=False)
  if status :
    chi_square = _chi_square_freq (model_modes, obs_modes,
                        surface_correction=surface_correction)

    return chi_square
  else :
    return np.inf
    
def compute_chi_square_freq_track (star_dir, obs_modes,
                                   surface_correction=None,
                                   template_filename=None) :
  """
  Compute chi square for seismic frequencies for all profiles
  included in the evolutionary track of one model directory.
  """
  (list_profiles, model_number, 
   list_summary) = persephone.grids.get_list_gyre_summary (star_dir, sort=True,
                                          template_filename=template_filename)
  list_profiles, model_number = np.array (list_profiles), np.array (model_number)
  chi_square = np.zeros (len (list_summary))
  for ii, gyre_summary in enumerate (list_summary) :
    chi_square[ii] = compute_chi_square_freq_profile (gyre_summary, obs_modes,
                                         surface_correction=surface_correction)
  # Keeping only model where chi_square could be computed with all 
  # modes
  cond = chi_square!=np.inf
  return list_profiles[cond], model_number[cond], chi_square[cond]

def compute_chi_square_freq_grid (grid_dir, obs_modes,
                                  surface_correction=None,
                                  template_filename=None) :
  """
  Compute chi square for seismic frequencies for all profiles
  on the grid.
  """
  # The model id is not included I guess, it should probably be added
  # while looping on the directories.
  list_dir = persephone.grids.get_listdir (grid_dir)
  list_profiles, model_id, model_number, chi_square = [], [], [], [] 
  for star_dir in list_dir :
    (l_profiles, 
     m_number, 
     c_square) = compute_chi_square_freq_track (star_dir, obs_modes,
                                   surface_correction=surface_correction,
                                   template_filename=template_filename)
    # Careful that we now use numpy arrays. It will have to be assessed
    # what is the most convenient computationnally. This is not ultra-clean
    # but I do not see yet a better way to proceed.
    list_profiles = np.concatenate ([list_profiles, l_profiles])
    model_number = np.concatenate ([model_number, m_number])
    chi_square = np.concatenate ([chi_square, c_square])
    # The model id should be the name of the track directory
    # inside the main grid directory.
    track_id = os.path.split (star_dir)[1]
    model_id = np.concatenate ([model_id, np.full (c_square.size, track_id)])

  model_number = model_number.astype (int)
    
  return list_profiles, model_id, model_number, chi_square

def fit_observables_on_grid (grid_dir, observables,
                             observable_names, err_observables=None,
                             obs_modes=None, surface_correction=None,
                             template_filename=None) :
  """
  Fit a set of observables on the grid using a chi square minimisation. 
  If observed seismic modes frequencies are provided, the fit will be 
  performed considering only models with saved profiles and generated
  GYRE summary.

  Parameters
  ----------
  observables : array-like
    Observable to use to compute chi square.

  observable_names : array-like or List
    The corresponding list of observable names.

  err_observables : array-like
    Uncertainties to consider for the observable set.
    If no uncertainties are provided, ``1`` will be set
    for every parameter (not recommended).
    Optional, default ``None``.

  obs_modes : ndarray
    Observed set of modes.
    Column order is ``n``, ``\ell``, ``m``,
    ``freq`` and ``e_freq``. Optional, default ``None``.

  surface_correction : str
    Correction prescription to consider for mode surface 
    effects. No correction will be applied if ``None``.
    Optional, default ``None``.  

  Returns
  -------
  tuple 
    If ``obs_modes`` is ``None``, returns the directory array
    the model number arrayi, the chi square array and the index of
    the best fit profile. If ``obs_modes`` is not ``None``, returns 
    additionnally the profile name array.
  """
  history = persephone.grids.get_history_data (grid_dir)
  model_id, model_number, chi_square = compute_chi_square_grid (history, observables,
                                                                observable_names,
                                                                err_observables=err_observables)
  if obs_modes is not None :
    (list_profiles,
     model_id_freq, 
     model_number_freq, 
     chi_square_freq) = compute_chi_square_freq_grid (grid_dir, obs_modes,
                                                surface_correction=surface_correction,
                                                template_filename=template_filename)
    unique_id = concatenate_id_number (model_id, model_number)
    unique_id_freq = concatenate_id_number (model_id_freq, model_number_freq)
    _, indices, _ = np.intersect1d (unique_id, unique_id_freq, return_indices=True)
    # The correct sorting of the elements should be checked
    chi_square = chi_square[indices] + chi_square_freq

  i_best_fit = np.argmin (chi_square)
  if obs_modes is not None :
    return (model_id_freq, model_number_freq, 
            chi_square, i_best_fit,
            list_profiles)
  else :
    return (model_id, model_number, 
            chi_square, i_best_fit)

def modes_parameters_kic6603624 () :
  """
  Load mode parameters fitted with ``apollinaire``
  for KIC6603624.

  Returns
  -------
  ndarray
    The observed mode parameters, with an array structure
    ready to be used with ``fit_observables_on_grid``.
  """
  resource = "modes_param_kic6603624.pkb"
  _context_manager = as_file(files(persephone.grids.templates).joinpath(resource))
  with _context_manager as filename :
    (n, l, freq, 
     e_freq, E_freq) = np.loadtxt (filename, usecols=(0,1,2,3,4), unpack=True) 
  # apollinaire automated order labelling has a +/- 1 uncertainties, it seems
  # that here it is indeed shifted
  n += 1
  # Using largest uncertainties
  e_freq = np.maximum (e_freq, E_freq)
  m = np.zeros (n.size)
  obs_modes = np.c_[n, l, m, freq, e_freq] 
  return obs_modes

def compute_dnu (modes) :
    """
    Compute dnu from a set of mode frequencies.
    """
    freq_l0 = np.sort (modes[modes[:,1]==0,3])
    dnu = np.mean (np.diff (freq_l0))
    return dnu

def echelle_diagram (modes, dnu=None, 
                     markers=None, colors=None,
                     ax=None, figsize=(6,6),
                     s=50, labels=None) :
    """
    Compute the echelle diagram for the provided
    set of modes. 
    
    Parameters
    ----------
    modes : tuple or ndarray
      If a simple array is provided, it will be considered as a unique
      set of modes. The array must have at least five columns: order,
      degrees, azimuthal number, frequencies, error on frequencies (set
      0 if not relevant, e.g. for modes obtained from a model.
      Distinct set of modes, each one provided as a ndarray
      can also be passed to the function as a tuple of ndarray. They should
      have the structure described above.
      
    dnu : float
      Large separation to consider for the diagram. If not provided, 
      it will be computed from the first set of modes provided in ``modes``.
      Optional, default ``None``.
    """
    if ax is None :
        fig, ax = plt.subplots (1, 1, figsize=figsize) 
    else :
        fig = ax.get_figure()
    
    ax.set_xlabel (r"$\nu$ mod $\Delta \nu$ ($\mu$Hz)")
    ax.set_ylabel (r"$\nu$ ($\mu$Hz)")
    
    if type(modes)!=tuple :
        # Making a tuple to loop on
        # as in the other expected case
        modes = (modes,)
        
    if dnu is None :
        dnu = compute_dnu (modes[0])
        
    if colors is not None :
        if type (colors)==str :
            colors = (colors,) * len (modes)
    if markers is None :
            markers = "o"
    if type (markers)==str :
        markers = (markers,) * len (modes)
    if labels is None :
        labels = (None,) * len (modes)
    if type (s) in [int, float] :
        s = (s,) * len (modes)
        
    for ii, mode_set in enumerate (modes) :
        freq, e_freq = mode_set[:,3], mode_set[:,4]
        if colors is None :
            color = "C{}".format (ii)
        else :
            color = colors[ii]
        ax.scatter (freq%dnu, freq, edgecolor=color,
                    marker=markers[ii], facecolor="none",
                    s=s[ii], label=labels[ii])
    if labels[0] is not None :
        ax.legend ()
    return fig
  

def intersect2d (a, b) :
  """
  Intersect row-wise numpy arrays
  """
  nrows, ncols = a.shape
  dtype={'names':['f{}'.format(i) for i in range(ncols)],
         'formats':ncols * [a.dtype]}

  c, ind_a, ind_b = np.intersect1d (a.view(dtype), b.view(dtype),
                                    return_indices=True)
  c = c.view(a.dtype).reshape(-1, ncols)
  return c, ind_a, ind_b
