"""
Parser for the main program and available commands
"""

import argparse
from typing import Sequence

from .Commands import *

# command parser dictionary
commands = {}

# Main parser
main_parser = argparse.ArgumentParser(description="MSManalysis by Luca S. and Luca B.", add_help=True)
main_parser.add_argument("-i", dest="input_file", help="Input file with command instructions.", default=None, type=str, metavar='INPUT_FILE')
main_args = main_parser.parse_args()

# Main parser argument
input_file = main_args.input_file

# activate reading mode
if input_file is not None:
    print('Reading commands from {}!'.format(input_file))
    interactive_mode = False
else:
    interactive_mode = True
# set the interactive mode status for the main program
MSM.interactive_mode = interactive_mode

class MyArgumentParser(argparse.ArgumentParser):
    """
    My ArgumentParser Class for personalized error managing. 
    """

    def error(self, message):
        print('%s: error: %s\n' % (self.prog, message))
        print('')
        #self.print_help()
        if interactive_mode:
            #self.print_help()
            pass
        else:
            print('Exit due to error(s) in the execution!')
            self.exit(2)


# Command Parser
command_parser = MyArgumentParser(prog="", add_help=False, exit_on_error=False)
command_subparsers = command_parser.add_subparsers(title='Available commands', 
                                                   description='Use one of the following commands:', 
                                                   dest="command", 
                                                   help="Use 'command -h/--help' for more details.", 
                                                   required=True) 


# center_info parser
center_info_parser = command_subparsers.add_parser('center_info',
                                                   help='Print information on microstates.',
                                                   description='This command shows a table with loaded microstates and their CVs values.',
                                                   add_help=False)
center_info_parser.add_argument("-h", "--help", action='store_true', help="Show help message.")
center_info_parser.set_defaults(func=center_info)
commands['center_info'] = center_info_parser

# ck_test parser
ck_test_parser = command_subparsers.add_parser('ck_test',
                                               help='Perform Chapman-Kolmogorov analysis with a chosen number of macrostate.',
                                               description="This command perform Chapman-Kolmogorov analysis with a chosen set of macrostate.\n\
                                                A MSM must be selected before with 'select_model'.",
                                                add_help=False)
ck_test_parser.add_argument('n', metavar='N_macrostates', type=int, nargs='?', default=2, help='Number of macrostates for CK analysis. Default is 2')
ck_test_parser.add_argument("-h", "--help", action='store_true', help="Show help message.")
ck_test_parser.set_defaults(func=ck_test)
commands['ck_test'] = ck_test_parser

# kinetics parser
kinetics_parser = command_subparsers.add_parser('kinetics',
                                                help='Compute kinetic analysis between two macrostate.',
                                                description="This command computes mean first passage times (in ns) and event rates in 1us between two macrostate.\
                                                    If PCCA+ has not be performed, single microstates will be used.\n\
                                                    A MSM must be selected before with 'select_model'",
                                                    add_help=False)
kinetics_parser.add_argument('A', metavar='STATE_A', type=int, nargs='?', help='Starting macrostate id.')
kinetics_parser.add_argument('B', metavar='STATE_B', type=int, nargs='?', help='Target macrostate id.')
kinetics_parser.add_argument("-h", "--help", action='store_true', help="Show help message.")
kinetics_parser.set_defaults(func=kinetics)
commands['kinetics'] = kinetics_parser

# load_centers parser
load_centers_parser = command_subparsers.add_parser('load_centers',
                                                    help='Load MSMs microstate from a file.',
                                                    description='This command load MSM microstates from a .pkl file.',
                                                    add_help=False)
load_centers_parser.add_argument('file', metavar='CENTERS_FILE', type=str, nargs='?', help='File containing MSMs microstates')
load_centers_parser.add_argument("-h", "--help", action='store_true', help="Show help message.")
load_centers_parser.set_defaults(func=load_centers)
commands['load_centers'] = load_centers_parser

# load_models parser
load_models_parser = command_subparsers.add_parser('load_models',
                                                   help='Load MSMs from a file.',
                                                   description='This command load MSMs from a .pkl file.',
                                                   add_help=False)
load_models_parser.add_argument('file', metavar='MODELS_FILE', nargs='?', type=str, help='Models file')
load_models_parser.add_argument("-h", "--help", action='store_true', help="Show help message.")
load_models_parser.set_defaults(func=load_models)
commands['load_models'] = load_models_parser

# mfpt parser
mfpt_parser = command_subparsers.add_parser('mfpt',
                                            help='Comute mean first passage times (in ns) between two microstates.',
                                            description="This command computes mean first passage times (in ns) between two microstates.\n\
                                                A MSM must be selected before with 'select_model'",
                                                add_help=False)
mfpt_parser.add_argument('A', metavar='MICROSTATE_A', type=int, nargs='?', help='Starting center id.')
mfpt_parser.add_argument('B', metavar='MICROSTATE_B', type=int, nargs='?', help='Target center id.')
mfpt_parser.add_argument("-h", "--help", action='store_true', help="Show help message.")
mfpt_parser.set_defaults(func=mfpt)
commands['mftp'] = mfpt_parser

# pcca_assigments_parser
pcca_assigments_parser = command_subparsers.add_parser('pcca_assigments',
                                                       help='Perform PCCA+ with a chosen number of macrostates on a selected MSM.',
                                                       description="This command perform PCCA+ with a chosen number of macrostates on a selected MSM.\n\
                                                        If no number of macrostates is provided, the PCCA+ will be performed with 2 macrostates.\n\
                                                        A MSM must be selected before with 'select_model'",
                                                        add_help=False)
pcca_assigments_parser.add_argument('n', metavar='N_macrostates',type=int, default=2, nargs='?', help='Number of macrostate for PCCA+ analysis. Default is 1.')
pcca_assigments_parser.add_argument("-h", "--help", action='store_true', help="Show help message.")
pcca_assigments_parser.set_defaults(func=pcca_assigments)
commands['pcca_assigments'] = pcca_assigments_parser

# plot_its
plot_its_parser = command_subparsers.add_parser('plot_its',
                                                help='Perform and plot the implied timescale analysis of a given number of eigenvalue.',
                                                description='This program perform and plot the implied timescale analysis.\n\
                                                    If no number of eigenvalue is provided, only the first eigenvalue will be shown.',
                                                add_help=False)
plot_its_parser.add_argument('n_its', metavar='N_eigenvalues', type=int, default=1, nargs='?', help='Number of eigenvalues to plot. Default is 1.')
plot_its_parser.add_argument("-h", "--help", action='store_true', help="Show help message.")
plot_its_parser.set_defaults(func=plot_its)
commands['plot_its'] = plot_its_parser

# quit parser
quit_parser = command_subparsers.add_parser('quit',
                                            help='Terminate the program.',
                                            add_help=False)
quit_parser.add_argument("-h", "--help", action='store_true', help="Show help message.")
quit_parser.set_defaults(func=quit)
commands['quit'] = quit_parser

#select_model
select_model_parser = command_subparsers.add_parser('select_model',
                                                    help='Select the MSM to analyze choosing the lagtime (in step units).',
                                                    description='This command selects a MSM by providing a lagtime (in step units).\n\
                                                        If the provided lagtime is not present in the loaded MSMs, the MSM with the closest lagtime will be chosen.',
                                                    add_help=False)
select_model_parser.add_argument('lagtime', metavar='LAGTIME', nargs='?', type=int, help='Lagtime of the selected model (in step units)')
select_model_parser.add_argument("-h", "--help", dest='help', action='store_true', help="Show help message.")
select_model_parser.set_defaults(func=select_model)
commands['select_model'] = select_model_parser

# timestep parser
timestep_parser = command_subparsers.add_parser('timestep',
                                                help='Set the conversion unit between step units and ns.',
                                                description='This command sets the conversion unit between step units nanosecond.\
                                                    If no timestep is provided, it will print the active timestep unit conversion value.',
                                                add_help=False)
timestep_parser.add_argument('timestep', metavar='TIMESTEP', type=float, nargs='?', help='Timestep in ns.', default=None)
timestep_parser.add_argument("-h", "--help", action='store_true', help="Show help message.")
timestep_parser.set_defaults(func=timestep)
commands['timestep'] = timestep_parser

# command execution function
def execute_command(command_line: Sequence[str]):
    """
    Execute a command line.

    Parameters
    ----------
    command : Sequence[str]
        Command line to be executed
    """
    command = command_line[0]
    if command in commands.keys():
        parser = commands[command]
        args, _ = parser.parse_known_args(command_line[1:])

        if args.help:
            parser.print_help()
        else:
            args.func(args)
        
        
