"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                Programmer: Aaron "A.J." Cassell. (@BrotatoBoi)
                        Program Name: Spud Language.
                     Description: My custom language.
                            File: parser.py
                            Date: 2026/01/02
                        Version: 1.1.2-2026.01.13

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

# ~ Import Local Modules. ~ #
from nodes import (
	IntegerNode, StringNode, BinOperNode, VariableNode, SayNode, GetNode,
    LogicNode, BoolNode, CheckNode
)
from tokenizer import Token


class Parser:
    """
    ~ The parser class that is responsible for creating nodes from tokens. ~

    Functions:
		- __init__                     : Initializes the parser.
		- peek                         : Peek at the next token.
		- advance                      : Advance to the next token.
		- parse_say                    : Parse a 'say' statement.
		- parse_expression             : Parse an expression.
		- parse_primary                : Parse a primary expression.
		- parse_get                    : Parse a 'get' statement.
		- parse_set_variable           : Parse a variable assignment.
		- parse                        : Parse the source code.
    """

    def __init__(self):
        """
        ~ Initialize the Parser. ~

        Attributes:
			index                (int) : The current index in the tokens.
			tokens              (list) : The list of tokens.
			token              (Token) : The current token.
			parsed              (list) : The list of parsed nodes.
        """

        self.index = 0
        self.tokens = None
        self.token = None
        self.parsed = []
        self.sprouts = 0

    def peek(self, amount=0):
        """
        ~ Peek at the next token. ~

        Arguments:
			amount               (int) : The amount to peek ahead.

        Returns:
			Token                      : The next token to process.
        """

        if self.tokens and self.index + amount < len(self.tokens):
            return self.tokens[self.index + amount]

    def advance(self, amount=1):
        """
        ~ Advance to the next token. ~

        Arguments:
			amount               (int) : The amount to advance.
        """

        self.index += amount
        self.token = self.peek()

        if not self.token:
            self.token = Token("EOF", "EOF", None, None)

    def parse_say(self):
        """
        ~ Parse a 'say' statement. ~

        Returns:
			SayNode                    : The parsed 'say' statement.
        """

        line, col = self.token.line, self.token.col
        self.advance()

        return SayNode(self.parse_expression(), line, col)

    def parse_expression(self):
        """
        ~ Parse an expression. ~

        Returns:
			BinOperNode                : The parsed expression.
        """

        left = self.parse_primary()

        while self.token.type == "OPERATOR":
            oper = self.token.value
            self.advance()

            right = self.parse_primary()
            left = BinOperNode(
				oper,
				left,
				right,
				self.token.line,
				self.token.col
			)

        return left

    def parse_primary(self):
        """
        ~ Parse a primary expression. ~

        Returns:
			Node                       : The parsed primary expression.
        """

        token = self.token

        if token.type == "INTEGER":
            self.advance()
            return IntegerNode(token.value, token.line, token.col)

        elif token.type == "STRING":
            self.advance()
            return StringNode(token.value, token.line, token.col)

        elif token.type == "IDENTIFIER":
            self.advance()
            return VariableNode(token.value, token.line, token.col)

        elif token.type == "LPARAM":
            self.advance()
            node = self.parse_expression()

            if self.token.type != "RPARAM":
                raise SyntaxError("Expected ')' after expression.")

            self.advance()
            return node

        elif token.type == "RPARAM":
            raise SyntaxError("Found a ')' that does not close an expression.")

        elif token.type == "LOGIC":
            self.advance()

            return LogicNode(token.value, token.line, token.col)

    def parse_get(self):
        """
        ~ Parse a 'get' statement. ~

        Returns:
			GetNode                    : The parsed 'get' statement.
        """

        self.advance()
        var_name = ""
        prompt = ""

        if self.token.type == "IDENTIFIER":
            var_name = self.token.value
            self.advance()

        else:
            raise SyntaxError("Expected identifier after 'get'.")

        if self.token.type not in ["EOL", "EOF"]:
            prompt = self.parse_expression()

        return GetNode(var_name, prompt, self.token.line, self.token.col)

    def parse_set_variable(self):
        """
        ~ Parse a variable assignment. ~

        Returns:
			VariableNode               : The parsed variable assignment.
        """

        var_name = self.token.value
        line, col = self.token.line, self.token.col
        self.advance()

        if self.token.type != "EQUAL":
            raise SyntaxError("Expected '=' after variable name.")

        self.advance()

        expression_tree = self.parse_expression()

        return VariableNode(var_name, line, col, value_parts=expression_tree)

    def parse_condition(self):
        """
        ~ Parse a condition. ~

        Returns:
			BoolNode                   : The parsed condition.
        """
        
        left = self.parse_expression()


        while self.token.type == "LOGIC":
            logic = self.token.value
            self.advance()

            right = self.parse_expression()

            left = BoolNode(
                logic,
                left,
                right,
                self.token.line,
                self.token.col
            )

        return left


    def parse_check(self):
        """
        ~ Parse a 'check' statement. ~

        Returns:
			CheckNode                  : The parsed 'check' statement.
        """

        self.advance()
        conditions = self.parse_condition()
        code = []
        self.advance()
        # print(self.token)
        # for token in self.tokens:
        #     print(token)

        if self.token.type == "SPROUT":
            sprouts = self.token.value
            # print(sprouts)
            # print("HEHE")
            if sprouts == self.sprouts + 1:
                # print("HAHA")
                self.sprouts = self.token.value

                while self.index <= len(self.tokens):
                    # print("TOKEN")
                    # print(self.token)
                    if self.token.type == "TERMINATOR":
                        self.advance()
                        break  
                    
                    token = self.token
                    if token.type == "KEYWORD":
                        if token.value == "say":
                            code.append(self.parse_say())

                        elif token.value == "get":
                            code.append(self.parse_get())

                        elif token.value == "check":
                            code.append(self.parse_check())

                    elif token.type == "IDENTIFIER":
                        code.append(self.parse_set_variable())

                    if self.token.type == "EOL":
                        if self.peek(1).type == "TERMINATOR":
                            self.advance()
                            break
                        elif self.peek(1).type != "SPROUT":
                            raise SyntaxError("Expected sprout after code.")



                    # self.advance()
                    # print(self.token)
                    # if self.token.type != "SPROUT":
                    #     raise SyntaxError("Expected sprout after code.")

                    self.advance()

                print(code)
                
            elif sprouts > self.sprouts:
                raise SyntaxError("Code has been over-sprouted.")

            elif sprouts < self.sprouts:
                raise SyntaxError("Code has been under-sprouted.")

        else:
            raise SyntaxError("Expected code to sprout after `check` keyword.")

        return CheckNode(code, self.token.line, self.token.col, condition=conditions)


    def parse(self, tokens):
        """
        ~ Parse the source code. ~

        Arguments:
			tokens              (list) : The list of tokens.

        Returns:
			list                       : The list of parsed nodes.
        """

        self.tokens = tokens
        self.token = self.peek() or Token("EOF", "EOF", None, None)

        while self.token.type != "EOF":
            token = self.token

            if token.type == "KEYWORD":
                if token.value == "say":
                    self.parsed.append(self.parse_say())

                elif token.value == "get":
                    self.parsed.append(self.parse_get())

                elif token.value == "check":
                    self.parsed.append(self.parse_check())

            elif token.type == "IDENTIFIER":
                self.parsed.append(self.parse_set_variable())

            else:
                self.advance()

        return self.parsed
