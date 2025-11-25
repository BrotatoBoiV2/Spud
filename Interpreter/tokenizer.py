"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                Programmer: Aaron "A.J." Cassell. (@BrotatoBoi)
                        Program Name: Spud Language.
                     Description: My custom language.
                           File: tokenizer.py
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

class Token:
  def __init__(self, tokenType, value):
    self.tokenType = tokenType
    self.value = value
    
  def __repr__(self):
    return f"Token({self.tokenType}, {self.value})"
    
def tokenize(source):
  tokens = []
  i = 0
  
  while i < len(source):
    char = source[i]
    
    if char.isspace():
      i += 1
      continue
    
    if char.isdigit():
      num = char
      i += 1
      
      while i < len(source) and source[i].isdigit():
        num += source[i]
        i += 1
      
      tokens.append(Token("NUMBER", int(num)))
      continue
    
    if char.isalpha():
      ident = char
      i += 1
      
      while i < len(source) and source[i].isalnum():
        ident += source[i]
        i += 1
        
      if ident == "set":
        tokens.append(Token("KEYWORD_SET", ident))
        
      elif ident == "say":
        tokens.append(Token("KEYWORD_SAY", ident))
        
      elif ident == "get":
        tokens.append(Token("KEYWORD_GET", ident))
        
      else:
        tokens.append(Token("IDENTIFIER", ident))

      continue
    
    if char == "#":
      i += 1
      comment = ""
      
      while i < len(source) and source[i] != "#":
        comment += source[i]
        i += 1        
        
      #tokens.append(Token("COMMENT", comment))
      i += 1
      continue
    
    if char == "=":
      tokens.append(Token("EQUALS", "="))
      i += 1
      
      continue
    
    if char == '"':
      i += 1
      string_data = ""
      
      while i < len(source) and source[i] != '"':
        string_data += source[i]
        i += 1
        
      if i >= len(source):
        raise Exception("Unterminated string!")

      i += 1
      tokens.append(Token("STRING", string_data))
      
      continue
    
    raise Exception(f"Unknown character: {char}")
    
  tokens.append(Token("EOF", None))
  return tokens
