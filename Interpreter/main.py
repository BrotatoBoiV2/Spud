"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                Programmer: Aaron "A.J." Cassell. (@BrotatoBoi)
                        Program Name: Spud Language.
                     Description: My custom language.
                              File: main.py
                            Date: 2025/11/24
                        Version: 0.1-2025.11.24

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

import tokenizer as t
import parser as p
import executor as e

class Main:
    def __init__(self):
        self._isRunning = True
        self.executor = e.Executor()
        # self.parser = Parser()
        # self.analyzer = Analyzer()
        
    # maybe make get/read file functions a separate thing.
    def read_file(self, filename):
        source = ""
        
        with open(filename, 'r') as file:
            for line in file.readlines():
                for char in line:
                    source += char
                # source += "[EOL]"
                    
        return source
    
    def get_file(self):
        args = sys.argv
        argc = len(args)
        
        if argc != 2:   raise ValueError(f"Sorry, that is not the correct usage, this would be: {args[0]} filename.pot")
        
        filename = args[1]
        
        if filename[-4:] != '.pot': raise TypeError("Sorry, that is not a `.pot` file!")
        if not os.path.exists(filename):    raise FileNotFoundError("Sorry, that file is not found!")
        
        return filename
        

    def execute(self):
        filename = self.get_file()
        source = self.read_file(filename)
        tokens = t.tokenize(source)
        # print(f"Processing the file: {tokens}")
        parser = p.Parser(tokens)
        ast = parser.parse()
        
        self.executor.run(ast)
        
        


if __name__ == '__main__':
    main = Main()

    main.execute()

