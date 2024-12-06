import numpy as np
import mesa_reader as mr
import matplotlib.pyplot as plt
import importlib.resources
import os
import subprocess
import shutil
import persephone
import warnings
import h5py
import glob
from pathos.pools import ProcessPool
import pathlib

"""
A set of functions to build and manage a
MESA grid.
"""

def get_listdir (directory, sort=True) :
  """
  Get absolute or relative list of directories.

  Returns 
  -------
  List
    The list of directories in ``directory``.
  """
  listdir = [entry.path for entry in os.scandir(directory) if entry.is_dir ()]
  if sort :
    listdir.sort ()
  return listdir

def get_mesa_dir () :
  """
  Get MESA directory path through the
  ``MESA_DIR`` environment variable.

  Returns
  -------
  str
    The path stored in the ``MESA_DIR``
    environment variable.
  """
  try :
    mesa_dir = os.environ["MESA_DIR"]
  except KeyError :
    raise Exception ("MESA_DIR environment variable not found. Check that MESA is properly installed.")
  return mesa_dir

def get_listdir_gyre_details (star_dir, sort=True) :
  """
  Get absolute or relative list of GYRE details directories
  in a MESA model work directory.

  star_dir : str or Path object
    Path of the consider MESA working directory.

  sort : bool
    Returned list will be sorted if ``True``.
    Optional, default ``True``.

  Returns 
  -------
  List
    The list of GYRE details directories in the ``LOGS``
    directory of ``star_dir``.
  """
  directory = os.path.join (star_dir, "LOGS")
  listdir = [entry.path for entry in os.scandir(directory) if entry.is_dir () \
             and "details" in os.path.basename (entry.path)]
  if sort :
    listdir.sort ()
  return listdir

def get_detail_file (details_dir, n=1, l=0, m=0,
                     detail_template=None) :
  """
  Get the path of a detail file in a directory
  ``details_dir``.

  Parameters
  ----------
  details_dir : str or Path object
    Directory where GYRE details file are stored.

  n : int
    mode order

  l : int 
    mode degree

  m : int
    mode azimuthal number

  detail_template : str
    Detail template of the detail files if not 
    standard. Optional, default ``None``.

  Returns
  -------
  tuple
    A tuple with the path of the file
    and a boolean stating if the file
    actually exists.
  """
  if detail_template is None :
    detail_template = "detail.n{}.l{}.m{}.h5"
  if n>= 0 :
    n = "+{}".format (n)
  else :
    n = "{}".format (n)
  l = "{}".format (l)
  if m>= 0 :
    m = "+{}".format (m)
  else :
    m = "{}".format (m)
  filename = os.path.join (details_dir, 
                detail_template.format (n, l, m))
  status = os.path.exists (filename)
  return filename, status

def get_list_profiles (star_dir, sort=True) :
  """
  Get absolute or relative list of MESA profiles
  in a MESA model work directory.

  Parameters
  ----------
  star_dir : str or Path object
    Path of the consider MESA working directory.

  sort : bool
    Returned list will be sorted if ``True``.
    Optional, default ``True``.

  Returns 
  -------
  List
    The list of MESA profile files in the ``LOGS``
    directory of ``star_dir``.
  """
  pattern = os.path.join (star_dir, "LOGS", "profile*.data")
  list_profiles = glob.glob (pattern)
  if sort :
    list_profiles.sort ()
  return list_profiles

def get_list_profiles_grid (grid_dir, sort=True) :
  """
  Get absolute or relative list of MESA profiles
  in a whole model grid.

  Parameters
  ----------
  grid_dir : str or Path object
    Path of the grid.

  sort : bool
    Returned list will be sorted if ``True``.
    Optional, default ``True``.

  Returns 
  -------
  List
    The list of MESA profile files in the whole grid.
  """
  list_profiles = []
  listdir = get_listdir (grid_dir, sort)
  for star_dir in listdir :
    list_profiles += get_list_profiles (star_dir, sort=sort)
  return list_profiles

def get_profile (filename) :
  """
  Read the profile located at ``filename`` as a 
  ``MesaData`` object.

  Parameters
  ----------
  filename : str or Path instance
    The path to the file with the profile to read.

  Returns
  -------
  MesaData
    A MesaData object as constructed by ``pymesa_reader``.
  """
  p = mr.MesaData (filename)
  return p

def get_profile_model_number (star_dir) :
  """
  Return list of model numbers corresponding to the profile
  saved in the MESA ``LOGS`` directory.
  """
  list_profiles = get_list_profiles (star_dir, sort=True)
  model_number = []
  for filename in list_profiles :
    p = get_profile (filename)
    model_number.append (p.model_number)
  return list_profiles, model_number

def get_gyre_summary (profile_name, template_filename=None) :
  """
  Get GYRE summary file path from corresponding 
  profile name.

  Parameters
  ----------
  profile_name : str or Path instance
    Path to the model profile for which to recover
    GYRE summary path.

  Returns
  -------
  str
    The path for the GYRE summary file.
  """
  if template_filename is None :
    template_filename = "{}_gyre_summary.h5"
  file_summary = template_filename.format (os.path.splitext(profile_name)[0])
  return file_summary

def get_list_gyre_summary (star_dir, sort=True,
                           template_filename=None) :
  """
  Get absolute or relative list of GYRE summary files
  in a MESA model work directory.

  Parameters
  ----------
  star_dir : str or Path object
    Path of the consider MESA working directory.

  sort : bool
    Returned list will be sorted if ``True``.
    Optional, default ``True``.

  Returns 
  -------
  tuple of Lists
    In this order: the list of MESA profile, the 
    corresponding list of model numbers in the ``history.data``
    file, the list of GYRE summary files in the ``LOGS``
    directory of ``star_dir``.
  """
  if template_filename is None :
    template_filename = "{}_gyre_summary.h5"
  list_profiles, model_number = get_profile_model_number (star_dir)
  list_summary = []
  status = read_status_dir (star_dir, attribute="run_gyre_done") 
  if status :
    for filename in list_profiles :
      file_summary = template_filename.format (os.path.splitext(filename)[0])
      if not os.path.exists (file_summary) :
        warnings.warn ("File {} should exist but not found.".format (file_summary),
                      skip_file_prefixes=(os.path.dirname(__file__),))
      list_summary.append (file_summary)
    
  return list_profiles, model_number, list_summary

def get_supported_mesa_version () :
  """
  Get list of supported MESA versions.
  """
  versions = ["r15140",
              "r21.12.1",
              "r22.05.1",
              "r22.11.1",
              "r23.05.1"]
  return versions

def load_inlist_template () :
  """
  Load inlist empty template and return
  it as a list of strings (one element for 
  each line).
  """
  f = importlib.resources.open_text (persephone.grids.templates, 
                                     "empty_inlist")
  template = [line.rstrip () for line in f]
  f.close ()
  return template

def save_template (filename, template) :
  """
  Save a template provided as a list of string
  into a text file.
  """
  with open (filename, "w") as f:
    for line in template :
      f.write (line + "\n")
    f.close ()

def copy_profile_columns_file (repo_path, default="persephone", 
                               filename=None, mesa_version="r15140") :
  """
  Copy profile columns file.
  """
  if filename is None : 
    if default=="persephone" :
      if importlib.resources.files (persephone.grids.templates).joinpath (
                            "default_profile_columns_{}.list".format (mesa_version)
                             ).is_file () :
        _context_manager = importlib.resources.as_file (
                           importlib.resources.files (persephone.grids.templates).joinpath (
                              "default_profile_columns_{}.list".format (mesa_version)
                               )
                           )
      else :
        default = "MESA"
    if default=="MESA" :
      mesa_dir = get_mesa_dir ()
      _context_manager = pathlib.Path (mesa_dir, "star/defaults/profile_columns.list")
  else :
    _context_manager = pathlib.Path (filename)
  with _context_manager as f :
    shutil.copy (f, os.path.join (repo_path, "profile_columns.list"))

def copy_history_columns_file (repo_path, default="persephone",
                              filename=None, mesa_version="r15140") :
  """
  Copy history columns file.
  """
  if filename is None :
    if default=="persephone" :
      if importlib.resources.files (persephone.grids.templates).joinpath (
                            "default_history_columns_{}.list".format (mesa_version)
                             ).is_file () :
        _context_manager = importlib.resources.as_file (
                           importlib.resources.files (persephone.grids.templates).joinpath (
                                "default_history_columns_{}.list".format (mesa_version)
                                )
                           )
      else :
        default = "MESA"
    if default=="MESA" :
      mesa_dir = get_mesa_dir ()
      _context_manager = pathlib.Path (mesa_dir, "star/defaults/history_columns.list")
  else :
    _context_manager = pathlib.Path (filename)
  with _context_manager as f :
    shutil.copy (f, os.path.join (repo_path, "history_columns.list"))

def insert_namelist (template, namelist, 
                     namelist_dict) :
  """
  Insert all parameter line 
  related to one type of parameters 
  into the inlist template.
  """ 
  ii, jj = 0, 0 
  while not "&"+namelist in template[ii] :
    ii+= 1
  for elt in namelist_dict.items () :
    string = "  {}={}".format (elt[0], elt[1])
    template.insert (ii+jj+1, string) 
    jj += 1
  return template

def set_default_inlist (parameters=None, 
                        mesa_version="r15140") :
  """
  Set default values for parameter dictionary.

  Parameters
  ----------
  parameters : dict
    Input dictionary of MESA namelist. The function will
    not override parameters if already set.

  Returns 
  -------
  dict
    Dictionary with the default set of parameters used by ``persephone``.
  """
  versions = get_supported_mesa_version ()
  if mesa_version not in versions :
    raise Exception ("Specified MESA version is not supported. Supported versions are {}".format (versions))

  if parameters is None :
    parameters = {}
  # Initialising subdictionaries if not provided
  parameters.setdefault ("star_job", {})
  parameters.setdefault ("eos", {})
  parameters.setdefault ("kap", {})
  parameters.setdefault ("controls", {})
  # Creating variable for dictionaries
  star_job = parameters["star_job"]
  eos = parameters["eos"]
  kap = parameters["kap"]
  controls = parameters["controls"]

  # Star job namelist default
  star_job.setdefault ("create_pre_main_sequence_model", ".true.")
  star_job.setdefault ("load_saved_model", ".false.")
  star_job.setdefault ("save_model_when_terminate", ".true.")
  star_job.setdefault ("save_model_filename", "'final_model.mod'")
  star_job.setdefault ("profile_columns_file", "'profile_columns.list'")
  star_job.setdefault ("history_columns_file", "'history_columns.list'")
  star_job.setdefault ("pgstar_flag", ".false.")
  # Kap namelist default 
  kap.setdefault ("use_type2_opacities", ".true.")
  kap.setdefault ("zbase", "0.02")
  # Controls namelist default
  controls.setdefault ("initial_mass", "1.0")
  controls.setdefault ("initial_z", "0.0134")
  controls.setdefault ("initial_y", "-1")
  controls.setdefault ("mixing_length_alpha", "2.15")
  if mesa_version==versions[0] : 
    controls.setdefault ("use_dedt_form_of_energy_eqn", ".true.")
  elif mesa_version in versions[1:] :
    controls.setdefault ("energy_eqn_option", "'dedt'")
  controls.setdefault ("use_gold_tolerances", ".true.")
  controls.setdefault ("max_num_profile_models", "50000")
  controls.setdefault ("profile_interval", "100")
  controls.setdefault ("write_pulse_data_with_profile", ".true.")
  controls.setdefault ("pulse_data_format", "'GYRE'")
  controls.setdefault ("add_atmosphere_to_pulse_data", ".true.")
  controls.setdefault ("xa_central_lower_limit_species(1)", "'h1'")
  controls.setdefault ("xa_central_lower_limit(1)", "1d-7")
  controls.setdefault ("use_ledoux_criterion", ".true.")
  return parameters

def make_inlist (parameters=None, filename=None,
                 mesa_version="r15140") :
  """
  Make the inlist file for the model using a default
  parameter dictionary or the parameter dictionary 
  provided by the user.
  """
  parameters = set_default_inlist (parameters,
                                   mesa_version=mesa_version)

  template = load_inlist_template ()
  for elt in parameters.items () :
    template = insert_namelist (template, elt[0],
                                elt[1])
  if filename is not None :
    save_template (filename, template)
  return template 

def copy_mesa_work (star_dir) :
  """
  Copy MESA reference work directory.

  Parameters
  ---------- 
  star_dir : str or Path object
    MESA working directory to consider.
  """
  mesa_dir = get_mesa_dir ()
  shutil.copytree (os.path.join (mesa_dir, "star/work"),
                   star_dir)
  # Remove unnecessary default MESA inlist
  os.remove (os.path.join (star_dir, "inlist_project"))
  os.remove (os.path.join (star_dir, "inlist_pgstar"))

def create_metadata_file (star_dir) :
  """
  Create metadata file in MESA directory.

  Parameters
  ---------- 
  star_dir : str or Path object
    MESA working directory to consider.
  """
  filename = os.path.join (star_dir, "persephone_metadata.h5")
  with h5py.File (filename, "x") as f :
    grp = f.create_group ("persephone")
    grp.attrs["version"] = persephone.__version__
    grp.attrs["compile_mesa_done"] = False
    grp.attrs["run_mesa_done"] = False
    grp.attrs["run_gyre_done"] = False
    f.close ()

def check_metadata (star_dir) :
  """
  Check if the ``persephone`` metadata
  file exists

  Parameters
  ---------- 
  star_dir : str or Path object
    MESA working directory to consider.

  Returns
  -------
  bool
    Return ``True`` if the file exists, ``False`` instead.
  """
  status = os.path.exists (os.path.join (star_dir, "persephone_metadata.h5")) 
  return status

def read_status_dir (star_dir, attribute="run_mesa_done") :
  """
  Read status in metadata file in MESA directory.

  Parameters
  ---------- 
  star_dir : str or Path object
    MESA working directory to consider.

  attribute : str
    Keyword to read in the ``persephone_metadata.h5``
    file. Optional, default ``run_mesa_done``.

  Returns
  -------
  bool
    The status of the considered directory relatively
    to the the ``attribute`` keyword``.
  """
  filename = os.path.join (star_dir, "persephone_metadata.h5")
  with h5py.File (filename, "r") as f :
    grp = f["persephone"]
    status = grp.attrs[attribute] 
    f.close ()
  return status

def set_status_dir (star_dir, attribute="run_mesa_done",
                    status=True) :
  """
  Set status in metadata file in MESA directory.

  Parameters
  ---------- 
  star_dir : str or Path object
    MESA working directory to consider.

  attribute : str
    Keyword to set in the ``persephone_metadata.h5``
    file. Optional, default ``run_mesa_done``.

  status : bool
    Status to set. Optional, default ``True``.
  """
  filename = os.path.join (star_dir, "persephone_metadata.h5")
  with h5py.File (filename, "r+") as f :
    grp = f["persephone"]
    grp.attrs[attribute] = status
    f.close ()

def compile_repository (star_dir, verbose=True) :
  """
  Compile MESA work repository.

  Parameters
  ---------- 
  star_dir : str or Path object
    MESA working directory to consider.

  verbose : bool
    Output verbosity. Optional, default ``True``.
  """
  if read_status_dir (star_dir, attribute="compile_mesa_done") :
    if verbose :
      print ("Directory at {} already compiled.".format (star_dir))
  else :
    if verbose :
      print ("Compiling directory at {}.".format (star_dir))
    with open (os.path.join (star_dir, "compile_mesa.out"), "w") as stdout :
      subprocess.run ("./mk", shell=True, cwd=star_dir,
                      stdout=stdout,
                      )
      stdout.close ()
    set_status_dir (star_dir, attribute="compile_mesa_done")

def run_mesa_model (star_dir, verbose=True,
                    rerun=False) :
  """
  Run MESA in selected repository.

  Parameters
  ---------- 
  star_dir : str or Path object
    MESA working directory to consider.

  verbose : bool
    Output verbosity. Optional, default ``True``.

  rerun : bool
    If set to ``True``, MESA will be run even
    if the status of ``run_mesa_done`` is ``True``.
  """
  status = read_status_dir (star_dir, attribute="run_mesa_done")
  if rerun or not status :
    if verbose :
      print ("Running model at {}.".format (star_dir))
    with open (os.path.join (star_dir, "run_mesa.out"), "w") as stdout :
      subprocess.run ("./rn", shell=True, cwd=star_dir,
                      stdout=stdout,
                      )
      stdout.close ()
    set_status_dir (star_dir, attribute="run_mesa_done")
  elif verbose :
      print ("Model at {} has already been run, set rerun to True if you want to run MESA again.".format (star_dir))

def create_mesa_model (path=".", model_dir="MESA_work_dir", mesa_version="r15140", 
                       default_history="persephone", default_profile="persephone",
                       profile_columns=None, history_columns=None, 
                       parameters=None, compile_mesa=True, run_mesa=False,
                       run_gyre=False, parameters_gyre=None, template_file_gyre=None,
                       verbose=True, erase_existing=False, add_details=False,
                       rerun=False) :
  """
  Create, initialise, and (optionally) run, repository for a
  given stellar evolution model.

  Parameters
  ----------
  path : str or Path object
    Path where to create the model directory. Optional, default ".".

  model_dir : str or Path object
    Name of the model directory. Optional, default ``MESA_work_dir``.

  mesa_version : str
    MESA version installed on the system. Optional, default "r15140". 

  default_history : str
    Where to take the default history file: from the ``persephone`` 
    installation ("persephone" option) or from the MESA installation
    ("MESA" option). Optional, default ``"persephone"``.

  default_profile : str
    Where to take the default profile file: from the ``persephone`` 
    installation ("persephone" option) or from the MESA installation
    ("MESA" option). Optional, default ``"persephone"``.

  profile_columns : str or Path object
    MESA profile columns file to replace the one used by default by
    ``persephone``. Optional, default ``None``.

  history_columns : str or Path object
    MESA history columns file to replace the one used by default by
    ``persephone``. Optional, default ``None``.

  parameters : dict
    MESA inlist parameter dictionary. Keys are MESA inlist namelists,
    each key contains a dictionary with parameter name as keys and 
    selected status as element.

  compile_mesa : bool
      Whether to compile MESA or not. Optional, default ``True``.

  run_mesa : bool
    Whether to run MESA or not. Optional, default ``False``.

  run_gyre :
    Whether to run GYRE on the computed MESA profiles or not. 
    ``run_mesa`` needs to be set to ``True`` for this option
    to have effects.
    Optional, default ``False``.

  parameters_gyre : dict
    Dictionary of parameters to add to the GYRE input file.
    Optional, default ``None``.

  template_file_gyre : dict
    Template GYRE input file to replace the one used by default by
    ``persephone``. Optional, default ``None``

  verbose : bool
      Output verbosity.

  erase_existing : bool
    If set to ``True``, existing model directories will be erased
    when existing, otherwise they will be ignored. 
    Optional, default ``False``.

  add_details : bool
    Add a GYRE details output file template if set to ``True``
    and create ``details`` output directories together with the GYRE
    input files.

  rerun : bool
    If set to ``True`` and the directory already existed, 
    MESA will be rerun.
  """
  star_dir = os.path.join (path, model_dir)
  # Erasing directory if necessary
  if os.path.exists (star_dir) :
    if erase_existing :
      print ("Erasing existing directory at {} and creating new one.".format (star_dir))
      os.rmdir (star_dir)
    elif verbose :
      print ("Directory at {} already exist.".format (star_dir))
  elif verbose :
    print ("Creating new MESA work directory at {}.".format (star_dir))
  if not check_metadata (star_dir) :
    # Copying MESA work directory
    copy_mesa_work (star_dir)
    # Copying column file 
    copy_profile_columns_file (star_dir, default=default_profile,
                               filename=profile_columns, mesa_version=mesa_version)
    # Copying history file
    copy_history_columns_file (star_dir, default=default_history, 
                               filename=history_columns, mesa_version=mesa_version)
    # Creating inlist 
    make_inlist (parameters=parameters, 
                 filename=os.path.join (path, model_dir, "inlist"),
                 mesa_version=mesa_version)
    # Create metadata file
    create_metadata_file (star_dir)

  # Compiling MESA
  if compile_mesa :
    compile_repository (star_dir, verbose=verbose) 
  # Running MESA
  if run_mesa :
    run_mesa_model (star_dir, verbose=verbose,
                    rerun=rerun)
    # Running GYRE (only if MESA has been run before)
    if run_gyre :
      analyse_gyre (star_dir, run=True, 
                    template_file=template_file_gyre,
                    parameters=parameters_gyre, verbose=verbose,
                    rerun=rerun, add_details=add_details)

def make_ranges (mstar_min=1., mstar_max=1.2, mstar_step=0.1,
                 z_min=0.01, z_max=0.02, z_step=0.01) :
  """
  Make mass and metallicity ranges to use.

  Parameters
  ----------

  mstar_min : float
    Minimal mass (in solar mass) to consider in the grid.

  mstar_max : float
    Maximal mass (in solar mass) to consider in the grid.

  mstar_step : float
    Mass step (in solar mass) to consider in the grid.

  z_min : float
    Minimal metallicity to consider in the grid.

  z_max : float
    Minimal metallicity to consider in the grid.

  z_step : float
    Metallicity step to consider in the grid.

  Returns
  -------
  tuple
    Tuple of list with mass and metallicity to use
    when computing the grid.

  """
  range_mstar = [mstar_min]
  range_z = [z_min]
  if mstar_step is not None :
    ii = 1
    while mstar_min + ii*mstar_step <= mstar_max :
      range_mstar.append (mstar_min + ii*mstar_step)
      ii += 1
    # Adding the maximal value if necessary 
    if mstar_max not in range_mstar :
      range_mstar.append (mstar_max)

  if z_step is not None :
    ii = 1
    while z_min + ii*z_step <= z_max :
      range_z.append (z_min + ii*z_step)
      ii += 1
    # Adding the maximal values if necessary 
    if z_max not in range_z :
      range_z.append (z_max)

  return range_mstar, range_z

def create_grid (grid_dir, model_dir_name_template=None, 
                 mesa_version="r15140", 
                 mstar_min=1., mstar_max=1.2, mstar_step=0.1,
                 z_min=0.01, z_max=0.02, z_step=None, 
                 range_mstar=None, range_z=None,
                 default_history="persephone", default_profile="persephone",
                 profile_columns=None, history_columns=None,
                 parameters=None, compile_mesa=True, run_mesa=False,
                 run_gyre=False, verbose=True, erase_existing=False,
                 parameters_gyre=None, template_file_gyre=None,
                 parallelise=False, nodes=2, add_details=False,
                 rerun=False) : 
  """
  Create MESA models grid with a given range of mass and metallicity.

  Parameters
  ----------
  grid_dir : str or Path object
    Directory of the grid.

  model_dir_name_template : str
    Template to use for the model directories. 
    If ``None``, the template name will be ``mesa_model_mstar_{}_z_{}``
    Optional, default ``None``.
  
  mesa_version : str
    MESA version installed on the system. Optional, default "r15140". 

  mstar_min : float
    Minimal mass (in solar mass) to consider in the grid.

  mstar_max : float
    Maximal mass (in solar mass) to consider in the grid.

  mstar_step : float
    Mass step (in solar mass) to consider in the grid.

  z_min : float
    Minimal metallicity to consider in the grid.

  z_max : float
    Minimal metallicity to consider in the grid.

  z_step : float
    Metallicity step to consider in the grid.

  range_mstar : array-like
    Range of mass to consider (in solar mass). If provided, ``mstar_min``, 
    ``mstar_max``, and ``mstar_step`` will be ignored.
    Optional, default ``None``.

  range_z : array-like
    Range of metallicity to consider. If provided, ``z_min``, ``z_max``, and
    ``z_step`` will be ignored.
    Optional, default ``None``.

  default_history : str
    Where to take the default history file: from the ``persephone`` 
    installation ("persephone" option) or from the MESA installation
    ("MESA" option). Optional, default ``"persephone"``.

  default_profile : str
    Where to take the default profile file: from the ``persephone`` 
    installation ("persephone" option) or from the MESA installation
    ("MESA" option). Optional, default ``"persephone"``.

  profile_columns : str or Path object
    MESA profile columns file to replace the one used by default by
    ``persephone``. Optional, default ``None``.

  history_columns : str or Path object
    MESA history columns file to replace the one used by default by
    ``persephone``. Optional, default ``None``.

  parameters : dict
    MESA inlist parameter dictionary. Keys are MESA inlist namelists,
    each key contains a dictionary with parameter name as keys and 
    selected status as element.

  compile_mesa : bool
      Whether to compile MESA or not. Optional, default ``True``.

  run_mesa : bool
    Whether to run MESA or not. Optional, default ``False``.

  run_gyre :
    Whether to run GYRE on the computed MESA profiles or not. 
    ``run_mesa`` needs to be set to ``True`` for this option
    to have effects.
    Optional, default ``False``.

  verbose : bool
      Output verbosity.

  erase_existing : bool
    If set to ``True``, existing model directories will be erased
    when existing, otherwise they will be ignored. 
    Optional, default ``False``.

  parameters_gyre : dict
    Dictionary of parameters to add to the GYRE input file.
    Optional, default ``None``.

  template_file_gyre : dict
    Template GYRE input file to replace the one used by default by
    ``persephone``. Optional, default ``None``

  parallelise : bool 
    Whether to run the MESA and GYRE runs in parallel through 
    ``pathos.multiprocess``. Optional, default ``False``.

  nodes : int
    Number of nodes used in ``pathos.multiprocess.ProcessPool``
    when ``parallelise=True``. Optional, default ``2``.

  add_details : bool
    Add a GYRE details output file template if set to ``True``
    and create ``details`` output directories together with the GYRE
    input files.

  rerun : bool
    If set to ``True``, MESA and GYRE will be rerun in directories
    where they have already been run.
  """
  if not os.path.exists (grid_dir) :
    os.mkdir (grid_dir)
  if model_dir_name_template is None :
    model_dir_name_template = "mesa_model_mstar_{}_z_{}"
  aux_range_mstar, aux_range_z = make_ranges (mstar_min=mstar_min, 
                                      mstar_max=mstar_max, mstar_step=mstar_step,
                                      z_min=z_min, z_max=z_max, z_step=z_step)
  if range_mstar is None :
    range_mstar = aux_range_mstar
  if range_z is None :
    range_z = aux_range_z

  parameters = set_default_inlist (parameters, mesa_version=mesa_version)
  for mstar in range_mstar :
    for z in range_z :
       model_dir = model_dir_name_template.format (str(mstar), str(z))
       parameters["controls"]["initial_mass"] = str (mstar)
       parameters["controls"]["initial_z"] = str (z)
       create_mesa_model (path=grid_dir, model_dir=model_dir,
                          default_history=default_history, 
                          default_profile=default_profile,
                          profile_columns=profile_columns, 
                          history_columns=history_columns,
                          parameters=parameters, compile_mesa=compile_mesa, 
                          run_mesa=False, run_gyre=False, mesa_version=mesa_version,
                          verbose=verbose, erase_existing=erase_existing)
  if compile_mesa and run_mesa :
    run_grid (grid_dir, verbose=verbose, parallelise=parallelise,
              nodes=nodes, rerun=rerun)
    if run_gyre :
      analyse_grid_gyre (grid_dir, parameters=parameters_gyre,
                         template_file=template_file_gyre,
                         verbose=verbose, parallelise=parallelise,
                         nodes=nodes, add_details=add_details,
                         rerun=rerun)
    

def compile_grid (grid_dir, verbose=True) :
  """
  Compile MESA in model directories. 

  Parameters
  ----------
  grid_dir : str or Path object
    Directory of the grid.
 
  verbose : bool
    Output verbosity.
  """
  listdir = get_listdir (grid_dir)
  for star_dir in listdir :
    if check_metadata (star_dir) :
        compile_repository (star_dir, verbose=verbose)

def _run_wrapper (star_dir, rerun=False, verbose=False) :
  """
  Convenience wrapper for parallelisation.
  """
  if check_metadata (star_dir) :
    run_mesa_model (star_dir, verbose=verbose,
                    rerun=rerun)

def run_grid (grid_dir, verbose=True, rerun=False,
              parallelise=False, nodes=2) :
  """
  Run MESA in model directories. Directories with `run_mesa_done`
  metadata set to ``True`` will be re-run only if ``rerun``
  is set to ``True``.

  Parameters
  ----------
  grid_dir : str or Path object
    Directory of the grid.
 
  verbose : bool
    Output verbosity.

  rerun : bool
    If set to ``True``, MESA will be rerun in directories
    where it has already been run.

  parallelise : bool 
    Whether to run the MESA and GYRE runs in parallel through 
    ``pathos.multiprocess``. Optional, default ``False``.

  nodes : int
    Number of nodes used in ``pathos.multiprocess.ProcessPool``
    when ``parallelise=True``. Optional, default ``2``.
  """
  listdir = get_listdir (grid_dir)
  if parallelise :
    if verbose :
      print ("Running MESA in parallel with {} nodes on grid located at {}.".format (nodes, 
                                                                                 grid_dir))
    pool = ProcessPool (nodes=nodes)
    pool.map (_run_wrapper, 
              listdir,
              [rerun] * len(listdir),
             )
  else :
    for star_dir in listdir :
      _run_wrapper (star_dir, rerun=rerun,
                    verbose=verbose)

def get_gyre_dir () :
  """
  Get GYRE directory path through the
  ``GYRE_DIR`` environment variable.

  Returns
  -------
  str
    The path stored in the ``GYRE_DIR``
    environment variable.
  """
  try :
    gyre_dir = os.environ["GYRE_DIR"]
  except KeyError :
    raise Exception ("GYRE_DIR environment variable not found. Check that GYRE is properly installed.")
  return gyre_dir

def get_kernel_example_gyre_input () :
  """
  Get GYRE input file to use for the kernel
  example notebook.
  """
  f = importlib.resources.path (persephone.grids.templates,
                                "kernel_example_gyre.in")
  return f

def show_kernel_example_gyre_input () :
  """
  Show GYRE input file to use for the kernel
  example notebook as a string.
  """
  f = importlib.resources.open_text (persephone.grids.templates,
                                     "kernel_example_gyre.in")
  with f as lines :
    for line in lines :
      print (line.rstrip ()) 

def load_gyre_input_template (template_file=None) :
  """
  Load a GYRE input template file and return
  it as a list of strings (one element for 
  each line).

  Parameters
  ----------
  template_file : str or Path object
    Template file to load as a template. If ``None``,
    the ``persephone`` default template will be loaded. 

  Returns
  -------
  List
    The template as a list of strings (one list element per line).
  """
  if template_file is None :
    _context_manager = importlib.resources.path (persephone.grids.templates,
                                                 "default_gyre.in")
  else :
    _context_manager = pathlib.Path (template_file)
  with _context_manager as path : 
    f = open (path, "r")
    template = [line.rstrip () for line in f]
    f.close ()
  return template

def set_default_gyre_namelist (parameters=None,
                               filename="profile.data.GYRE",
                               add_details=False) :
  """
  Set default values for parameter dictionary
  to build GYRE input namelist. The ``filename``
  file is the MESA output with the ``.GYRE``
  extension.

  Parameters
  ----------
  parameters : dict
    Dictionary of parameters to include in the GYRE input file.

  filename : str or Path object
    Name of the ``.data.GYRE`` MESA-generated file to use for the
    GYRE run.

  add_details : bool
    Add a GYRE details output file template if set to ``True``.

  Returns 
  -------
  dictionary
    Dictionary with the default set of parameters used by ``persephone``.
  """
  profile_name = os.path.splitext (os.path.splitext (filename)[0])[0]
  if parameters is None :
    parameters = {}
  # Initialising subdictionaries 
  parameters.setdefault ("model", {})
  parameters.setdefault ("ad_output", {})
  # Creating variable for dictionaries
  model = parameters["model"]
  ad_output = parameters["ad_output"]

  model.setdefault ("file", "'{}'".format (filename))
  ad_output.setdefault ("summary_file", "'{}_gyre_summary.h5'".format (profile_name))
  if add_details :
    ad_output.setdefault ("detail_template", "'{}_details/detail.n%n.l%l.m%m.h5'".format (profile_name))
    

  return parameters

def make_gyre_input (gyre_profile_name, parameters=None, filename=None,
                     template_file=None, add_details=False) :
  """
  Make the inlist file for the model using a default
  parameter dictionary or the parameter dictionary 
  provided by the user.
  """
  parameters = set_default_gyre_namelist (parameters, gyre_profile_name,
                                          add_details=add_details)

  template = load_gyre_input_template (template_file=template_file)
  for elt in parameters.items () :
    template = insert_namelist (template, elt[0],
                                elt[1])
  if filename is not None :
    save_template (filename, template)
  return template

def run_gyre_individual (logs_dir, gyre_in, verbose=True) :
  """
  Run GYRE for selected input file ``gyre_in`` in directory
  ``logs_dir``.
  """
  if verbose :
    print ("Running GYRE with input {} at {}.".format (gyre_in, logs_dir))
  gyre_dir = get_gyre_dir ()
  with open (os.path.join (logs_dir, 
             "{}.out".format(os.path.splitext(gyre_in)[0])), "w") as stdout :
    subprocess.run ("{}/bin/gyre {}".format (gyre_dir, gyre_in), shell=True, 
                    cwd=logs_dir,
                    stdout=stdout,
                    )
    stdout.close ()

def analyse_gyre (star_dir, run=False, template_file=None,
                  parameters=None, verbose=True, add_details=False, 
                  rerun=False) :
  """
  Run GYRE for the profiles in the LOGS directory of a MESA
  work directory. 

  Parameters
  ---------- 

  star_dir : str or Path object
    MESA model directory.
  
  run : bool
    Whether to run GYRE or to create only the input files. Optional,
    default ``False``.

  template_file : dict
    Template GYRE input file to replace the one used by default by
    ``persephone``. Optional, default ``None``

  parameters : dict
    Dictionary of parameters to add to the GYRE input file.
    Optional, default ``None``.

  verbose : bool
    Output verbosity.

  add_details : bool
    Add a GYRE details output file template if set to ``True``
    and create ``details`` output directories together with the GYRE
    input files.

  rerun : bool
    If set to ``True``, GYRE will be rerun in directories
    where it has already been run.
    Optional, default ``False``.
  """
  # Collecting .GYRE files 
  status = read_status_dir (star_dir, attribute="run_gyre_done")
  if status and not rerun :
    if verbose :
      print ("GYRE has already been run for profiles in this directory, skipping.") 
    return
  if verbose :
    print ("Creating GYRE inputs for profiles in directory {}.".format (os.path.join (star_dir)))
  list_files = glob.glob (os.path.join (star_dir, "LOGS", "*.GYRE"))
  list_files.sort ()
  for gyre_profile_name in list_files :
    profile_name = os.path.splitext (os.path.splitext (gyre_profile_name)[0])[0]
    gyre_in_filename = "{}_gyre.in".format (profile_name)
    if add_details :
      details_dir = "{}_details".format (profile_name)
      if not os.path.exists (details_dir) :
        os.mkdir (details_dir)
    make_gyre_input (os.path.basename (gyre_profile_name), 
                     parameters=parameters, 
                     filename=gyre_in_filename,
                     template_file=template_file,
                     add_details=add_details) 
    if run :
      if verbose :
        print ("Running GYRE for profiles in directory {}.".format (os.path.join (star_dir)))
      run_gyre_individual (os.path.split (gyre_in_filename)[0], 
                os.path.split (gyre_in_filename)[1], 
                verbose=verbose)
      set_status_dir (star_dir, attribute="run_gyre_done")

def _analyse_grid_gyre_wrapper (star_dir, template_file=None, parameters=None,
                                add_details=False, rerun=False, verbose=False) :
  """
  Convenience wrapper for parallelisation.
  """
  if check_metadata (star_dir) :
    status = read_status_dir (star_dir,
                              attribute="run_gyre_done")
    if rerun or not status :
      analyse_gyre (star_dir, run=True, template_file=template_file,
                    parameters=parameters, verbose=verbose, 
                    add_details=add_details, rerun=rerun)

def analyse_grid_gyre (grid_dir, template_file=None, parameters=None,
                       verbose=True, add_details=False, 
                       rerun=False, parallelise=False, nodes=2) :
  """
  Run GYRE for each profile in model directories. 
  Directories with `run_mesa_done`
  metadata set to ``True`` will be re-run only if ``rerun``
  is set to ``True``.

  Parameters
  ---------- 

  grid_dir : str or Path object
    Directory of the grid.

  template_file : dict
    Template GYRE input file to replace the one used by default by
    ``persephone``. Optional, default ``None``

  parameters : dict
    Dictionary of parameters to add to the GYRE input file.
    Optional, default ``None``.

  verbose : bool
    Output verbosity.

  add_details : bool
    Add a GYRE details output file template if set to ``True``
    and create ``details`` output directories together with the GYRE
    input files.

  rerun : bool
    If set to ``True``, GYRE will be rerun in directories
    where it has already been run.
    Optional, default ``False``.

  parallelise : bool 
    Whether to run the MESA and GYRE runs in parallel through 
    ``pathos.multiprocess``. Optional, default ``False``.

  nodes : int
    Number of nodes used in ``pathos.multiprocess.ProcessPool``
    when ``parallelise=True``. Optional, default ``2``.
  """
  listdir = get_listdir (grid_dir)
  if parallelise :
    if verbose :
      print ("Running GYRE in parallel with {} nodes on grid located at {}.".format (nodes, 
                                                                                 grid_dir))
    pool = ProcessPool (nodes=nodes)
    pool.map (_analyse_grid_gyre_wrapper, 
              listdir,
              [template_file] * len (listdir),
              [parameters] * len (listdir),
              [add_details] * len (listdir),
              [rerun] * len(listdir),
             )
  else :
    for star_dir in listdir :
      _analyse_grid_gyre_wrapper (star_dir, template_file=template_file, 
                                  parameters=parameters, add_details=add_details,
                                  rerun=rerun, verbose=verbose)


def get_history_data (grid_dir) :
  """
  Get history data for the models in the grid.
  
  Parameters
  ----------
  grid_dir : str or Path object
    Directory of the grid.

  Returns
  -------
  dict
    A dictionary with the model directory names as keys
    and the ``mesa_reader`` history object as elements.
  """
  listdir = os.listdir (grid_dir)
  listdir.sort ()
  history = {}
  for subdir in listdir :
    star_dir = os.path.join (grid_dir, subdir)
    if check_metadata (star_dir) :
      h = mr.MesaData(os.path.join (star_dir, "LOGS/history.data"))
      history[subdir] = h
  return history

def get_model_global_param (star_dir) :
  """
  Get model global parameters such as 
  ``initial_mass`` and ``initial_z``.
  These parameters are read from the first 
  profile files.

  Parameters
  ----------
  grid_dir : str or Path object
    Model directory.

  Returns
  -------
  dict
    Dictionary with the read parameters.
  """
  p = mr.MesaData(os.path.join (star_dir, "LOGS/profile1.data"))
  parameters = {}
  parameters["initial_mass"] = p.initial_mass
  parameters["initial_z"] = p.initial_z
  return parameters

def get_grid_global_param (grid_dir) :
  """
  Get history data for the models in the grid.
  
  Parameters
  ----------
  grid_dir : str or Path object
    Directory of the grid.

  Returns
  -------
  dictionary
    A dictionary with the model directory names as keys
    and the dictionary of parameters as elements.
  """
  listdir = os.listdir (grid_dir)
  listdir.sort ()
  grid_parameters = {}
  for subdir in listdir :
    star_dir = os.path.join (grid_dir, subdir)
    if check_metadata (star_dir) :
      model_parameters = get_model_global_param (star_dir)
      grid_parameters[subdir] = model_parameters
  return grid_parameters


def plot_evolutionary_tracks (grid_dir, diagram="Kiel",
                              min_age=None, ax=None, figsize=(6,6), 
                              colors=None, cmap="tab10", 
                              show_legend=True, kwargs_legend={}, 
                              mass_to_select=None, z_to_select=None,
                              **kwargs) :
  """
  Plot evolutionary tracks of the model of the grid.

  Parameters
  ----------
  grid_dir : str or Path object
    Directory of the grid.

  diagram : str
    Type of diagram. May be ``Kiel`` or ``HR``. Optional,
    default ``Kiel``.

  min_age : float
    Minimum age to consider for the tracks.
    Optional, default ``None``.

  figsize : tuple
    Figure size.

  colors : array-like or str
    List of colors to consider for the tracks. Must match
    the total number of tracks of the grid. 
    It is also possible to give a
    single color as a string, the tracks will all be drawn
    with the same color in this case. 
    Optional, default ``None``. If not provided, the ``cmap``
    argument will be automatically used to attribute a color
    the tracks.

  cmap : str or Path object
    Color map to use. Optional, default ``tab10``.

  show_legend : bool
    Whether to show legend or not. Optional, default ``True``.

  kwargs_legend : dict
    Keywords arguments to pass to ``matplotlib.pyplot.legend``.

  mass_to_select : array-like
    If provided, only tracks matching one of the stellar masses 
    listed in the argument will be plotted.

  z_to_select : array-like
    If provided, only tracks matching one of the metallicity listed 
    in the argument will be plotted.

  **kwargs :
    Arguments to pass to ``matplotlib.pyplot.plot``.

  Returns
  -------
  matplotlib.pyplot.figure
    The created figure.
  """
  if min_age is None :
    min_age = 0

  if diagram not in ["Kiel", "HR"] :
    raise Exception ("Unknown diagram type.")
  history = get_history_data (grid_dir)
  grid_parameters = get_grid_global_param (grid_dir)
  n_model = len (history)

  # Setting colors
  if colors is None :
    colors = plt.get_cmap (cmap)
    from_cmap = True
  else :
    from_cmap = False
    if type (colors)==str :
      colors = [colors for ii in range (n_model)]

  # Making the figure
  if ax is None :
    fig, ax = plt.subplots (1, 1, figsize=figsize)
    ax.invert_xaxis ()
    if diagram=="Kiel" :
      ax.invert_yaxis ()
  else :
    fig = ax.get_figure ()
  ax.set_xlabel (r"$T_\mathrm{eff}$ (K)")

  for ii, (key, h) in enumerate (history.items ()) : 
    if from_cmap :
      color = colors (ii / max (1, n_model-1))
    else :
      color = colors [ii // max (1, n_model-1)]
    mass, z = (grid_parameters[key]["initial_mass"],
               grid_parameters[key]["initial_z"])
    label = r"{} $\rm M_\odot$, $Z = {}$".format (mass, z)
    if mass_to_select is not None and mass not in mass_to_select :
      continue
    if z_to_select is not None and z not in z_to_select :
      continue
    cond = h.star_age>min_age
    if diagram=="Kiel" :
      ax.plot (10**h.log_Teff[cond], 
               h.log_g[cond],
               color=color, label=label,
               **kwargs)
    elif diagram=="HR" :
      ax.plot (10**h.log_Teff[cond], 
               10**h.log_L[cond], 
               color=color, label=label,
               **kwargs)

  if diagram=="Kiel" :
    ax.set_ylabel (r"$\log g$ (dex)")
  elif diagram=="HR" :
    ax.set_ylabel (r"$L$ ($\rm L_\odot$)")
  if show_legend :
    ax.legend (**kwargs_legend)

  return fig


