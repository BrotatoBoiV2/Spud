"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                Programmer: Aaron "A.J." Cassell. (@BrotatoBoi)
                        Program Name: Spud Language.
                     Description: My custom language.
                            File: parser.py
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

class SetNode:
  def __init__(self, name, value=None):
    """
      This Node sets variables values.

      Arguments:
        name (str) : The name of the variable.
        value (str) : The value of the variable.
    """

    self.name = name
    self.value = value


class SayNode:
  def __init__(self, prompt):
    """
      This Node outputs text and in the future, speaks.

      Arguments:
        prompt (str) : The prompt that needs to be said.

      Attributes:
        prompt (str) : Extends from the argument `prompt`.
        value (str) : Alias for compatibility with executor.
    """

    self.prompt = prompt


class GetNode:
  def __init__(self, var_name, prompt):
    """
      This Node gets input from the user with a prompt to display.

      Arguments:
        var_name (str) : The name of the variable.
        prompt (str) : The prompt to display to the user.

      Attributes:
        var_name (str) : Extends from the argument `var_name`.
        prompt (str) : Extends from the argument `prompt`.
    """

    self.var_name = var_name
    self.prompt = prompt


class Parser:
  def __init__(self, tokens):
    """
      Initialize the parser and its variables.

      Arguments:
        tokens (array) : Tokens extracted from the source code.

      Attributes:
        tokens (array) : Extends from the argument `tokens`.
        pos (int) : The position of the current token.
    """

    self.tokens = tokens
    self.pos = 0

  def current(self):
    """Get the current token."""

    return self.tokens[self.pos]

  def eat(self, token_type):
    """
      Consume the current token if it matches the expected type.

      Arguments:
        token_type (str) : The expected type of the token.
    """

    if self.current().token_type == token_type:
      self.pos += 1
    else:
      raise Exception(
        f"Expected {token_type}, got {self.current().token_type}"
      )

  def parse_set(self):
    """Parse the `set` keyword."""

    self.eat("KEYWORD_SET")
    name = self.current().value
    self.eat("IDENTIFIER")
    self.eat("EQUALS")

    value = self.current().value
    self.eat(self.current().token_type)

    return SetNode(name, value)

  def parse_say(self):
    """Parse the `say` keyword."""

    self.eat("KEYWORD_SAY")
    value = self.current().value
    self.eat(self.current().token_type)

    return SayNode(value)

  def parse_get(self):
    """Parse the `get` keyword."""

    self.eat("KEYWORD_GET")
    var_name = self.current().value
    self.eat("IDENTIFIER")

    prompt = self.current().value
    self.eat(self.current().token_type)

    return GetNode(var_name, prompt)

  def parse(self):
    """
      Parse all tokens and generate statements.

      Returns:
        statements (array) : Parsed statements ready for execution.
    """

    statements = []

    while self.current().token_type != "EOF":
      if self.current().token_type == "KEYWORD_SET":
        statements.append(self.parse_set())
      elif self.current().token_type == "KEYWORD_SAY":
        statements.append(self.parse_say())
      elif self.current().token_type == "KEYWORD_GET":
        statements.append(self.parse_get())
      else:
        raise Exception(
          f"Unexpected token: {self.current().token_type}:"
          f"{self.current().value}"
        )

    return statements
