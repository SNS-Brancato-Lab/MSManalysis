"""
Collection of types for this program.
"""
from typing import List

from deeptime.markov.msm import MarkovStateModelCollection
from numpy import ndarray

Models = List[MarkovStateModelCollection]
Centers = ndarray
Trajectory = List[ndarray]
DTrajectory = List[ndarray[int]]