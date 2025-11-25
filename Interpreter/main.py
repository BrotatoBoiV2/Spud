"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                Programmer: Aaron "A.J." Cassell. (@BrotatoBoi)
                        Program Name: Spud Language.
                     Description: My custom language.
                              File: main.py
                            Date: 2025/11/24
                        Version: 0.3-2025.11.25

===============================================================================

                        Copyright (C) 2025 BrotatoBoi
        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published
        by: The Free Software Foundation, either the version 3 of the
        License, or any later version.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


# ~ Import standard modules. ~ #
import os
import sys

# ~ Import custom modules. ~ #
import tokenizer as t
import parser as p
import executor as e


class Main:
    def __init__(self):
        """
            Initialize the main program.

            Attributes:
                _isRunning (bool) : State of the loop. (Possibly deprecate)
                executor (obj) : Executes the parsed AST.
        """

        self._isRunning = True
        self.executor = e.Executor()

    # maybe make get/read file functions a separate thing.
    def read_file(self, filename):
        """
            Read a file and return the entire source code within it.

            Arguments:
                filename (str) : The name of the source file to read.

            Returns:
                source (str) : Full text of the Spud source file.
        """

        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()

    def get_file(self):
        """
            Get a filename from the command line.
            Check if that file exists or is in the right format.

            Returns:
                filename (str) : The name of the source file.
        """

        args = sys.argv
        argc = len(args)

        if argc != 2:
            raise ValueError(
                f"Sorry, that is not the correct usage, this would be: "
                f"{args[0]} filename.pot"
            )

        filename = args[1]

        if not filename.endswith('.pot'):
            raise TypeError("Sorry, that is not a `.pot` file!")

        if not os.path.exists(filename):
            raise FileNotFoundError("Sorry, that file is not found!")

        return filename

    def execute(self):
        """
            Get a file from the argument line.
            Tokenize the source code, parse it into an AST, then execute it.
        """

        # ~ Get the file and read the source. ~ #
        filename = self.get_file()
        source = self.read_file(filename)

        # ~ Tokenize, Parse and Execute the source. ~ #
        tokens = t.tokenize(source)
        parser = p.Parser(tokens)
        ast = parser.parse()
        self.executor.run(ast)


if __name__ == '__main__':
    main = Main()
    main.execute()
