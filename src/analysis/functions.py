"""
Useful functions for MSM analysis
"""
from src.tools import Models, Centers, DTrajectory, Trajectory

from deeptime.plots import plot_implied_timescales, plot_ck_test
from deeptime.util.validation import implied_timescales
from deeptime.markov.msm import MarkovStateModelCollection

import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.lines import Line2D

import numpy as np

from typing import List, Optional

from tabulate import tabulate

# plotting implied time scale
def its_plot(models: Models, n_its: int):
    """
    Plot the implied timescale test.

    Parameters
    ----------
    models : Models
        Collection of MSMs at different lagtime on wich the implied timescale test is performed
    n_its : int
        Number of eigenvalue to plot
    """

    # creating its object
    its_data = implied_timescales(models)

    # check for max number of process:
    if n_its > its_data.max_n_processes:
        print(f'Warning! Max num. of processes is {its_data.max_n_processes}!') 
        n_its = its_data.max_n_processes
    # plot setup
    _, ax = plt.subplots(1, 1)

    plot_implied_timescales(its_data, n_its=n_its, ax=ax)
    ax.set_yscale('log')
    ax.set_title('Implied Timescales')
    ax.set_xlabel('Lagtime (steps)')
    ax.set_ylabel('Timescale (steps)')
    plt.show()

# model selections
def choose_model(models: Models, lagtime: int) -> MarkovStateModelCollection:
    """
    Select a MSM from a list of MSMs based on a given lagtime (in step units).

    Parameters
    ----------
    models : Models
        List of MSMs
    lagtime : int
        The chosen lagtime (in step units)

    Returns
    -------
    MarkovStateModelCollection
        The selected MSM
    """

    # creating its object
    its_data = implied_timescales(models).lagtimes

    # its parameters

    index = np.abs(its_data-lagtime).argmin()
    selected_model = models[index]
    print('Lagtime chosen is {}.'.format(lagtime))
    print('Selecting model number {} with lagtime {}.'.format(index, its_data[index]))

    return selected_model

# Chapman-Kolmogorov test
def ck_testing(models: Models, test_model: MarkovStateModelCollection, n_sets:int):
    """
    Perfom Chapman-Kolmogorov test on a selected MSM.

    Parameters
    ----------
    models : Models
        List of MSMs from wich the MSM was selected 
    test_model : MarkovStateModelCollection
        The selected MSM
    n_sets : int
        Number of macrostate to test
    """
    
    ck_test = test_model.ck_test(models, n_metastable_sets=n_sets)
    grid = plot_ck_test(ck_test, legend=False)

    # test the model stored before the one chosen
    index = models.index(test_model)
    if index == 0:
        test_model2 = models[index+1]
    else:
        test_model2 = models[index-1]

    ck_test = test_model2.ck_test(models, n_metastable_sets=n_sets)
    plot_ck_test(ck_test, legend=True, grid=grid)
    plt.show()


def mfpt(test_model: MarkovStateModelCollection, state_A: int, state_B: int, ts_units: float):
    """
    Compute the mean first passage time (in ns) and the rates of transition events in 1us between two microstates.

    Parameters
    ----------
    test_model : MarkovStateModelCollection
        The selected MSM
    state_A : int
        Starting microstate
    state_B : int
        Target microstate
    ts_units : float
        Conversion unit for MSM lagtime and timestep (usually lagtime*timestep) 
    """

    # forward mfpt
    fw_mfpt = test_model.mfpt(state_A, state_B)
    fc = 1e3/(fw_mfpt*ts_units)

    print(
        f'MFPT between microstate {state_A} --> microstate {state_B} is '
        f'{fw_mfpt*ts_units:.2f} ns \n'


        f' k center {state_A}--> center {state_B} is '
        f'{fc:.2f} events/us'
        )
    
    # backward mfpt
    bc_mfpt = test_model.mfpt(state_B, state_A)
    bc = 1e3/(bc_mfpt*ts_units)

    print(
        f'MFPT between microstate {state_B} --> microstate {state_A} is '
        f'{bc_mfpt*ts_units:.2f} ns \n'


        f' k center {state_B}--> center {state_A} is '
        f'{bc:.2f} events/us'
        )
    
# pcca assignements
def pcca_assign_centers(test_model: MarkovStateModelCollection, centers: Centers, n_states: int, interactive_mode: bool = False) -> List[List[int]]:
    """
    Perform PCCA+ on a MSM.

    Parameters
    ----------
    test_model : MarkovStateModelCollection
        MSM to analyze
    centers : Centers
        Microstates of the MSM
    n_states : int
        Number of macrostate for the PCCA+
    interactive_moode : bool
        True if interactive mode in on, default is False

    Returns
    -------
    List[List[int]]
        List of ordered MSM microstates based on the PCCA+ assigments

    Raises
    ------
    ValueError
        Raised if the number of macrostates is higher than the number of MSM eigenvalues.
    """

    if n_states > test_model.n_eigenvalues+1:
        msg = f'Eigenvalues of the selected MSM are {test_model.n_eigenvalues}. Cannot do PCCA with {n_states}!'
        if interactive_mode:
            print(msg)
        else:
            raise ValueError(msg)
    
    pcca = test_model.pcca(n_states) 
    pcsp = pcca.coarse_grained_stationary_probability
    
    print('\nPCCA analysis.')
    unique_ass = np.unique(pcca.assignments)
    n_unique_ass = len(unique_ass)
    print('PCCA found {} unique assignemets:'.format(n_unique_ass))
    ordered_states = []
    
    for i in range(n_unique_ass):
    
        print('Assigned macrostate {} with a stationary probability of {}'.format(i, pcsp[i]))
        ind = np.where(pcca.assignments == i)[0]
        ordered_states.append(ind)
        
        tab = []
        for j in ind:
            row = []
            state = 'Microstate {}'.format(j)
            cvs = ['{:.2f}'.format(cv) for cv in centers[j, :]]
            row.append(state)
            tab.append(row + cvs)

        print('State {}:'.format(i))
        print(tabulate(tab))
        print('\n')

    return ordered_states

def TPTkinetic_analysis(test_model: MarkovStateModelCollection, state_A: int, state_B: int, assignements: List[List[int]], ts_units: float):
    """
    Estract mfpt(s) following the TPT for transtition between two states.

    Arguments:
    ----------
        test_model (MarkovStateModelCollection): MSM to analyze
        assignemets (List[List[int]]): list of ordered microstates from pcca
        states (List[int]): list of macrostates for the transition analysis
        lagtime (int): lagtime of the selected MSM in ns 
    """

    # forward kinetics A -> B
    fflux = test_model.reactive_flux(assignements[state_A],
                                    assignements[state_B])

    _, ftpt = fflux.coarse_grain(assignements)

    fc = (1e9/ts_units)*(ftpt.rate)

    print(
        f'\nMFPT between assigned ms {state_A} --> {state_B} is '
        f'{ftpt.mfpt*ts_units:.2f} ns \n'


        f' k assigned ms {state_A}--> {state_B} is '
        f'{fc:.2e} s^-1'
        )
    
    # backward kinetics B -> A
    bflux = test_model.reactive_flux(assignements[state_B],
                                    assignements[state_A])

    _ , btpt = bflux.coarse_grain(assignements)

    bc = (1e9/ts_units)*btpt.rate
    print(
            f'MFPT between assigned ms {state_B} --> {state_A} is'
            f' {btpt.mfpt*ts_units:.2f} ns \n'

            f' k assigned ms {state_B}--> {state_A} is '
            f'{bc:.2e} s^-1'
            )


#############WORK IN PROGRESS############

# score analysis: still to improve
def score_analysis(test_model: MarkovStateModelCollection, dtraj: Trajectory, method: str = 'E') -> float:
    """
    Perform score analysis on a MSM.

    Attributes:
    -----------
        test_model (MarkovStateModelCollection): MSM to analyze
        dtraj (Trajectory): discretized trajectory used for the MSM
        method (str, default='E'): method used to compute the score

    Returns:
    --------
        score (float): score of the model
    """

    score = test_model.score(dtrajs=dtraj, r="E")
    
    return score

# plotting functions: still to improve

def trajectory_plot(traj: Trajectory, dtraj: Trajectory, test_model: MarkovStateModelCollection, assigments: list):
    """
    """
    n_states = len(assigments)
    pcca = test_model.pcca(n_states)

    ass = np.concatenate(dtraj, axis=0)
    traj_concat = np.concatenate(traj, axis=0)

    fig, axes = plt.subplots(n_states, 1, figsize=(15, 10))
    axes = axes.ravel()
    for i in range(len(axes)):
        ax = axes[i]
        ax.set_title(f"Metastable set {i+1} probabilities")
        ax.scatter(traj_concat[::100], traj_concat[::100],
                   c=pcca.memberships[ass[::100], i], cmap=plt.cm.Reds)
    norm = mpl.colors.Normalize(vmin=0, vmax=1)
    fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=plt.cm.Reds),
                 ax=axes, shrink=.8)
    plt.show()

def dtraj_plotting(traj: Trajectory, dtraj: Trajectory):
    """
    """

    colors = ['red', 'blue', 'green', 'yellow', 'pink', 'purple']

    ass = np.concatenate(dtraj[:][::100], axis=0)
    traj_concat = np.concatenate(traj[::100], axis=0)

    microstates = np.unique(ass)

    # Scatter plot
    plt.figure(figsize=(15, 10))
    for i in microstates:
        mask = ass == i
        plt.scatter(traj_concat[mask, 0], traj_concat[mask, 1], color=colors[i], label=f'Microstate {i}')

    plt.xlabel('CV')
    plt.title('Dtraj assigments')
    plt.legend()
    plt.show()
    
def state_plotting(test_model: MarkovStateModelCollection, assignements: List[List[int]], centers: Centers, lagtime: int, timestep: float):
    """
    """

    # energy in kJ/mol
    RT = 2.479
    # time in ns
    ns_unit = timestep*lagtime

    # find each macrostate pcca stationary prob.
    n_states = len(assignements)

    pcca = test_model.pcca(n_states) 
    pcsp = pcca.coarse_grained_stationary_probability

    #energy reference (state with max. probability is taken to have energy 0)
    ref_en = -RT*np.log(np.max(pcsp))
    en = -RT*np.log(pcsp) - ref_en

    if centers.shape[1] >= 2:
        ax = plt.subplot(projection='3d')
    else:
        ax = plt.subplot()
    # find each macrostate CV as a mean of microstate CVs
    states = np.zeros([n_states, centers.shape[1]])

    for i in range(n_states):

        mean_cv = np.mean(centers[assignements[i], :], axis=0) # only 1D plot for now!
        cv = np.round(mean_cv)
        states[i, :] = cv
        if centers.shape[1] >= 2:
            ax.plot(cv[0], cv[1], en[i], 'o', markersize=50, color='blue')
            ax.text(cv[0], cv[1], en[i], str(cv[:2].tolist()), fontsize=20, color='green', ha='center', va='center')
        else:
            ax.plot(cv[0], en[i], 'o', markersize=50, color='blue')
            ax.text(cv[0], en[i], str(int(cv)), fontsize=20, color='white', ha='center', va='center')
    
    ref_id = np.argsort(en)[0]

    if centers.shape[1] <= 1:
        #drowing arrows with mfpts
        for i in np.argsort(en)[1:]:
            ax.annotate('', xy=(states[i], en[i]),
                    xytext=(states[ref_id], en[ref_id]),
                    arrowprops=dict(arrowstyle='<->', color='black'), fontsize = 15)
        
            mid_x = (states[i] + states[ref_id])/2
            mid_y = (en[i] + en[ref_id])/2

        
            color_1 = 'green'
            color_2 = 'red'

            # forward
            fflux = test_model.reactive_flux(assignements[ref_id],
                                    assignements[i])
            _, ftpt = fflux.coarse_grain(assignements)
            mfpt_fw = f'{ftpt.mfpt*ns_unit:.2f} ns \n'

            ax.text(mid_x, mid_y, mfpt_fw, color=color_1, 
                fontsize=10, ha='left', va='top')
        
            # backward
            bflux = test_model.reactive_flux(assignements[i],
                                    assignements[ref_id])
            _ , btpt = bflux.coarse_grain(assignements)
            mfpt_bw = f' {btpt.mfpt*ns_unit:.2f} ns \n'

            ax.text(mid_x, mid_y, mfpt_bw, color=color_2, 
                fontsize=10, ha='right', va='bottom')

        # Create custom legend
        legend_elements = [
        Line2D([0], [0], color='green', label='Forward Time'),
        Line2D([0], [0], color='red', label='Backward Time')
        ]

        # Add the legend to the plot with colored labels
        ax.legend(handles= legend_elements, handlelength=0, handletextpad=0, loc='lower left',
          prop={'size': 12, 'weight': 'bold'}, frameon=False,
          labels=['Forward MFPT', 'Backward MFPT'], 
          handler_map={legend_elements[0]: mpl.legend_handler.HandlerLine2D()},
          labelcolor=['green', 'red'])

        plt.xlabel('CV')
        plt.ylabel('Energy (kJ/mol)')
    
        plt.xlim([np.min(states)-1, np.max(states)+1])
        plt.ylim([np.min(en) -5, np.max(en) + 5])
    
    plt.title('MSM analysis')
    plt.show()        

