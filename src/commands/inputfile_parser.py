"""
Input module for input file parsing and execution.
"""

from .command_parser import execute_command

class InputReader:

    def __init__(self, input_file: str):

        self.input_file = input_file

    
    def read_and_execute(self):

        with open(self.input_file) as f:

            for line in f:
                
                command_line = line.split("#", 1)[0].strip() # ignore comments that start with '#'

                if command_line:
                    print('\n>', command_line)                    
                    execute_command(command_line.split())