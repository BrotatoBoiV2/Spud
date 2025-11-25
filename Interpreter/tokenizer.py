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
        by: The Free Software Foundation, either version 3 of the
        License, or any later version.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


class Token:
    def __init__(self, token_type, value):
        """
            Initialize a token with its attributes.
            
            Arguments:
                token_type (str) : The type that the token should be.
                value (str) : The value of the token.
                
            Attributes:
                token_type (str) : Extends from argument `token_type`.
                value (str) : Extends from argument `value`.
        """
        
        self.token_type = token_type
        self.value = value
    
    def __repr__(self):
        """
            Display the token.
        """
        
        return f"Token({self.token_type}, {self.value})"


def tokenize(source):
    """
        Tokenize the source code into Tokens.
        
        Arguments:
            source (str) : The source code that needs to be interpreted.
          
        Returns:
            tokens (array) : All of the Tokens that were processed.
    """
    
    tokens = []
    i = 0
    
    while i < len(source):
        char = source[i]
        
        # ~ Skip whitespace. ~ #
        if char.isspace():
            i += 1
            continue
        
        # ~ Process a number. ~ #
        if char.isdigit():
            num = char
            i += 1
            
            while i < len(source) and source[i].isdigit():
                num += source[i]
                i += 1
            
            tokens.append(Token("NUMBER", int(num)))
            continue
        
        # ~ Process identifiers and keywords. ~ #
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
        
        # ~ Process comment blocks. ~ #
        if char == "#":
            i += 1
            
            while i < len(source) and source[i] != "#":
                i += 1
            
            i += 1
            continue
        
        # ~ Process equals symbol. ~ #
        if char == "=":
            tokens.append(Token("EQUALS", "="))
            i += 1
            continue
        
        # ~ Process string literals. ~ #
        if char == '"':
            i += 1
            string_data = ""
            
            while i < len(source) and source[i] != '"':
                string_data += source[i]
                i += 1
                
            if i >= len(source):
                raise Exception("Unterminated string literal.")
            
            i += 1
            tokens.append(Token("STRING", string_data))
            continue
        
        # ~ Handle unknown characters. ~ #
        raise Exception(f"Unknown character in source: {char}")
    
    tokens.append(Token("EOF", None))
    
    return tokens
