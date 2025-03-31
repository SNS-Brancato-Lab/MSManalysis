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
    headers = ['Microstates'] + ['CV{}'.format(i+1) for i in range(centers.dimension())]
    for i in range(centers.n_centers()):
        row = []
        state = 'Microstate {}'.format(i)
        cvs = ['{:.3f}'.format(cv) for cv in centers[i, :]]
        row.append(state)
        tab.append(row + cvs)
    
    # printing infos
    print('\n### Microstate Info: ###')
    print('\nNumber of microstates: {}'.format(centers.n_centers()))
    print('Microstate dimension: {}\n'.format(centers.dimension()))
    print(tabulate(tab, headers=headers))