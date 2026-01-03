"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                Programmer: Aaron "A.J." Cassell. (@BrotatoBoi)
                        Program Name: Spud Language.
                     Description: My custom language.
                           File: tokenizer.py
                            Date: 2026/01/02
                        Version: 0.3-2026.01.03

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


# from dataclasses import dataclass


# @dataclass
class Token:
    def __init__(self, token_type, token_value, token_line, token_column):
        self.type = token_type
        self.value = token_value
        self.line = token_line
        self.column = token_column

    def __str__(self):
        return f"Token({self.type} | {self.value} | {self.line} | {self.column})"


class Tokenizer:
    def __init__(self):
        self.code = None
        self.index = 0

    def peek(self):
        if self.index + 1 < len(self.code):   return self.code[self.index+1]
        return ""


    def tokenize(self, code):
        self.code = code

        column = 0
        row = 0
        ident = ""
        tokens = []
        in_comment = False
        in_string = False

        while self.index < len(code):
            column += 1

            if code[self.index] == "\n":
                row += 1
                column = 0

            token = code[self.index]

            if token.isalpha():
                if in_comment or in_string:
                    while True:
                        if not (token == " " and (self.peek() == '"' or self.peek() == "~")):
                            ident += token
                        self.index += 1
                        token = code[self.index]

                        if token == '"' or token == "~" and self.peek() == ")":
                            break
                else:
                    ident += token

            if token == "(" and self.peek() == "~":
                self.index += 1
                in_comment = True

            elif token == "~" and self.peek() == ")":
                in_comment = False
                tokens.append(Token("COMMENT", ident, row, column))
                ident = ""
                self.index += 1

            elif token == '"':
                if not in_string:
                    in_string = True
                else:
                    tokens.append(Token("STRING", ident, row, column))
                    ident = ""
                    in_string = False

            elif self.peek() == " " and ident:
                if ident in ["say"]:
                    tokens.append(Token("KEYWORD", ident, row, column))
                else:
                    raise Exception(f"Unknown keyword: {ident}")

                ident = ""

            self.index += 1

        return tokens

