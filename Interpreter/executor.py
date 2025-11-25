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
        by: The Free Software Foundation, either the version 3 of the
        License, or any later version.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import parser as p

class Executor:
  def __init__(self):
    self.variables = {}
    
  def run(self, statements):
    for state in statements:
      if isinstance(state, p.SetNode):
        self.variables[state.name] = state.value
      
      if isinstance(state, p.SayNode):
        output = state.value
        
        if output in self.variables:
          print(self.variables[output])
        else:
          print(output)
        
      if isinstance(state, p.GetNode):
        self.variables[state.var_name] = input(state.prompt)