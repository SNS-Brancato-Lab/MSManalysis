"""
Collection of types for this program.
"""
import numpy as np

from deeptime.markov.msm import MarkovStateModelCollection
from numpy import ndarray

class Models(list[MarkovStateModelCollection]):
    pass

class Centers(ndarray):
    def __new__(cls, centers_array):
        centers = np.asarray(centers_array).view(cls)
        return centers

class DTrajectory(list[ndarray[int]]):
    pass

class Trajectory(list[ndarray]):
    pass