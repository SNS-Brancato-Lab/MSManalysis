"""
Available commands
"""
import sys

# import the main analysis object
from src.MarkovStates import System

MSM = System()

def center_info(args):
    """
    Print information about loaded centers.
    """

    MSM.center_infos()

def ck_test(args):
    """
    Perform Chapman-Kolmogorov test.
    """

    n_macrostate = args.n
    MSM.ck_test(n_sets=n_macrostate)

def kinetics(args):
    """
    Compute kinetic analysis between two macrostates.
    """

    macrostate_A = args.A
    macrostate_B = args.B

    MSM.compute_TPT_kinetics(macrostate_A, macrostate_B)

def load_centers(args):
    """
    Load center file.
    """

    center_file = args.file
    MSM.load_centers(file_name=center_file)

def load_models(args):
    """
    Load model file.
    """

    model_file = args.file
    MSM.load_models(file_name=model_file)

def mfpt(args):
    """
    Compute the mean first passage time between two microstates.
    """

    state_A = args.A
    state_B = args.B

    MSM.compute_mfpt(state_A, state_B)

def pcca_assigments(args):
    """
    Perform PCCA+ analysis on the selected MSM.
    """

    n_state = args.n
    MSM.pcca_compute_assignements(n_states=n_state)

def plot_its(args):
    """
    Plot the implied timescale of the loaded models.
    """

    n_its = args.n_its
    MSM.plot_its(n_its)
    
def quit(args):
    """
    Terminate the program.
    """

    print('Goodbye!')
    sys.exit()

def select_model(args):
    """
    Select the MSM to analyze by the lagtime.
    """

    lagtime = args.lagtime
    MSM.select_model(lagtime)

def timestep(args):
    """
    Set and/or print the timestep (in ns).
    """

    if args.timestep is not None:
        MSM.timestep_ns = args.timestep
    
    print('\nTimestep is {:.2e} ns.'.format(MSM.timestep_ns))
