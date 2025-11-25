"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                Programmer: Aaron "A.J." Cassell. (@BrotatoBoi)
                        Program Name: Spud Language.
                     Description: My custom language.
                           File: executor.py
                            Date: 2025/11/24
                        Version: 0.3-2025.11.25

===============================================================================

                        Copyright (C) 2025 BrotatoBoi 
        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published
        by: The Free Software Foundation, either version 3 of the
        License, or any later version.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

# ~ Import custom modules. ~ #
import parser as p


class Executor:
    def __init__(self):
        """
            Initialize the executor for the interpreter.
            
            Attributes:
                variables (dict) : A dictionary that stores variables.
        """
        
        self.variables = {}
    
    def run(self, statements):
        """
            Run the executor and process each node.
            
            Arguments:
                statements (array) : An array of AST nodes to process.
        """
        
        for state in statements:
            
            # ~ Handle variable assignment. ~ #
            if isinstance(state, p.SetNode):
                self.variables[state.name] = state.value
            
            # ~ Handle output. ~ #
            elif isinstance(state, p.SayNode):
                output = state.prompt
                
                if output in self.variables:
                    print(self.variables[output])
                else:
                    print(output)
            
            # ~ Handle input. ~ #
            elif isinstance(state, p.GetNode):
                self.variables[state.var_name] = input(state.prompt)
