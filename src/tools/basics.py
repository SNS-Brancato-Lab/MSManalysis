"""
Command used to load files.
"""
# Only binary files are supported for now.
import pickle as pkl
import typing as tp
import sys

def load_file(file_name: str, kind: str):
    """
    Loads a binary file.

    Arguments:
    ----------
        file_name (str): the name of the binary file
        kind (str): content kind inside the binary file (Models, Centers, Trajectory, Discretized Trajectory)

    Returns:
    --------
        data (Any): the content of the binary file
    """

    #to add: check the existence of the file

    print('\nLoading {} from {}'.format(kind, file_name))
    with open(file_name, 'rb') as file:
        data = pkl.load(file)

    print('{} loaded.\n'.format(kind)) 
    
    return data

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
    