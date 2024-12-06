import os, pytest
import persephone as pph

mesa_version = "r15140"

class TestInstallation :

  def test_mesa_installation (self) :
    pph.grids.get_supported_mesa_version ()
    pph.grids.get_mesa_dir ()

  def test_gyre_installation (self) :
    pph.grids.get_gyre_dir ()

class TestIndividualDir :

  @pytest.fixture(scope="class")
  def tmp_star_dir (self, tmp_path_factory) :
    star_dir = tmp_path_factory.mktemp("main_dir") / "test_star_dir" 
    return star_dir  

  def test_set_default_inlist (self) :
    pph.grids.set_default_inlist ()

  def test_make_inlist (self) :
    template = pph.grids.make_inlist ()

  def test_make_ranges (self) :
    pph.grids.make_ranges ()

  def test_load_gyre_input_template (self) :
    pph.grids.load_gyre_input_template ()

  def test_copy_mesa_work (self, tmp_star_dir) :
    pph.grids.copy_mesa_work (tmp_star_dir) 

  def test_create_mesa_datafile (self, tmp_star_dir) :
    pph.grids.create_metadata_file (tmp_star_dir)
    assert pph.grids.check_metadata (tmp_star_dir) == True
    assert pph.grids.read_status_dir (tmp_star_dir) == False
    pph.grids.set_status_dir (tmp_star_dir, attribute="run_mesa_done",
                              status=True)
    assert pph.grids.read_status_dir (tmp_star_dir) == True

  def test_compile_repository (self, tmp_star_dir) :
    pph.grids.compile_repository (tmp_star_dir, verbose=False)

class TestIndividualRun :

  @pytest.fixture(scope="class")
  def tmp_work_dir (self, tmp_path_factory) :
    main_dir = tmp_path_factory.mktemp ("work_dir") 
    star_dir = main_dir / "test_star_dir" 
    return main_dir, star_dir  

  def test_create_mesa_model (self, tmp_work_dir) :
    pph.grids.create_mesa_model (path=tmp_work_dir[0], model_dir=tmp_work_dir[1], 
                       mesa_version=mesa_version,
                       default_history="MESA", default_profile="MESA",
                       profile_columns=None, history_columns=None,
                       parameters=None, compile_mesa=True, run_mesa=True,
                       run_gyre=True, parameters_gyre=None, template_file_gyre=None,
                       verbose=False, erase_existing=False, add_details=False,
                       rerun=False)

  def test_profiles (self, tmp_work_dir) :
    list_profiles = pph.grids.get_list_profiles (tmp_work_dir[1])
    p = pph.grids.get_profile (list_profiles[1])
    pph.grids.get_profile_model_number (tmp_work_dir[1])

class TestGrid :

  @pytest.fixture(scope="class")
  def tmp_grid_dir (self, tmp_path_factory) :
    grid_dir = tmp_path_factory.mktemp ("test_grid") 
    return grid_dir  

  def test_create_grid (self, tmp_grid_dir) :
    pph.grids.create_grid (tmp_grid_dir, mesa_version=mesa_version,  
                           default_history="MESA", default_profile="MESA",
                           z_min=0.0134, mstar_max=1.1,
                           compile_mesa=False, verbose=False)
  
  def test_compile_grid (self, tmp_grid_dir) :
    pph.grids.compile_grid (tmp_grid_dir, verbose=False)
  
  def test_run_grid (self, tmp_grid_dir) :
    pph.grids.run_grid (tmp_grid_dir, verbose=False,
                        parallelise=True, nodes=2)

  def test_run_gyre (self, tmp_grid_dir) :
    pph.grids.analyse_grid_gyre (tmp_grid_dir, verbose=False,
                                 parallelise=True, nodes=2)

  def test_get_param (self, tmp_grid_dir) :
    pph.grids.get_grid_global_param (tmp_grid_dir)
  
  def test_plot_grid (self, tmp_grid_dir) :
    fig = pph.grids.plot_evolutionary_tracks (tmp_grid_dir, diagram="Kiel", figsize=(8,6),
                                              lw=2, min_age=1e8,
                                              kwargs_legend={"fontsize":14})

  def test_modelling (self, tmp_grid_dir) :
    history = pph.grids.get_history_data (tmp_grid_dir)
    observable_names = ["log_Teff", "log_g"]
    observables = [6500, 4.2]
    err_observables = [75, 0.1]
    pph.grids.check_observables (history, observable_names)
    model_id, model_number, chi_square = pph.grids.compute_chi_square_grid (history, observables,
                                                                            observable_names, 
                                                                            err_observables=err_observables)
