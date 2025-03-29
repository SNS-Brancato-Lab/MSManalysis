"""
Main module for the MSM analysis
"""
from typing import Optional, List
import os
from itertools import combinations

from src.tools.basics import load_file
from src.tools.info import get_center_infos
from src.tools.types import Models, Centers, Trajectory, DTrajectory
from src.analysis.functions import its_plot, choose_model, ck_testing, score_analysis, pcca_assign_centers, kinetic_analysis,\
                            trajectory_plot, dtraj_plotting, mfpt

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
    def models_exist(self):
        """
        True if models exist.
        """    
        return True if type(self.models) is Models else False
    
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
            
    # loading methods
    def load_models(self, file_name: str):
        """
        Load models from a file.

        Parameters
        ----------
        file_name : str
            Models filename
        """

        print('\nLoading Models')
        self.models = load_file(file_name, Models, interactive_mode=self.interactive_mode)


    def load_centers(self, file_name: str):
        """
        Load centers from a file.

        Parameters
        ----------
        file_name : str
            Center filename
        """

        print('\nLoading Centers')
        self.centers = load_file(file_name, Models, interactive_mode=self.interactive_mode)
        if self.centers_exist:
            self.center_infos()

    def load_dtraj(self, file_name: str):
        """
        Load discretized trajectory from a file.

        Parameters
        ----------
        file_name : str
            Discretized trajectory filename
        """
        if os.path.exists(file_name):
            self.dtraj = DTrajectory(load_file(file_name, kind='Discretized Trajectory'))
        else:
            print('Discretized trajectory file {} does not exist.'.format(file_name))
    
    def load_traj(self, file_name: str):
        """
        Loading Traj
        """
        if os.path.exists(file_name):
            self.traj = Trajectory(load_file(file_name, kind='Trajectory'))
        else:
            print('Trajectory {} does not exist.'.format(file_name))

    # its method
    def plot_its(self, n_its: int = 1):
        """
        Plot implied timescale.

        Arguments:
        ----------
            n_its (int, default): number of implied timescale to plot
        """

        if self.models_exist:
            print('\nPlotting implied time scales!')
            its_plot(self.models, n_its)
        else:
            print('Please load a model file!')

    # selection model method
    def select_model(self, lagtime: int):
        """
        Select a MSM based on a chosen lagtime (in step units).

        Parameters
        ----------
        lagtime : int
            The choosen lagime (in step units)
        """
        if self.models_exist:
            selected_model = choose_model(self.models, lagtime)
            self._test_model = selected_model
            self._lagtime = selected_model.lagtime

    # ck_test
    def ck_test(self, n_sets: int = 2):
        """
        Perform Chapman-Kolmogorov test.

        Arguments:
        ----------
            n_sets (int, default=2): number of metastable stets to test
        """
        if self._test_model is not None:
            print('Performing Chapman-Kolmogorov test with {} metastable sets.'.format(n_sets))
            ck_testing(self.models, self._test_model, n_sets)
        else:
            print('Select a MSM to test.')

    # compute mfpt
    def compute_mfpt(self, states: List[int]):
        """
        Compute mfpt(s) and rate constants between assigned states from a MSM model.

        Arguments:
        ----------
            states(List[int]): list of centers for the transition analysis
        """

        if self._test_model != None and self.centers_exist:
            print('Using lagtime {:.2e} ns'.format(self._lagtime*self.timestep_ns))
            mfpt(self._test_model, states, self._lagtime*self.timestep_ns)
        else:
            print('Please select a model and/or provide some centers!')

    # assignements
    def pcca_compute_assignements(self, n_states:int = 2):
        """
        Perform pcca assignements on the test model
        """

        if self._test_model != None:
            print('Doing PCCA with {} metastable states'.format(n_states))
            self.assignements = pcca_assign_centers(self._test_model, self.centers, n_states)

        else:
            print('Please select a test model!')
    
    # remove assigments
    def clear_pcca(self):
        """
        Remove previous pcca assigments.
        """
        if self.assignements != None:
            self.assignements = None
        else:
            print('No assigments found to remove!')

    def compute_transitions(self, states: Optional[List[int]] = None):
        """
        Compute mfpt(s) following TPT between pcca assigned states from a MSM model.

        Arguments:
        ----------
            states(optional, List[int], default=None): list of pcca macrostates for the transition analysis
        """

        # check for state assignement
        if self.assignements == None:
            print('\nNo pcca has been performed! Continuing with centers.')
            print('Using lagtime {:.2e} ns'.format(self._lagtime*self.timestep_ns))
            assigments = [[i] for i in range(len(self.centers))]
            if states == None:
                print('No state specified, doing all!')
                states = assigments
            pairs = list(combinations(states,2))

            for pair in pairs:
                print('\n Computing transitions between {} and {}'.format(pair[0], pair[1]))
                kinetic_analysis(self._test_model, assigments, pair, self._lagtime*self.timestep_ns)
        else:
            print('\nDoing some Kinetics!')
            print('Using lagtime {:.2e} ns'.format(self._lagtime*self.timestep_ns))
            if states == None:
                print('No state specified, doing all!')
                states = [i for i in range(len(self.assignements))]
            pairs = list(combinations(states,2))

            for pair in pairs:
                print('\n Computing transitions between {} and {}'.format(pair[0], pair[1]))
                kinetic_analysis(self._test_model, self.assignements, pair, self._lagtime*self.timestep_ns)


        

    # method to improve

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