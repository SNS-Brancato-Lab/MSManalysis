"""
Command used to load files.
"""
# Only binary files are supported for now. Module pickle is used for loading
import pickle as pkl
from typing import Union
import os
import sys

from src.tools.types import Models, Centers, Trajectory, DTrajectory
from .errors import ConversionError

def check_models_centers(models: Models, centers: Centers):
    """
    Check the compatibility between Models and Centers.

    Parameters
    ----------
    models : Models
        List of MSMs
    centers : Centers
        Microstates of a MSM
    """
    if centers.n_centers() != models[0].n_states:
        print('Warning! The number of centers is {} but models contain {} states. Be careful and check loaded files!'.format(centers.n_centers(), models[0].n_states))

def load_file(file_name: str, type: Union[Models, Centers, Trajectory, DTrajectory], interactive_mode: bool = False) -> Union[Models, Centers, Trajectory, DTrajectory]:
    """
    Load a file from .pkl format and convert it into the specific type (Models, Centers, Trajectory, DTrajectory).

    Parameters
    ----------
    file_name : str
        Name of the file to load
    type : Union[Models, Centers, Trajectory, DTrajectory]
        Type of file to load. Choose between Models, Centers, Trajectory, or DTrajectory
    interactive_mode : bool, optional
        True if interactive mode is on, by default False

    Returns
    -------
    Union[Models, Centers, Trajectory, DTrajectory]
        The file data converted in the specified type.

    Raises
    ------
    FileNotFoundError
        The file was not found.
    
    TypeError
        The data could not be converted in the required type
    """
    # file not found
    if not os.path.exists(file_name):
        msg = '\nWarning! File {} does not exist\n.'.format(file_name)
        if interactive_mode:
            print(msg)
            return None
        else:
            raise FileNotFoundError(msg)
    else:
        print('\nLoading file {}'.format(file_name))
        with open(file_name, 'rb') as file:
            data = pkl.load(file)

        #conversion
        try:
            converted_data = type(data)
            print('{} loaded.\n'.format(file_name))
            return converted_data
        
        except ConversionError as e:
            if interactive_mode:
                print('Warning!', ConversionError(file_name))
                print(e)
                return None
            else:
                print('Warning!', ConversionError(file_name))
                raise e

def quitting():
    """
    Terminate the program.
    """
    print('Adios!')
    sys.exit()

def starting():
    """
    Some fancy printing when starting!
    """
    print("""
        ___  ___ ________  ___                  _           _     
        |  \/  |/  ___|  \/  |                 | |         (_)    
        | .  . |\ `--.| .  . | __ _ _ __   __ _| |_   _ ___ _ ___ 
        | |\/| | `--. \ |\/| |/ _` | '_ \ / _` | | | | / __| / __|
        | |  | |/\__/ / |  | | (_| | | | | (_| | | |_| \__ \ \__|
        \_|  |_/\____/\_|  |_/\__,_|_| |_|\__,_|_|\__, |___/_|___/
                                                   __/ |          
                                                  |___/ 
            
          
        by Luca S. and Luca B.
          """)
    