"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                Programmer: Aaron "A.J." Cassell. (@BrotatoBoi)
                        Program Name: Spud Language.
                     Description: My custom language.
                           File: tokenizer.py
                            Date: 2026/01/02
                        Version: 1.7.6-2026.01.19

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


class Token:
    """
    ~ Represents a token in the source code. ~

    Functions:
        - __init__                     : Initializes the token.
        - __str__                      : Displays the Token as a string.
    """

    def __init__(self, token_type, token_value, token_row, token_column):
        """
        ~ Initialize the Token. ~

        Arguments:
            - token_type         (str) : The type of the token.
            - token_value        (str) : The value of the token.
            - token_row         (int) : The row number of the token.
            - token_column       (int) : The column number of the token.

        """

        self.type  = token_type
        self.value = token_value
        self.row  = token_row
        self.col   = token_column

    def __str__(self):
        """
        ~ Print the Token in a string format for debugging. ~

        Returns:
            - String                   : String representation of the token.
        """

        return f"Token({self.type} | {self.value} | {self.row} | {self.col})"


class Tokenizer:
    """
    ~ The class to turn the source code into tokens for the parser. ~

    Functions:
        - __init__                     : Initializes the tokenizer.
        - tokenize                     : Tokenizes the source code.
        - peek                         : Peek at the curretn or next token.
        - process_string               : Process a string token.
        - process_comment              : Process a comment token.
    """

    def __init__(self):
        """
        ~ Initialize the Tokenizer. ~

        Attributes:
            - code               (str) : The source code.
            - index              (int) : The current index in the code.
            - column             (int) : The current column in the code.
            - row                (int) : The current row in the code.
        """

        self.code  = None
        self.index = 0
        self.col   = 1
        self.row   = 1

    def peek(self, amount=0):
        """
        ~ Peek at the next token. ~

        Arguments:
            - amount             (int) : The amount to peek ahead.

        Returns:
            - String                   : The next token to process.
        """

        # ~ Check if the token exists to avoid errors. ~ #
        if self.index + amount < len(self.code):
            return self.code[self.index + amount]

        return ""

    def process_string(self):
        """
        ~ Process a string token. ~

        Returns:
            - String                   : The string token.
        """

        string_text = ""
        start_col = self.col
        self.index += 1
        self.col   += 1

        while self.index < len(self.code) and self.peek() != '"':
            if self.peek() == "\\" and self.peek(1) == "n":
                string_text += "\n"
                self.index  += 2
                self.col    += 2

            else:
                string_text += self.peek()
                self.index += 1
                self.col   += 1

            if self.index >= len(self.code):
                error_msg = "String isn't closed with a matching quotation!"
                location  = f"row: {self.row} ; Column:{self.col}"

                raise SyntaxError("Error: " + error_msg + "\n" + location)

        self.index += 1
        self.col   += 1

        return string_text, start_col

    def process_comment(self):
        """
        ~ Process a comment token. ~

        Returns:
            - String                   : The comment token.
        """

        comment_text = ""
        start_col = self.col
        self.index += 2
        self.col   += 2

        while self.index < len(self.code):
            if self.peek() == "~" and self.peek(1) == ")":
                break

            comment_text += self.peek()
            self.index   += 1
            self.col     += 1

            if self.index >= len(self.code):
                error_msg = "Comment isn't closed with Right Potato Ears! '~)'"
                location  = f"row: {self.row} ; Column:{self.col}"

                raise SyntaxError("Error: " + error_msg + "\n" + location)

        self.index += 2
        self.col   += 2

        return comment_text, start_col

    def tokenize(self, code):
        """
        ~ Tokenize the source code. ~

        Arguments:
            - code               (str) : The source code.

        Returns:
            - List                     : A list of tokens.
        """

        self.code  = code
        self.index = 0
        self.col   = 1
        self.row   = 1
        tokens     = []
        symbols    = {
            "=": "EQUAL", "+": "OPERATOR", "(": "LPARAM", ")": "RPARAM", 
            "-": "OPERATOR", "*": "OPERATOR", "/": "OPERATOR", "#": "OPERATOR",
            "%": "OPERATOR"
        }
        logic      = [
            "equals", "not"
        ]

        # ~ Iterate through each token in the source code. ~ #
        while self.index < len(code):
            char = self.peek()

            if char.isspace():
                if char == "\n":
                    tokens.append(Token("EOL", "EOL", self.row, self.col))
                    self.row += 1
                    self.col  = 1

                else:
                    self.col += 1

                self.index += 1

            elif char == '"':
                text, col = self.process_string()

                tokens.append(Token("STRING", text, self.row, col))

            elif char == "(" and self.peek(1) == "~":
                text, col = self.process_comment()

                tokens.append(Token("COMMENT", text, self.row, col))

            elif char == "~" and self.peek(1) == ")":
                error_msg = "No Left Potato Ear '(~' found to close comment!"
                location  = f"row: {self.row} ; Column:{self.col}"

                raise SyntaxError("Error: " + error_msg + "\n" + location)

            elif char.isdigit():
                num_text  = ""
                start_col = self.col

                while self.index < len(self.code) and self.peek().isdigit():
                    num_text += self.peek()
                    self.index += 1
                    self.col   += 1

                tokens.append(Token("INTEGER", num_text, self.row, start_col))

            elif char.isalpha():
                ident     = ""
                start_col = self.col
                keys      = [
                    "say", "get", "check", "instead", "otherwise"
                ]

                while self.index < len(self.code) and self.peek().isalnum():
                    ident += self.peek()
                    self.index += 1
                    self.col   += 1

                if ident in logic:
                    token_type = "LOGIC"
                else:
                    token_type = "KEYWORD" if ident in keys else "IDENTIFIER"

                tokens.append(Token(token_type, ident, self.row, start_col))

            elif char in symbols:
                tokens.append(Token(symbols[char], char, self.row, self.col))
                self.index += 1
                self.col   += 1

            elif char == "~":
                if self.peek(1) == ".":
                    tokens.append(Token("ROOT", "~.", self.row, self.col))
                    self.index += 2
                    self.col   += 2

                else:
                    sprouts = 1
                    start_col = self.col
                    self.index += 1
                    self.col   += 1

                    while self.index < len(self.code) and self.peek() == "~":
                        sprouts    += 1
                        self.index += 1
                        self.col   += 1

                    tokens.append(Token("SPROUT", sprouts, self.row, start_col))

            elif char == ".":
                if self.peek(1) == ".":
                    if self.peek(2) == ".":
                        tokens.append(Token("TERMINATOR", char, self.row, self.col))
                        self.index += 3
                        self.col   += 3

                elif self.peek(1) == "~":
                    tokens.append(Token("EYES", ".~", self.row, self.col))
                    self.index += 2
                    self.col   += 2
                else:
                    self.index += 1
                    self.col   += 1

            else:
                self.index += 1
                self.col   += 1

        tokens.append(Token("EOL", "EOL", self.row, self.col))
        tokens.append(Token("EOF", "EOF", self.row, self.col))

        return tokens
