"""
Functions that get and print informations
"""
from tabulate import tabulate
import numpy as np

from src.tools.types import Centers, Trajectory, Models

def get_center_infos(centers: Centers):
    """
    Print info about the loaded centers

    Arguments:
    ----------
        centers (Centers): the array of the MSM microstates
    """
    # tab creation:
    tab = []
    for i in range(centers.n_centers()):
        row = []
        state = 'Microstate {}'.format(i)
        cvs = ['{:.3f}'.format(cv) for cv in centers[i, :]]
        row.append(state)
        tab.append(row + cvs)
    
    # printing infos
    print('\n### Microstate Info: ###')
    print('Number of loaded microstates: {}'.format(centers.n_centers()))
    print('Microstate dimension: {}'.format(centers.dimension()))
    print('\nMicrostates:')
    print(tabulate(tab))