"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                Programmer: Aaron "A.J." Cassell. (@BrotatoBoi)
                        Program Name: Spud Language.
                     Description: My custom language.
                             File: nodes.py
                            Date: 2026/01/02
                        Version: 1.1-2026.01.09

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


def peek(parts, amount=1):
  if len(parts) > amount:
    return parts[amount]

def join_parts(parts, memory):
  if not parts: return None
  
  return parts.execute(memory)

class Node:
  def __init__(self, value, line, column):
    self.value = value
    self.line = line
    self.column = column


  def execute(self, memory):
    pass


class IntegerNode(Node):
  def __init__(self, value, line, column):
    super().__init__(value, line, column)

  def execute(self, memory):
    return int(self.value)


class StringNode(Node):
  def __init__(self, value, line, column):
    super().__init__(value, line, column)

  def execute(self, memory):
    return str(self.value)

  
class BinOperNode(Node):
  def __init__(self, value, left, right, line, column):
    super().__init__(value, line, column)

    self.left = left
    self.right = right

  def execute(self, memory):
    left = self.left.execute(memory)
    right = self.right.execute(memory)

    if self.value == "+":
      if isinstance(left, int) and isinstance(right, int):
        return int(left) + int(right)

      return str(left) + str(right)

    raise ValueError(f"Invalid operator: {self.value}")


class VariableNode(Node):
  def __init__(self, value, line, column, value_parts=None):
    super().__init__(value, line, column)

    self.value_parts = value_parts

  def execute(self, memory):
    if not self.value_parts:
      value = memory.get(self.value)

      if value is not None:
        return value

      raise ValueError(f"Variable {self.value} is not defined.")

    else:
      value = join_parts(self.value_parts, memory)
      
      memory.set(self.value, value)


class SayNode(Node):
  def __init__(self, value, line, column):
    super().__init__(value, line, column)


  def execute(self, memory):
    prompt = join_parts(self.value, memory)

    print(prompt, end="", flush=True)


class GetNode(Node):
  def __init__(self, value, prompt, line, column):
    super().__init__(value, line, column)

    self.prompt = prompt

  def execute(self, memory):
    is_num = True
    prompt = join_parts(self.prompt, memory) if self.prompt else ""
    value = input(prompt)

    if not value:
      raise ValueError("No value provided.")

    for val in value:
      if not val.isdigit():
        is_num = False
        break

    if is_num:
      value = int(value)
    
    memory.set(self.value, value)
