"""
Main module for the MSM analysis
"""
import numpy as np
from typing import Optional, List

from itertools import combinations

from .tools import load_file
from .tools import get_center_infos, check_models_centers
from .tools import Models, Centers, Trajectory, DTrajectory
from .tools import MissingAttribute
from src.analysis import its_plot, choose_model, ck_testing, score_analysis, pcca_assign_centers, \
                            TPTkinetic_analysis, trajectory_plot, dtraj_plotting, mfpt

class System:
    """
    Class containing all the main ingredients for the MSM analysis.
    """

    def __init__(self, models: Optional[Models] = None, centers: Optional[Centers] = None,
                 dtraj: Optional[Trajectory] = None, traj: Optional[Trajectory] = None):
        """
        Initialize the main object for MSM analysis

        Parameters
        ----------
        models : Optional[Models], optional
            List of MSMs to analyze, by default None
        centers : Optional[Centers], optional
            Microctate used to generate the MSMs, by default None
        dtraj : Optional[Trajectory], optional
            Discretized trajectory used to compute MSMs, by default None
        traj : Optional[Trajectory], optional
            Trajectory used to compute MSMs, by default None
        """

        self.models = models
        self.centers = centers
        self.dtraj = dtraj
        self.traj = traj

        self._test_model = None
        self._assignements = None
        self._timestep_ns = 1e-3  # 1 ps

        # interactive mode
        self._interactive_mode = False


    @property
    def interactive_mode(self) -> bool:
        """
        True if the interactive mode is on.

        Returns
        -------
        bool
            True if the ineractive mode is on
        """
        return self._interactive_mode
    @interactive_mode.setter
    def interactive_mode(self, status: bool):
        """
        Set the status of the interactive mode.

        Parameters
        ----------
        status : bool
            The status of the interactive mode
        """
        self._interactive_mode = status

    # check if the main ingredients exist or are correct           
    @property
    def centers_exist(self):
        """
        True if centers exist.
        """      
        return True if type(self.centers) is Centers else False
    
    @property
    def dtraj_exist(self):
        """
        True if discretized trajectory exists.
        """      
        return True if type(self.dtraj) is DTrajectory else False

    @property
    def models_exist(self):
        """
        True if models exist.
        """    
        return True if type(self.models) is Models else False
    
    @property
    def traj_exist(self):    
        """
        True if trajectory exists.
        """
        return True if type(self.traj) is Trajectory  else False
    
    
    # number of centers:
    @property
    def n_centers(self) -> int:
        """
        Number of loaded centers.

        Returns
        -------
        int
            Number of loaded centers
        """

        if self.centers_exist:
            return self.centers.n_centers()
        else:
            return 0

    # timestep
    @property
    def timestep_ns(self)-> float:
        """
        The timestep in ns.

        Returns
        -------
        float
            Timestep in ns
        """
        return self._timestep_ns

    @timestep_ns.setter
    def timestep_ns(self, timestep: float):
        """
        Set a new timestep (in ns).

        Parameters
        ----------
        timestep : float
            New timestep (in ns)
        """
        self._timestep_ns = timestep
    
    
    # info methods
    def center_infos(self):
        """
        Print the number of microstate used for the MSM analsysis.
        """
        if self.centers_exist:
            return get_center_infos(self.centers)
        else:
            print('No centers to analyze.')

    # ck_test method
    def ck_test(self, n_sets: int = 2):
        """
        Perform the Chapman-Kolmogorov test.

        Parameters
        ----------
        n_sets : int, optional
            Number of macrostates to test, by default 2

        Raises
        ------
        MissingAttribute
            Raised if no test MSM is selected
        """
        if self._test_model is not None:
            print('\nPerforming Chapman-Kolmogorov test with {} metastable sets.'.format(n_sets))
            ck_testing(self.models, self._test_model, n_sets)
        else:
            msg = '\nNo test MSM is selected. Please select a MSM!\n'
            if self.interactive_mode:
                print('Warning!', msg)
            else:
                raise MissingAttribute(message = msg)

    # compute mfpt
    def compute_mfpt(self, microstate_A: int, microstate_B: int):
        """
        Compute mean fist passage time (in ns) and transition events in 1us between two microstate of a MSM.

        Parameters
        ----------
        microstate_A : int
            Starting microstate
        microstate_B : int
            Target microstate

        Raises
        ------
        MissingAttribute
            Raised if no test MSM is selected
        """

        if self._test_model != None:
            print('\nUsing timestep unit {:.2e} ns'.format(self._lagtime*self.timestep_ns))
            mfpt(self._test_model, microstate_A, microstate_B, self._lagtime*self.timestep_ns)
        else:
            msg = '\nNo test MSM is selected. Please select a MSM!\n'
            if self.interactive_mode:
                print('Warning!', msg)
            else:
                raise MissingAttribute(message = msg)
    
    def compute_TPT_kinetics(self, state_A: int, state_B: int):
        """
        Compute mfpt(s) (in ns) and event rates in 1us following TPT between PCCA+ assigned states from a MSM model.
        If no PCCA+ has been performed, single microstates will be used.

        Parameters
        ----------
        state_A : int
            Starting macrostate (or microstate)
        state_B : int
            Target macrostate (or microstate)
        """

        print('\nCompute TPT kinetics!')
        print('Using lagtime {:.2e} ns'.format(self._lagtime*self.timestep_ns))
        # check for state assignement
        if self.assignements == None:
            print('\nNo PCCA+ assigments found! Continuing with centers.')
            assigments = [[i] for i in range(len(self.centers))] # fake assigments           
            
            print('\n Computing transitions between microstate {} and {}'.format(state_A, state_B))                        
            TPTkinetic_analysis(self._test_model, state_A, state_B, assigments, self._lagtime*self.timestep_ns)
        
        else:
            print('Found {} PCCA+ assigments.'.format(len(self.assignements)))        
            
            print('\n Computing transitions between microstate {} and {}'.format(state_A, state_B))
            TPTkinetic_analysis(self._test_model, state_A, state_B, self.assignements, self._lagtime*self.timestep_ns)

    # load methods
    def load_centers(self, file_name: str):
        """
        Load centers from a file.

        Parameters
        ----------
        file_name : str
            Center filename
        """

        print('\nLoading Centers')
        self.centers = load_file(file_name, Centers, interactive_mode=self.interactive_mode)
        if self.centers_exist:
            self.center_infos()

            # check compatibility with models
            if self.models_exist:
                check_models_centers(self.models, self.centers)


    def load_dtraj(self, file_name: str):
        """
        Load discretized trajectory from a file.

        Parameters
        ----------
        file_name : str
            Discretized trajectory filename
        """
        print('\nLoading Discretized Trajectory!')
        self.dtraj = load_file(file_name, DTrajectory, interactive_mode=self.interactive_mode)
            

    def load_models(self, file_name: str):
        """
        Load models from a file. If centers are not provided, a default set of centers will be generated as the number of states present in the models.

        Parameters
        ----------
        file_name : str
            Models filename
        """
        print('\nLoading Models')
        self.models = load_file(file_name, Models, interactive_mode=self.interactive_mode)

        # reset test model
        if self._test_model != None:
            self._test_model = None
                    
        # generate default centers or check model compatibility
        if not self.centers_exist:
            self.centers = Centers(np.arange(0, self.models[0].n_states).reshape(-1, 1))
            print(self.centers)
        else:
            check_models_centers(self.models, self.centers)
   
    def load_traj(self, file_name: str):
        """
        Load trajectory from a file.

        Parameters
        ----------
        file_name : str
            Trajectory filename
        """
        print('\nLoading Trajectory!')
        self.traj = load_file(file_name, Trajectory, interactive_mode=self.interactive_mode)

    # pcca assignements method
    def pcca_compute_assignements(self, n_states:int = 2):
        """
        Perform pcca assignements on the test model
        """

        if self._test_model is not None:
            print('Doing PCCA with {} metastable states'.format(n_states))
            self.assignements = pcca_assign_centers(self._test_model, self.centers, n_states)

        else:
            msg = '\nNo test MSM is selected. Please select a MSM!\n'
            if self.interactive_mode:
                print('Warning!', msg)
            else:
                raise MissingAttribute(message = msg)

    # plot its method
    def plot_its(self, n_its: int = 1):
        """
        Plot the implied timescale test.

        Parameters
        ----------
        n_its : int, optional
            Number of eigenvalues to plot, by default 1

        Raises
        ------
        MissingAttribute
            Raised if Models are not loaded
        """

        if self.models_exist:
            print('\nPlotting implied time scales!')
            its_plot(self.models, n_its)
        else:
            msg = '\nModels are not loaded. Please load a model file!\n'
            if self.interactive_mode:
                print('Warning!', msg)
            else:
                raise MissingAttribute(message = msg)

    # selection model method
    def select_model(self, lagtime: int):
        """
        Select a MSM based on a chosen lagtime (in step units). If the chosen lagtime is not present, the MSM with the closest lagtime will be selected.

        Parameters
        ----------
        lagtime : int
            The choosen lagime (in step units)
        Raises
        ------
        MissingAttribute
            Raised if Models are not loaded
        """
        if self.models_exist:
            selected_model = choose_model(self.models, lagtime)
            self._test_model = selected_model
            self._lagtime = selected_model.lagtime
        else:
            msg = '\nModels are not loaded. Please load a model file!\n'
            if self.interactive_mode:
                print('Warning!', msg)
            else:
                raise MissingAttribute(message = msg)

    # compute mfpt
    def compute_mfpt(self, microstate_A: int, microstate_B: int):
        """
        Compute mean fist passage time (in ns) and transition events in 1us between two microstate of a MSM.

        Parameters
        ----------
        microstate_A : int
            Starting microstate
        microstate_B : int
            Target microstate

        Raises
        ------
        MissingAttribute
            Raised if no test MSM is selected
        """

        if self._test_model != None:
            print('\nUsing timestep unit {:.2e} ns'.format(self._lagtime*self.timestep_ns))
            mfpt(self._test_model, microstate_A, microstate_B, self._lagtime*self.timestep_ns)
        else:
            msg = '\nNo test MSM is selected. Please select a MSM!\n'
            if self.interactive_mode:
                print('Warning!', msg)
            else:
                raise MissingAttribute(message = msg)

    # assignements
    def pcca_compute_assignements(self, n_states:int = 2):
        """
        Perform pcca assignements on the test model
        """

        if self._test_model is not None:
            print('Doing PCCA with {} metastable states'.format(n_states))
            self.assignements = pcca_assign_centers(self._test_model, self.centers, n_states, interactive_mode=self.interactive_mode)

        else:
            msg = '\nNo test MSM is selected. Please select a MSM!\n'
            if self.interactive_mode:
                print('Warning!', msg)
            else:
                raise MissingAttribute(message = msg)
    
    # remove assigments
    def clear_pcca(self):
        """
        Remove previous pcca assigments.
        """
        if self.assignements != None:
            self.assignements = None
            print('PCCA+ assigments removed!')







    #################### WORK IN PROGRESS

    # compute score
    def score(self, method: str = 'E'):
        """
        Compute score of the test model.

        Arguments:
        ----------
            method (str, default='E'): method used to compute the score
        """

        if self.dtraj_exist and self._test_model != None:
            score = score_analysis(self._test_model, self.dtraj, method)

            print('Model score: {:.2f}'.format(score))

        else:
            print('Missing dtraj or test_model.')

    # plotting PCCA assigments or discretized trajectory
    def plot_traj(self, bin: int = 100):
        """
        """

        if (self.traj_exist and self.dtraj_exist) and self.assignements != None:
            trajectory_plot(self.traj, self.dtraj, self._test_model, self.assignements)
        else:
            print('Select a traj, a dtraj and a model.')

    def plot_dtraj(self, bin: int = 100):
        """
        """
        if self.dtraj_exist and self.traj_exist:
            dtraj_plotting(self.traj, self.dtraj)
        else:
            print('Select a traj and a dtraj')