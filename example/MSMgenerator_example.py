"""
Example of a script used to generate MSMs
"""

import numpy as np
from src import System

MSM = System()

# generate and save trajectory
dir_traj = 'path/to/dir' #here insert the path to traj directory
# generate and save trajectory
MSM.generate_traj(dir=dir_traj)

# generates MSM at different clustering and lagtimes
centers_array = np.arange(6, 20) #here insert the range of number of microstates to test
lagtimes = np.arange(100, 1000, 10) #here insert the range of lagtimes to test

for n_centers in centers_array:

    # generate and save microstate and discretized trajectory
    MSM.generate_centers_dtraj(n_centers=n_centers)

    # generate and save MSMs
    MSM.generate_model(lagtimes=lagtimes)