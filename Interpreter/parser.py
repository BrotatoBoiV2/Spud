"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                Programmer: Aaron "A.J." Cassell. (@BrotatoBoi)
                        Program Name: Spud Language.
                     Description: My custom language.
                            File: parser.py
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


from nodes import *
from tokenizer import Token


class Parser:
  def __init__(self):
    self.index = 0
    self.tokens = None
    self.token = None
    self.parsed = []

  def peek(self, amount=0):
    if self.index+amount != len(self.tokens):
      return self.tokens[self.index+amount]

  def advance(self, amount=1):
    self.index += amount
    self.token = self.peek()

    if not self.token:
      self.token = Token("EOF", "EOF", None, None)

  def parse_say(self):
    self.advance()

    return SayNode(self.parse_expression(), self.token.line, self.token.column)

  def parse_expression(self):
    left = self.parse_primary()

    while self.token.type == "OPERATOR":
      oper = self.token.value
      self.advance()
      
      right = self.parse_primary()
      left = BinOperNode(oper, left, right, self.token.line, self.token.column)
    
    return left

  def parse_primary(self):
    token = self.token

    if token.type == "INTEGER":
      self.advance()
      return IntegerNode(token.value, token.line, token.column)

    elif token.type == "STRING":
      self.advance()
      return StringNode(token.value, token.line, token.column)

    elif token.type == "IDENTIFIER":
      self.advance()
      return VariableNode(token.value, token.line, token.column)

    elif token.type == "LPARAM":
      self.advance()
      node = self.parse_expression()

      if self.token.type != "RPARAM":
        raise SyntaxError("Expected ')' after expression.")

      self.advance()
      return node


  def parse_get(self):
    self.advance()

    var_name = ""
    prompt = ""

    if self.token.type == "IDENTIFIER":
      var_name = self.token.value
      self.advance()
    else:
      raise SyntaxError("Expected identifier after 'get'.")

    if self.peek(1).type != "EOL":
      prompt = self.parse_expression()

    return GetNode(var_name, prompt, self.token.line, self.token.column)

  def parse_set_variable(self):
    var_name = self.token.value
    self.advance()

    if self.token.type != "EQUAL":
      raise SyntaxError("Expected '=' after variable name.")

    self.advance()

    expression_tree = self.parse_expression()

    return VariableNode(var_name, self.token.line, self.token.column, value_parts=expression_tree)


  def parse(self, tokens):
    self.tokens = tokens
    self.token = self.peek()

    while self.token.type != "EOF":
      token = self.token

      if token.type == "KEYWORD":
        if token.value == "say":
          self.parsed.append(self.parse_say())
        
        elif token.value == "get":
          self.parsed.append(self.parse_get())

      elif token.type == "IDENTIFIER":
        self.parsed.append(self.parse_set_variable())

      else:
        self.advance()

    return self.parsed

