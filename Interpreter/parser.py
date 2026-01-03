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


class Parser:
    def __init__(self):
        self.index = 0
        self.tokens = None

    def peek(self):
        if self.index < len(self.tokens):
            return self.tokens[self.index+1]
        return None

    def eat(self, token):
        if token.type == "KEYWORD":
            if token.value == "say":
                if self.peek().type == "STRING":
                    output = self.peek().value
                    self.eat(self.peek())

                    return SayNode(output)

    def parse(self, tokens):
        self.tokens = tokens

        parsed = []

        while self.index < len(tokens):
            eaten = self.eat(tokens[self.index])
            if eaten:
                parsed.append(eaten)

            self.index += 1


        return parsed
            
