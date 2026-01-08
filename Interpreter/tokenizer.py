"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                Programmer: Aaron "A.J." Cassell. (@BrotatoBoi)
                        Program Name: Spud Language.
                     Description: My custom language.
                           File: tokenizer.py
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

    def peek(self, amount=1):
        if self.index + amount < len(self.code):   return self.code[self.index+amount]
        return ""

    def current(self):
        if self.index < len(self.code): return self.code[self.index]

    def tokenize(self, code):
        self.code = code

        column = 1
        row = 1
        ident = ""
        tokens = []

        while self.index < len(code):
            column += 1
            
            if self.current() == "\n":
                tokens.append(Token("EOL", "EOL", row, column))
                row += 1
                column = 1

            if self.current() == " ":
                self.index += 1

            if self.current().isalnum():
                ident += self.current()
                
            if self.current() == '"':
                string_text = ""
                self.index += 1

                while True:
                    if self.index == len(self.code):
                        error_msg = f"The string on line {row} at column {column} is missing a closing quote."

                        raise SyntaxError(error_msg)

                    if self.current() == '"' or self.current() == None:
                        break

                    elif self.current() == "\\" and self.peek() == "n":
                        string_text += "\n"
                        self.index += 2
                        continue
                    else:
                        if self.current():
                            string_text += self.current()

                        self.index += 1

                        continue

                    self.index += 1

                tokens.append(Token("STRING", string_text, row, column))

            if self.current() == "~" and self.peek() == ")":
                error_msg = f"There hasn't been a Left Potato Ear '(~' found for the matching pair on line {row} at column {column}."

                raise SyntaxError(error_msg)


            if self.current() == "(" and self.peek() == "~":
                comment_text = ""
                self.index += 2

                while True:
                    if self.index == len(self.code):
                        error_msg = f"The comment on line {row} at column {column} is missing a Right Potato Ear '~)'."

                        raise SyntaxError(error_msg)

                    if self.current() == "~" and self.peek() == ")":
                        self.index += 1
                        break

                    if self.current() == None:
                        break

                    comment_text += self.current()
                    self.index += 1

                tokens.append(Token("COMMENT", comment_text, row, column))
                continue

            if self.current().isdigit():
                while True:
                    self.index += 1
                    if self.current() == None or not self.current().isdigit():
                        break

                    ident += self.current()

                tokens.append(Token("INTEGER", ident, row, column))
                ident = ""

                continue

            if self.current() == "=":
                tokens.append(Token("EQUAL", "=", row, column))

            if self.current() == "+":
                tokens.append(Token("OPERATOR", self.current(), row, column))

            if self.current() == "(" and self.peek() == "~":
                self.index += 1
                in_comment = True

            if self.current() == "~" and self.peek() == ")":
                in_comment = False
                tokens.append(Token("COMMENT", ident, row, column))
                ident = ""

            if not self.peek().isalnum() and ident:
                if ident in ["say", "get"]:
                    tokens.append(Token("KEYWORD", ident, row, column))
                else:
                    tokens.append(Token("IDENTIFIER", ident, row, column))

                ident = ""

            self.index += 1

        tokens.append(Token("NEWLINE", "\\n", row, column))
        tokens.append(Token("EOF", "EOF", row, column))

        return tokens

