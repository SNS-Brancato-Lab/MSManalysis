"""
Collection of types for this program.
"""
import numpy as np
from typing import List

from deeptime.markov.msm import MarkovStateModelCollection
from numpy import ndarray

class Models(list):
    
    def __init__(self, MSMs: List[MarkovStateModelCollection]):
        
        if not all(isinstance(MSM, MarkovStateModelCollection) for MSM in MSMs):
            raise TypeError("One or more elements are not MSM.")
        super().__init__(MSMs)

    def n_models(self):

        return len(self) 

class Centers(ndarray):

    def __new__(cls, centers_array):
        centers = np.asarray(centers_array).view(cls)
        return centers
    
    def n_centers(self)-> int:
        
        return self.shape[0]

    def dimension(self):

        return self.shape[1]

class Trajectory(list):

    def __init__(self, arrays):
        
        if not all(isinstance(arr, np.ndarray) for arr in arrays):
            raise TypeError("All elements of the Trajectory must be of type numpy.ndarray")
        super().__init__(arrays)


class DTrajectory(list):
    
    def __init__(self, arrays):
        
        if not all(isinstance(arr, np.ndarray) for arr in arrays):
            raise TypeError("All elements of the Discretized Trajectory must be of type numpy.ndarray")
        super().__init__(arrays)