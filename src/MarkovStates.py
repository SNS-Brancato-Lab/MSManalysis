"""
Module for the MSM analysis
"""
from typing import Optional, List
import os

from src.tools.basics import load_file
from src.tools.info import get_center_infos
from src.tools.types import Models, Centers, Trajectory
from src.analysis.functions import its_plot, choose_model, ck_testing, score_analysis, pcca_assign_centers, kinetic_analysis,\
                            trajectory_plot, dtraj_plotting, state_plotting, mfpt
from itertools import combinations

class System:
    """
    This class contains all the main ingredients for the MSM analysis.

    Attributes:
    -----------
        models (Models): list of MSMs
        centers (Centers): microstates used to generate the MSMs
        dtraj (Trajectory): discretized trajectory used to generate the MSMs
        traj (Trajectory): trajectory used to generate the MSMs
        test_model (MarkovStateModelCollection): selected MSM to analyze

    """

    def __init__(self, models: Optional[Models] = None, centers: Optional[Centers] = None,
                 dtraj: Optional[Trajectory] = None, traj: Optional[Trajectory] = None):
        """
        Costructor for the class system:

        Arguments:
        ----------
            models (Models or None): list of MSMs
            centers (Centers or None): microstates used to generate the MSMs
            dtraj (Trajectory or None): discretized trajectory used to generate the MSMs
            traj (Trajectory or None): trajectory used to generate the MSMs
        """
        # Main attributes
        self.models = models
        self.centers = centers
        self.dtraj = dtraj
        self.traj = traj
        self.test_model = None
        self.assignements = None

        self._timestep_ns=1e-3  # 1 ps

    # existence propeties       
    @property
    def models_exist(self):
        """
        True if models exist.
        """    
        return True if self.models != None else False
    @property
    def centers_exist(self):
        """
        True if centers exist.
        """      
        return True if self.centers is not None else False
    @property
    def dtraj_exist(self):
        """
        True if discretized trajectory exists.
        """      
        return True if self.dtraj is not None else False
    @property
    def traj_exist(self):    
        """
        True if trajectory exists.
        """
        return True if self.traj is not None else False
    @property
    def assigments_exist(self):
        """
        True if assigments exist.
        """
        return True if self.assignements is not None else False
    
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
            return len(self.centers)
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
        if self.centers_exist:
            return get_center_infos(self.centers)
        else:
            print('No centers to analyze.')
            
    # loading methods
    def load_models(self, file_name: str):
        """
        Load MSMs
        """
        if os.path.exists(file_name):
            self.models = load_file(file_name, kind='Models')
        else:
            print('Models {} do not exist.'.format(file_name))

    def load_centers(self, file_name: str):
        """
        Loading Centers
        """
        if os.path.exists(file_name):
            self.centers = load_file(file_name, kind='Centers')
            self.center_infos()
        else:
            print('Centers {} do not exist.'.format(file_name))

    def load_dtraj(self, file_name: str):
        """
        Loading DTraj
        """
        if os.path.exists(file_name):
            self.dtraj = load_file(file_name, kind='Discretized Trajectory')
        else:
            print('Discretized trajectory {} does not exist.'.format(file_name))
    
    def load_traj(self, file_name: str):
        """
        Loading Traj
        """
        if os.path.exists(file_name):
            self.traj = load_file(file_name, kind='Trajectory')
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
    def select_model(self, bestlag: int):
        """
        Select the MSM to analyze.

        Attributes:
        -----------
            bestlag (int): the selected lagtime 
        """
        if self.models_exist:
            selected_model = choose_model(self.models, bestlag)
            self.test_model = selected_model
            self.lagtime = selected_model.lagtime

    # ck_test
    def ck_test(self, n_sets: int = 2):
        """
        Perform Chapman-Kolmogorov test.

        Arguments:
        ----------
            n_sets (int, default=2): number of metastable stets to test
        """
        if self.test_model != None:
            print('Performing Chapman-Kolmogorov test with {} metastable sets.'.format(n_sets))
            ck_testing(self.models, self.test_model, n_sets)
        else:
            print('Select a MSM to test.')

    # compute score
    def score(self, method: str = 'E'):
        """
        Compute score of the test model.

        Arguments:
        ----------
            method (str, default='E'): method used to compute the score
        """

        if self.dtraj_exist and self.test_model != None:
            score = score_analysis(self.test_model, self.dtraj, method)

            print('Model score: {:.2f}'.format(score))

        else:
            print('Missing dtraj or test_model.')

    # compute mfpt
    def compute_mfpt(self, states: List[int]):
        """
        Compute mfpt(s) and rate constants between assigned states from a MSM model.

        Arguments:
        ----------
            states(List[int]): list of centers for the transition analysis
        """

        if self.test_model != None and self.centers_exist:
            print('Using lagtime {:.2e} ns'.format(self.lagtime*self.timestep_ns))
            mfpt(self.test_model, states, self.lagtime*self.timestep_ns)
        else:
            print('Please select a model and/or provide some centers!')

    # assignements
    def pcca_compute_assignements(self, n_states:int = 2):
        """
        Perform pcca assignements on the test model
        """

        if self.test_model != None:
            print('Doing PCCA with {} metastable states'.format(n_states))
            self.assignements = pcca_assign_centers(self.test_model, self.centers, n_states)

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
            print('Using lagtime {:.2e} ns'.format(self.lagtime*self.timestep_ns))
            assigments = [[i] for i in range(len(self.centers))]
            if states == None:
                print('No state specified, doing all!')
                states = assigments
            pairs = list(combinations(states,2))

            for pair in pairs:
                print('\n Computing transitions between {} and {}'.format(pair[0], pair[1]))
                kinetic_analysis(self.test_model, assigments, pair, self.lagtime*self.timestep_ns)
        else:
            print('\nDoing some Kinetics!')
            print('Using lagtime {:.2e} ns'.format(self.lagtime*self.timestep_ns))
            if states == None:
                print('No state specified, doing all!')
                states = [i for i in range(len(self.assignements))]
            pairs = list(combinations(states,2))

            for pair in pairs:
                print('\n Computing transitions between {} and {}'.format(pair[0], pair[1]))
                kinetic_analysis(self.test_model, self.assignements, pair, self.lagtime*self.timestep_ns)

    def plot_traj(self, bin: int = 100):
        """
        """

        if (self.traj_exist and self.dtraj_exist) and self.assignements != None:
            trajectory_plot(self.traj, self.dtraj, self.test_model, self.assignements)
        else:
            print('Select a traj, a dtraj and a model.')

    def plot_dtraj(self, bin: int = 100):
        """
        """
        if self.dtraj_exist and self.traj_exist:
            dtraj_plotting(self.traj, self.dtraj)
        else:
            print('Select a traj and a dtraj')

    def plot_states(self):
        """
        """
        if self.assigments_exist:
            state_plotting(self.test_model, self.assignements, self.centers, self.lagtime, self.timestep_ns)

        else:
            print('Please assign some microstates!')
        