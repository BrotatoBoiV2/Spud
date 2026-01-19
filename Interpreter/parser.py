"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                Programmer: Aaron "A.J." Cassell. (@BrotatoBoi)
                        Program Name: Spud Language.
                     Description: My custom language.
                            File: parser.py
                            Date: 2026/01/02
                        Version: 1.9.6-2026.01.19

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
    LogicNode, BoolNode, CheckNode, LoopNode, CutNode
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
        - parse_condition              : Parse a condition.
		- parse_check                  : Parse a 'check' statement.
        - parse_branch                 : Parse a conditional statement branch.
    """

    def __init__(self):
        """
        ~ Initialize the Parser. ~

        Attributes:
			- index              (Int) : The current index in the tokens.
			- tokens            (List) : The list of tokens.
			- token            (Token) : The current token.
			- parsed            (List) : The list of parsed nodes.
        """

        self.index   = 0
        self.tokens  = None
        self.token   = None
        self.sprouts = 0

    def peek(self, amount=0):
        """
        ~ Peek at the next token. ~

        Arguments:
			- amount             (Int) : The amount to peek ahead.

        Returns:
			- Token                    : The next token to process.
            - String                   : Empty string to avoid errors.
        """

        if self.tokens and self.index + amount < len(self.tokens):
            return self.tokens[self.index + amount]

        return ""

    def advance(self, amount=1):
        """
        ~ Advance to the next token. ~

        Arguments:
			- amount             (Int) : The amount to advance.
        """

        self.index += amount
        self.token  = self.peek()

        if not self.token:
            self.token = Token("EOF", "EOF", None, None)

    def parse_say(self):
        """
        ~ Parse a 'say' statement. ~

        Returns:
			- SayNode                  : The parsed 'say' statement.
        """
        output    = []
        row, col = self.token.row, self.token.col
        
        self.advance()

        return SayNode(self.parse_expression(), row, col)

    def parse_expression(self):
        """
        ~ Parse an expression. ~

        Returns:
			- BinOperNode              : The parsed expression.
        """

        left = self.parse_primary()

        while self.token.type == "OPERATOR":
            oper  = self.token.value
            self.advance()

            right = self.parse_primary()
            left  = BinOperNode(
                oper,
				left,
				right,
				self.token.row,
				self.token.col
			)

        return left

    def parse_primary(self):
        """
        ~ Parse a primary expression. ~

        Returns:
			- Node                     : The node based on the token.
        """

        token = self.token

        if token.type == "INTEGER":
            self.advance()
            return IntegerNode(token.value, token.row, token.col)

        elif token.type == "STRING":
            self.advance()
            return StringNode(token.value, token.row, token.col)

        elif token.type == "IDENTIFIER":
            self.advance()
            return VariableNode(token.value, token.row, token.col)

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
            return LogicNode(token.value, token.row, token.col)
        
        elif token.type == "BOOL":
            self.advance()
            return BoolNode(token.value, token.row, token.col)

    def parse_get(self):
        """
        ~ Parse a 'get' statement. ~

        Returns:
			- GetNode                  : The parsed 'get' statement.
        """

        self.advance()
        var_name = ""
        prompt   = ""

        if self.token.type == "IDENTIFIER":
            var_name = self.token.value
            self.advance()

        else:
            raise SyntaxError("Expected identifier after 'get'.")

        if self.token.type not in ["EOL", "EOF"]:
            prompt = self.parse_expression()

        return GetNode(var_name, prompt, self.token.row, self.token.col)

    def parse_set_variable(self):
        """
        ~ Parse a variable assignment. ~

        Returns:
			- VariableNode             : The parsed variable assignment.
        """

        var_name        = self.token.value
        row, col       = self.token.row, self.token.col
        
        self.advance()

        # if self.token.type != "EQUAL":
        #     raise SyntaxError("Expected '=' after variable name.")

        self.advance()

        expression_tree = self.parse_expression()

        return VariableNode(var_name, row, col, value_parts=expression_tree)

    def parse_condition(self):
        """
        ~ Parse a condition. ~

        Returns:
			- BoolNode                 : The parsed condition for check node.
        """
        
        left = self.parse_expression()


        while self.token.type == "LOGIC":
            logic = self.token.value
            self.advance()

            right = self.parse_expression()

            left  = BoolNode(
                logic,
                self.token.row,
                self.token.col,
                left=left,
                right=right
            )

        return left

    def parse_branch(self, condition):
        """
        ~ Parse a conditional statement branch. ~

        Arguments:
			- condition         (Node) : The condition of the branch.
            - code              (List) : The code of the branch.

        Returns:
			- Dict                     : The branches of the check node,
        """

        branches            = {}
        code = []

        while self.token.type != "ROOT":
            if self.token.type == "EOF":
                raise SyntaxError("Potato Eyes needs to be closed with a Potato Root! '~.'")

            if self.token.type == "KEYWORD":
                if self.token.value == "say":
                    code.append(self.parse_say())

                elif self.token.value == "get":
                    code.append(self.parse_get())

                elif self.token.value == "check":
                    code.append(self.parse_check())

                elif self.token.value == "instead":
                    branches[condition] = code
                    code                = []

                    self.advance()
                    condition = self.parse_condition()

                elif self.token.value == "otherwise":
                    branches[condition] = code
                    code                = []
                    
                    self.advance()
                    condition           = BoolNode(
                                "ripe",
                                self.token.row,
                                self.token.col
                    )

                elif self.token.value == "cut":
                    code.append(CutNode(self.token.row, self.token.col))


            elif self.token.type == "IDENTIFIER":
                code.append(self.parse_set_variable())

            self.advance()

        branches[condition] = code

        return branches


    def parse_check(self):
        """
        ~ Parse a conditional statement block. ~

        Returns:
			- CheckNode                : The parsed statement block.
        """

        while self.index < len(self.tokens):
            self.advance()

            condition = self.parse_condition()

            code      = []

            # ~ Make sure the condition exists. ~ #
            if condition:
                if self.token.type == "EYES":
                    nest = self.sprouts
                    self.sprouts += 1
                    self.advance()

                    branches = self.parse_branch(condition)

                    return CheckNode(branches, self.token.row, self.token.col)

                else:
                    raise SyntaxError("A `check` block needs to be started with some Potato Eyes! '.~'")

            self.advance()

    def parse_loop(self):
        """
        ~ Parse a loop statement. ~

        Returns:
			- LoopNode                 : The parsed loop statement.
        """

        while self.index < len(self.tokens):
            self.advance()

            condition = self.parse_condition()

            code      = []

            # ~ Make sure the condition exists. ~ #
            if condition:
                if self.token.type == "EYES":
                    self.sprouts += 1
                    self.advance()
                    code = self.parse_code()
                    value = [condition, code]

                    return LoopNode(value, self.token.row, self.token.col)

                else:
                    raise SyntaxError("A `loop` block needs to be started with some Potato Eyes! '.~'")

    def parse_code(self):
        code = []

        while self.token.type != "ROOT":
            if self.token.type == "EOF":
                raise SyntaxError("Potato Eyes needs to be closed with a Potato Root! '~.'")
            
            if self.token.type == "KEYWORD":
                if self.token.value == "say":
                    code.append(self.parse_say())

                elif self.token.value == "get":
                    code.append(self.parse_get())

                elif self.token.value == "check":
                    code.append(self.parse_check())

                elif self.token.value == "instead":
                    branches[condition] = code
                    code                = []

                    self.advance()
                    condition = self.parse_condition()

                elif self.token.value == "otherwise":
                    branches[condition] = code
                    code                = []
                    
                    self.advance()
                    condition           = BoolNode(
                                "ripe",
                                self.token.row,
                                self.token.col
                    )

                elif self.token.value == "cut":
                    code.append(CutNode(self.token.row, self.token.col))

            elif self.token.type == "IDENTIFIER":
                code.append(self.parse_set_variable())

            self.advance()

        return code


    def parse(self, tokens):
        """
        ~ Parse the source code gotten from the file. ~

        Arguments:
			- tokens            (List) : The list of tokens in the source code.

        Returns:
			- List                     : The list of parsed nodes to execute.
        """

        self.tokens = tokens
        self.token  = self.peek() or Token("EOF", "EOF", None, None)
        parsed = []

        # for token in self.tokens:
        #     print(token)

        while self.token.type != "EOF":
            token = self.token

            if token.type == "KEYWORD":
                if token.value == "say":
                    parsed.append(self.parse_say())

                elif token.value == "get":
                    parsed.append(self.parse_get())

                elif token.value == "check":
                    parsed.append(self.parse_check())
                
                elif token.value == "loop":
                    parsed.append(self.parse_loop())

            elif token.type == "IDENTIFIER":
                parsed.append(self.parse_set_variable())

            else:
                self.advance()

        return parsed
