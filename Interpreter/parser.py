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
    self.name = name
    self.value = value
    
class SayNode:
  def __init__(self, value):
    self.value = value
    
class GetNode:
  def __init__(self, var_name, prompt):
    self.var_name = var_name
    self.prompt = prompt
    
class Parser:
  def __init__(self, tokens):
    self.tokens = tokens
    self.pos = 0
    
  def current(self):
    return self.tokens[self.pos]
  
  def eat(self, tokenType):
    if self.current().tokenType == tokenType:
      self.pos += 1
      
    else:
      raise Exception(f"Expected {tokenType}, got {self.current().tokenType}")
    
  def parse_set(self):
    self.eat("KEYWORD_SET")
    name = self.current().value
    self.eat("IDENTIFIER")
    self.eat("EQUALS")
    value = self.current().value
    
    self.eat(self.current().tokenType)
    
    return SetNode(name, value)
  
  def parse_say(self):
    self.eat("KEYWORD_SAY")
    value = self.current().value
    
    self.eat(self.current().tokenType)
    
    return SayNode(value)
    
  def parse_get(self):
    self.eat("KEYWORD_GET")
    var_name = self.current().value
    
    self.eat("IDENTIFIER")  
    prompt = self.current().value
    self.eat(self.current().tokenType)
    
    return GetNode(var_name, prompt)
    
  def parse_comment(self):
    pass
  
  def parse(self):
    statements = []
    
    while self.current().tokenType != "EOF":
      if self.current().tokenType == "KEYWORD_SET":
        statements.append(self.parse_set())
      elif self.current().tokenType == "KEYWORD_SAY":
        statements.append(self.parse_say())
      elif self.current().tokenType == "KEYWORD_GET":
        statements.append(self.parse_get())
      else:
        raise Exception(f"Unexpected token: {self.current().tokenType}:{self.current().value}")
      
    return statements
    