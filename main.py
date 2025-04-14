"""
Main program execution file.
"""
# starting MSManalysis
from src.tools import starting
starting()

from src.commands import interactive_mode, input_file
from src.commands.command_parser import execute_command
from src.commands import InputReader

def main():

    if interactive_mode:
        print('\nInteractive mode is on!\n')
        print("Type 'quit' to exit.")
    
    # interactive mode
    while interactive_mode == True:
        command_line = input("> ")
        execute_command(command_line.split())

    # input file mode
    reader = InputReader(input_file=input_file)
    reader.read_and_execute()

if __name__ == "__main__":
    main()