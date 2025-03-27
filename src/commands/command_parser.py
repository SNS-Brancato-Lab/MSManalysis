"""
Parser for the main program and available commands
"""

import argparse
from typing import Sequence

from src.commands.commands import *

# Main parser
main_parser = argparse.ArgumentParser(description="MSManalysis by Luca S. and Luca B.", add_help=True)
main_parser.add_argument("-i", dest="input_file", help="Input file with command instructions.", default=None, type=str, metavar='input.in')
main_args = main_parser.parse_args()

# Main parser argument
input_file = main_args.input_file

# activate reading mode
if input_file is not None:
    print('Reading commands from {}!'.format(input_file))
    interactive_mode_status = False
else:
    interactive_mode_status = True

# Command Parser
command_parser = argparse.ArgumentParser(prog="", add_help=False)
command_subparsers = command_parser.add_subparsers(dest="command", required=True) 

# center_info parser
center_info_parser = command_subparsers.add_parser('center_info')
center_info_parser.set_defaults(func=center_info)

# ck_test parser
ck_test_parser = command_subparsers.add_parser('ck_test')
ck_test_parser.add_argument('n', type=int, default=2, help='Number of macrostates for CK analysis. Default is 2')
ck_test_parser.set_defaults(func=ck_test)

# kinetics parser
kinetics_parser = command_subparsers.add_parser('kinetics')
kinetics_parser.add_argument('A', type=int, help='Starting macrostate id.')
kinetics_parser.add_argument('B', type=int, help='Target macrostate id.')
kinetics_parser.set_defaults(func=kinetics)

# load_centers parser
load_centers_parser = command_subparsers.add_parser('load_centers')
load_centers_parser.add_argument('file', type=str, help='Center file')
load_centers_parser.set_defaults(func=load_centers)

# load_models parser
load_models_parser = command_subparsers.add_parser('load_models')
load_models_parser.add_argument('file', type=str, help='Models file')
load_models_parser.set_defaults(func=load_models)

# mfpt parser
mfpt_parser = command_subparsers.add_parser('mfpt')
mfpt_parser.add_argument('A', type=int, help='Starting center id.')
mfpt_parser.add_argument('B', type=int, help='Target center id.')
mfpt_parser.set_defaults(func=mfpt)

# pcca_assigments_parser
pcca_assigments_parser = command_subparsers.add_parser('pcca_assigments')
pcca_assigments_parser.add_argument('n', type=int, default=2, help='Number of macrostate for PCCA+ analysis. Default is 1.')
pcca_assigments_parser.set_defaults(func=pcca_assigments)

# plot_its
plot_its_parser = command_subparsers.add_parser('plot_its')
plot_its_parser.add_argument('n_its', type=int, default=1, help='Number of implied scale to plot. Default is 1.')
plot_its_parser.set_defaults(func=plot_its)

# quit parser
quit_parser = command_subparsers.add_parser('quit')
quit_parser.set_defaults(func=quit)

#select_model
select_model_parser = command_subparsers.add_parser('select_model')
select_model_parser.add_argument('lagtime', type=int, help='Lagtime of the selected model (in frame units)')
select_model_parser.set_defaults(func=select_model)

# timestep parser
timestep_parser = command_subparsers.add_parser('timestep')
timestep_parser.add_argument('timestep', type=float, help='Timestep in ns.', default=None)
timestep_parser.set_defaults(func=timestep)

# command execution function
def execute_command(command_line: Sequence[str]):
    """
    Execute a command line.

    Parameters
    ----------
    command : Sequence[str]
        Command line to be executed
    """
    args = command_parser.parse_args(command_line)
    args.func(args)