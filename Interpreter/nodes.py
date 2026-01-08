"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                Programmer: Aaron "A.J." Cassell. (@BrotatoBoi)
                        Program Name: Spud Language.
                     Description: My custom language.
                             File: nodes.py
                            Date: 2026/01/02
                        Version: 0.8-2026.01.07

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

def peek(parts, amount=1):
  if len(parts) > amount:
    return parts[amount]

def join_parts(parts):
  index = 0

  if parts:
    while index < len(parts):
      part = parts[index]
      
      if isinstance(part, VariableNode):
        return part.evaluate()

      return part.execute()

      index += 1 


class IntegerNode:
  def __init__(self, value, line, column):
    self.value = int(value)
    self.line = line
    self.column = column


  def execute(self):
    return self.value


class StringNode:
  def __init__(self, value, line, column):
    self.value = value
    self.line = line
    self.column = column

  def execute(self):
    return self.value

  
class BinOperNode:
  def __init__(self, left, oper, right, line, column):
    self.oper = oper
    self.left = left
    self.right = right
    self.line = line
    self.column = column

  def execute(self):
    left = None
    right = None

    if self.oper == "+":
      if isinstance(self.left, VariableNode):
        left = self.left.evaluate()
      elif isinstance(self.left, StringNode):
        left = self.left.execute()

      if isinstance(self.right, VariableNode):
        right = self.right.evaluate()
      elif isinstance(self.right, StringNode):
        right = self.right.execute()

      if type(left) == str or type(right) == str:
        return str(left) + str(right)

      return left + right



    raise ValueError(f"Invalid operator: {self.oper}")


class VariableNode:
  def __init__(self, name, line, column, value_parts=None):
    self.name = name
    self.line = line
    self.column = column
    self.value_parts = value_parts

  def evaluate(self):
    # print(VARIABLES)
    if self.name in VARIABLES:
      return VARIABLES[self.name]

    raise ValueError(f"Variable {self.name} is not defined.")

  def execute(self):
    value = join_parts(self.value_parts)
    VARIABLES[self.name] = value


class SayNode:
  def __init__(self, output_parts, line, column):
    self.output_parts = output_parts
    self.line = line
    self.column = column

  def execute(self):
    prompt = join_parts(self.output_parts)

    print(prompt, end="")


class GetNode:
  def __init__(self, var_name, prompt, line, column):
    self.var_name = var_name
    self.prompt = prompt
    self.line = line
    self.column = column

  def execute(self):
    value = input(self.prompt)
    VARIABLES[self.var_name] = value
    # print(VARIABLES)
