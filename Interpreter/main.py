"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                Programmer: Aaron "A.J." Cassell. (@BrotatoBoi)
                        Program Name: Spud Language.
                     Description: My custom language.
                              File: main.py
                            Date: 2026/01/02
                        Version: 1.0-2026.01.09

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
from sys import argv

# ~ Import Local Modules. ~ #
from tokenizer import Tokenizer
from parser import Parser
from memory import Environment


class Main:
    def __init__(self):
        self.tokenizer = Tokenizer()
        self.parser = Parser()
        self.file = argv[1] if len(argv) > 1 else self.display_usage()

        if not self.file.endswith(".pot"):
            print("File is not a `.pot` file!")
            self.display_usage()

        self._is_running = True

    def display_usage(self):
        print(f"Usage: python3 {argv[0]} <file.pot>")
        exit()

    def read_file(self):
        with open(self.file, "r") as f:
            return f.read()

    def execute(self):
        global_memory = Environment()

        while self._is_running:
            file_string = self.read_file()
            tokens = self.tokenizer.tokenize(file_string)
            # for token in tokens:
            #     print(token)
            ast = self.parser.parse(tokens)
            
            for node in ast:
                if node:
                    node.execute(global_memory)

            print("")

            self._is_running = False


if __name__ == '__main__':
    main = Main()

    if "--debug" in argv:
        main.execute()

    else:
        try:
            main.execute()
        except Exception as e:
            print(f"Error: {e}")
