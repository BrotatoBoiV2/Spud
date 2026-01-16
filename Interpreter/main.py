"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                Programmer: Aaron "A.J." Cassell. (@BrotatoBoi)
                        Program Name: Spud Language.
                     Description: My custom language.
                              File: main.py
                            Date: 2026/01/02
                        Version: 1.6.5-2026.01.16

===============================================================================

                    Copyright (C) 2025 BrotatoBoi
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/>

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

# ~ Import System Modules. ~ #
import sys

# ~ Import Local Modules. ~ #
from tokenizer import Tokenizer
from parser import Parser
from memory import Environment


class SpudInterpreter:
    """
    ~ The interpreter class responsible for executing the source code. ~

    Functions:
        - __init__                     : Initializes the interpreter.
        - display_usage                : Displays the usage of the interpreter.
        - read_file                    : Reads the file.
        - execute                      : Executes the file.
    """

    def __init__(self, file_path):
        """
        ~ Initialize the Interpreter. ~

        Arguments:
            - file_path       (String) : The path to the file to be executed.

        Attributes:
            - tokenizer    (Tokenizer) : The tokenizer instance.
            - parser          (Parser) : The parser instance.
            - env        (Environment) : The environment instance.
            - file_path       (String) : The path to the file to be executed.
        """

        self.tokenizer = Tokenizer()
        self.parser = Parser()
        self.env = Environment()
        self.file_path = file_path

        # ~ Check if it is a valid file extension. ~ #
        if not self.file_path.endswith(".pot"):
            err = f"Invalid file extension: '{self.file_path}'."
            raise ValueError(err + " Expected '.pot'.")

    def _read_file(self):
        """
        ~ Read the source code from the file. ~

        Returns:
            - Stirng                   : The raw source code string.
        """

        with open(self.file_path, "r", encoding="utf-8") as f:
            return f.read()

    def execute(self):
        """
        ~ Orchestrate the execution of the interpretation pipeline. ~

        1.) Tokenize the source code.
        2.) Parse the source code.
        3.) Execute the parsed code.
        """

        source_code = self._read_file()
        tokens = self.tokenizer.tokenize(source_code)
        nodes = self.parser.parse(tokens)
        
        # ~ Maybe turn into `nodes.execute()`. ~ #
        if nodes:
            for node in nodes:
                if node:
                    node.execute(self.env)

            print("")


def display_usage():
    """
    ~ Display the correct usage syntax for the interpreter. ~
    """

    print(f"Usage: python {sys.argv[0]} <file.pot> [--debug]")


if __name__ == "__main__":
    # ~ Seperate the filename from the flags. ~ #
    args = sys.argv[1:]
    debug_mode = "--debug" in args

    # ~ Isolate the filename by removing the flag. ~ #
    if debug_mode:
        args.remove("--debug")

    # ~ Check if a file path was provided and set it. ~ #
    if not args:
        display_usage()
        sys.exit(1)

    file_path = args[0]
    interpreter = SpudInterpreter(file_path)

    # ~ Execute the interpreter based on the debug setting. ~ #
    if debug_mode:
        interpreter.execute()

    else:
        try:                      # ~ Debug Mode: Displays Python Errors. ~ #
            interpreter.execute()
            sys.exit(0)

        except Exception as e:    # ~ Spud Mode: Displays Spud Errors. ~ #
            print(f"Error: {e}")
            sys.exit(1)
