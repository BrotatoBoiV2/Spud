"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                Programmer: Aaron "A.J." Cassell. (@BrotatoBoi)
                        Program Name: Spud Language.
                     Description: My custom language.
                            File: parser.py
                            Date: 2026/01/02
                        Version: 0.5-2026.01.03

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

    def peek(self):
        if self.index != len(self.tokens):
            return self.tokens[self.index]

    def advance(self):
        self.index += 1
        self.token = self.peek()

        if not self.token:
            self.token = Token("EOF", "EOF", None, None)

        # print(f"TEST: {self.token}")

    def consume(self):
        if self.token:
            if self.token.type == "KEYWORD":
                return self.token.value

            if self.token.type == "IDENTIFIER":
                return self.token.value

            if self.token.type == "STRING":
                return self.token.value

            else:
                pass

        return None

    def begin_parser(self, tokens):
        self.tokens = tokens 
        self.token = self.peek()

    def parse(self, tokens):
        self.begin_parser(tokens)

        # for token in tokens:
        #     print(token)


        parsed = []

        # if not self.token:
        #     return False

        while self.token.type != "EOF":
            token_value = self.consume()
            
            if token_value == "say":
                output = ""

                while True:
                    if self.token.type == "EOL" or self.token.type == "EOF":
                        break
                    
                    if self.token.type == "STRING":
                        output += self.token.value

                    if self.token.type == "INTEGER":
                        # ~ Make an update to handle math equations. ~ #
                        output += self.token.value

                    self.advance()

                print(output, end="")

            
            self.advance()

        print("")
