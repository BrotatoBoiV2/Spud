"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                Programmer: Aaron "A.J." Cassell. (@BrotatoBoi)
                        Program Name: Spud Language.
                     Description: My custom language.
                            File: parser.py
                            Date: 2026/01/02
                        Version: 0.6-2026.01.05

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

    def consume(self):
        if self.token:
            if self.token.type == "KEYWORD":
                return self.token.value

            elif self.peek().type == "IDENTIFIER":
                if self.peek(1).type == "EQUAL":
                    return "SET_VARIABLE"

                return self.token.value

            elif self.token.type == "STRING":
                self.parsed.append(StringNode(self.token.value))

                return None

            elif self.token.type == "INTEGER":
                self.parsed.append(IntegerNode(self.token.value))

                return None

        return None

    def begin_parser(self, tokens):
        self.tokens = tokens 
        self.token = self.peek()

    def parse_say(self):
        self.advance()
        
        output_parts = []
        
        while True:
            if self.token.type == "EOL" or self.token.type == "EOF":
                break
            
            elif self.token.type == "STRING":
                output_parts.append(StringNode(self.token.value))

            elif self.token.type == "INTEGER":
                output_parts.append(IntegerNode(self.token.value))

            elif self.token.type == "IDENTIFIER":
                output_parts.append(VariableNode(self.token.value))

            elif self.token.type == "ADDITION":
                output_parts.append(OperatorNode(self.token.value))

            self.advance()

        return SayNode(output_parts)

    def parse_get(self):
        self.advance()

        var_name = ""
        prompt = ""

        if self.token.type == "IDENTIFIER":
            var_name = self.token.value
            self.advance()
        else:
            raise SyntaxError("Expected an identifier after `get` keyword.")

        while True:
            if self.token.type == "EOL" or self.token.type == "EOF":
                break

            if self.token.type == "IDENTIFIER":
                var_name += self.token.value

            if self.token.type == "STRING":
                prompt += self.token.value

            self.advance()

        return GetNode(var_name, prompt)

    def parse_set_variable(self):
        value_parts = []
        var_name = self.token.value

        while True:
            if self.peek(1).type == "EOL" or self.peek(1).type == "EOF":
                break

            elif self.peek(1).type == "STRING":
                value_parts.append(StringNode(self.peek(1).value))

            elif self.peek(1).type == "INTEGER":
                value_parts.append(IntegerNode(self.peek(1).value))
            
            self.advance()
            
        return VariableNode(var_name, value_parts)

    def parse(self, tokens):
        self.begin_parser(tokens)

        while self.token.type != "EOF":
            token_value = self.consume()
            
            if token_value == "say":
                self.parsed.append(self.parse_say())
            
            elif token_value == "get":
                self.parsed.append(self.parse_get())

            elif token_value == "SET_VARIABLE":
                self.parsed.append(self.parse_set_variable())
            
            self.advance()

        return self.parsed
