"""
Parser for terminal commands.
"""

import argparse
import os

from commands import MSM

parser = argparse.ArgumentParser(description="MSManalysis by Luca S. and Luca B.")
parser.add_argument("-m", "--models", dest="models", help="pkl file of MSMs", default=None)
parser.add_argument("-c", "--centers", dest="centers", help="pkl file of centers", default=None)
parser.add_argument("-tr", "--traj", dest="traj", help="pkl file of trajectory", default=None)
parser.add_argument("-dtr", "--dtraj", dest="dtraj", help="pkl file of discretized trajectory", default=None)
parser.add_argument("-lt", "--lagtime", dest="bestlag", type=int, help="lagtime for the MSM selection", default=None)
parser.add_argument("-ns", "--assigments", dest="n_states", type=int, help="number of macrostates for the PCCA", default=None)
args = parser.parse_args()

models = args.models
centers = args.centers
traj = args.traj
dtraj = args.dtraj
bestlag = args.bestlag
n_states = args.n_states

if models is not None and os.path.exists(models):
    MSM.load_models(models)

if centers is not None and os.path.exists(centers):
    MSM.load_centers(centers)

if traj is not None and os.path.exists(traj):
    MSM.load_traj(traj)

if dtraj is not None and os.path.exists(dtraj):
    MSM.load_models(dtraj)    

if bestlag is not None:
    MSM.select_model(bestlag)

if n_states is not None:
    MSM.pcca_compute_assignements(n_states)