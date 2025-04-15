"""
Function used to generate MSMs ingredients: Trajectory, Centers, Discretized Trajectory, Models
"""
import os
import numpy as np

from src.tools.types import Centers, DTrajectory, Models, Trajectory

from deeptime.clustering import KMeans
from deeptime.markov import TransitionCountEstimator
from deeptime.markov.msm import MaximumLikelihoodMSM

def generate_trajectory(dir: str) -> Trajectory:
    """
    Generate a trajectory from text files in a given directory.

    Parameters
    ----------
    dir : str
        Directory of the trajectory files

    Returns
    -------
    Trajectory
        A trajectory object
    """

    # Get a list of all files in the directory
    traj_files = os.listdir(dir)

    traj = []
    # Iterate over the C files and load each one
    for f in traj_files:
        file_path = os.path.join(dir, f)
        data = np.loadtxt(file_path)
        traj.append(data)

    return Trajectory(traj)

def generate_centers_dtraj(traj: Trajectory, n_centers: int) -> tuple[Centers, DTrajectory]:
    """
    Generate microstates and discretized trajectory from a trajectory using KMeans clustering algorithm.

    Parameters
    ----------
    traj : Trajectory
        Trajectory to discretize
    n_centers : int
        Number of microstates

    Returns
    -------
    tuple[Centers, DTrajectory]
        Microstates and discretized trajectory
    """

    traj_concat = np.concatenate(traj, axis=0)

    # clustering with KMeans
    estimator = KMeans(
                        n_clusters=n_centers,
                        init_strategy='kmeans++',
                        max_iter=0,
                        n_jobs=16,
                        )
    
    # initial guess
    initial_clustering = estimator.fit_fetch(traj_concat)

    # refinement
    estimator.initial_centers = initial_clustering.cluster_centers
    estimator.max_iter = 5000
    clustering = estimator.fit_fetch(traj_concat)

    # generate microstates and discretized traj
    centers = clustering.cluster_centers.T
    dtraj = [clustering.transform(tr) for tr in traj]

    return Centers(centers), DTrajectory(dtraj)

def generate_model(dtraj: DTrajectory, lagtimes:np.ndarray[int]) -> Models:
    """
    Generate MSMs from a discretized trajectory at different lagtimes.

    Parameters
    ----------
    dtraj : DTrajectory
        Discretized trajectory
    lagtimes : np.ndarray[int]
        Array of list of lagtimes at which generate MSMs

    Returns
    -------
    Models
        List of MSMs
    """
    
    models = []
    
    for lt in lagtimes:
        tce = TransitionCountEstimator(
                                        lagtime=lt,
                                        count_mode='sliding'
                                        )
        counts = tce.fit_fetch(dtraj)
        models.append(MaximumLikelihoodMSM().fit_fetch(counts))

        return Models(models)
