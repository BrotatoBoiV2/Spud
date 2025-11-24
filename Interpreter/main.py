"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                Programmer: Aaron "A.J." Cassell. (@BrotatoBoi)
                        Program Name: Spud Language.
                     Description: My custom language.
                              File: main.py
                            Date: 2025/11/24
                        Version: 0.0-2025.11.24

===============================================================================

                        Copyright (C) 2025 BrotatoBoi 
        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published
        by: The Free Software Foundation, either the version 3 of the
        License, or any later version.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

# Tokenizer
# Parser -> Builds an AST
# Semantic Analysis (vars before use, type checking, scope rules, function signatures, proper imports, and other similar checking)
# Executer (for Interpreter) | Code Generator (for Compiler)


# read a file line by line and process it as outlined above. 
import os
import sys

class Main:
    def __init__(self):
        self._isRunning = True
        # self.tokenizer = Tokenizer()
        # self.parser = Parser()
        # self.analyzer = Analyzer()
        
    def read_file(self, filename):
        lines = []
        
        with open(filename, 'r') as file:
            for line in file.readlines():
                lines.append(line.strip())
            
        return lines

    def execute(self):
        args = sys.argv
        argc = len(args)
        
        if argc != 2:
            print(f"Usage: {args[0]} file.pot")
        
            return False
        
        filename = args[1]
        
        if filename[-4:] != '.pot':
            print("Please use a `.pot` file!")
            
            return False
        
        if not os.path.exists(filename):
            print("That file does not exist!")
            
            return False
        
        file_lines = self.read_file(filename)
        
        print(f"Processing the file: {file_lines}")


if __name__ == '__main__':
    main = Main()

    main.execute()

