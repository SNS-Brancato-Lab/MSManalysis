"""
Main program execution file.
"""

from src.commands.command_parser import interactive_mode, input_file, execute_command
from src.commands.inputfile_parser import InputReader
from src.tools.basics import starting

def main():

    # starting messages
    starting()
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