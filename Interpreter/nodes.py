"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                Programmer: Aaron "A.J." Cassell. (@BrotatoBoi)
                        Program Name: Spud Language.
                     Description: My custom language.
                             File: nodes.py
                            Date: 2026/01/02
                        Version: 0.6-2026.01.05

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


VARIABLES = {}


class VariableNode:
  def __init__(self, name, value_parts=None):
    self.name = name
    self.value_parts = value_parts

  def evaluate(self):
    if self.name in VARIABLES:
      # print(VARIABLES[self.name])
      return VARIABLES[self.name]

    raise ValueError(f"Variable {self.name} is not defined.")

  # ~ Add an execute function that creates a variable
  # A simple `VARIABLES[self.name] = self.value` is possibly all that is needed
  def execute(self):
    value = ""

    for part in self.value_parts:
      if isinstance(part, VariableNode):
        if part.evaluate():
          value += part.evaluate()
        else:
          raise ValueError(f"Variable {part.name} is not defined.")
      else:
        value += part

    VARIABLES[self.name] = value


class SayNode:
  def __init__(self, output_parts):
    self.output_parts = output_parts

  def execute(self):
    prompt = ""

    for output in self.output_parts:
      if isinstance(output, VariableNode):
        if output.evaluate():
          prompt += output.evaluate()
        else:
          raise ValueError(f"Variable {output.name} is not defined.")
      else:
        prompt += output

    print(prompt, end="")
    

class GetNode:
  def __init__(self, var_name, prompt):
    self.var_name = var_name
    self.prompt = prompt

  def execute(self):
    value = input(self.prompt)
    VARIABLES[self.var_name] = value
    # print(VARIABLES)
