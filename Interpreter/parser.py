"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                Programmer: Aaron "A.J." Cassell. (@BrotatoBoi)
                        Program Name: Spud Language.
                     Description: My custom language.
                            File: parser.py
                            Date: 2026/01/02
                        Version: 2.3.7-2026.01.21

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
    LogicNode, BoolNode, CheckNode, LoopNode, CutNode, PotNode, BloomNode
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
        - parse_loop                   : Parse a loop statement.
        - parse_code                   : Parse a block of code.
    """

    def __init__(self):
        """
        ~ Initialize the Parser. ~

        Attributes:
			- index              (Int) : The current index in the tokens.
			- tokens            (List) : The list of tokens.
			- token            (Token) : The current token.
        """

        self.index   = 0
        self.tokens  = None
        self.token   = None

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
            if self.peek(1).type == "LPARAM":
                # print("SHatwoth")
                args = []
                self.advance()

                while True:
                    self.advance()
                    arg = self.parse_expression()
                    args.append(arg)

                    if not arg or self.token.type == "RPARAM":
                        self.advance()
                        break                    

                value = {
                    "action": "run",
                    "content": {
                        "name": token.value,
                        "args": args
                    }
                }
                
                return VariableNode(value, token.row, token.col)

            self.advance()
            value = {
                "action": "get",
                "content": {
                    "name": token.value
                }
            }
            return VariableNode(value, token.row, token.col)

        elif token.type == "LPARAM":
            self.advance()
            node = self.parse_expression()

            if self.token.type != "RPARAM":
                error = "Expected ')' after expression."
                location = f"row: {self.token.row} ; Column:{self.token.col}"

                raise SyntaxError("Error: " + error + "\n" + location)

            self.advance()
            return node

        elif token.type == "RPARAM":
            error = "Found a ')' that does not close an expression."
            location = f"row: {self.token.row} ; Column:{self.token.col}"

            raise SyntaxError("Error: " + error + "\n" + location)

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
            error = "Expected identifier after 'get'."
            location = f"row: {self.token.row} ; Column:{self.token.col}"

            raise SyntaxError("Error: " + error + "\n" + location)

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

        self.advance()

        exp = self.parse_expression()

        value = {
            "action": "set",
            "content": {
                "name": var_name,
                "value": exp
            }
        }

        return VariableNode(value, row, col)

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

    def parse_check(self):
        """
        ~ Parse a conditional statement block. ~

        Returns:
			- CheckNode                : The parsed statement block.
        """
        err = "A `check` block needs to be started with some Potato Eyes! '.~'"
        
        while self.index < len(self.tokens):
            self.advance()

            cond = self.parse_condition()

            code      = []

            # ~ Make sure the condition exists. ~ #
            if cond:
                if self.token.type == "EYES":
                    self.advance()

                    branches = self.parse_code(is_check=True, condition=cond)

                    return CheckNode(branches, self.token.row, self.token.col)

                else:
                    loc = f"row: {self.token.row} ; Column:{self.token.col}"

                    raise SyntaxError("Error: " + err + "\n" + loc)

            self.advance()

    def parse_loop(self):
        """
        ~ Parse a loop statement. ~

        Returns:
			- LoopNode                 : The parsed loop statement.
        """

        err = "A `loop` block needs to be started with some Potato Eyes! '.~'"

        while self.index < len(self.tokens):
            self.advance()

            condition = self.parse_condition()

            code      = []

            # ~ Make sure the condition exists. ~ #
            if condition:
                if self.token.type == "EYES":
                    self.advance()
                    code = self.parse_code()
                    value = [condition, code]

                    return LoopNode(value, self.token.row, self.token.col)

                else:
                    loc = f"row: {self.token.row} ; Column:{self.token.col}"

                    raise SyntaxError("Error: " + err + "\n" + loc)

    def parse_pot(self):
        """
        ~ Parse a pot statement. ~

        Returns:
			- PotNode                   : The parsed pot statement.
        """

        pot_name = ""
        code = []
        args = []

        self.advance()

        if self.token.type == "IDENTIFIER":
            pot_name = self.token.value

            self.advance()

            if self.token.type == "LPARAM":
                while True:
                    self.advance()

                    if self.token.type == "RPARAM":
                        self.advance()
                        break
                    
                    args.append(self.token.value)

            if self.token.type == "EYES":
                code = self.parse_code()

            else:
                err = "Unexpected token after `pot` declaration."
                location = f"row: {self.token.row} ; Column:{self.token.col}"

                raise SyntaxError("Error: " + err + "\n" + location)

        pot_value = {
            "name": pot_name,
            "args": args, 
            "code": code,
        }

        pot = PotNode(pot_value, self.token.row, self.token.col)
        pot_value["potNode"] = pot

        # VariableNode(var_value, self.token.row, self.token.col).hidden()
        return pot
        # return VariableNode(var_value, self.token.row, self.token.col)

    def parse_code(self, is_check=False, condition=None):
        """
        ~ Parse a block of code. ~

        Attributes:
            - is_check       (Boolean) : Whether the block is a check block.
            - condition         (Node) : The condition for the check block.


        Returns:
			- List                     : The parsed block of code.
        """

        code = []
        branches = {}

        while self.token.type != "EOF":
            token = self.token
            
            if token.type == "ROOT":
                self.advance()
                break

            if token.type == "KEYWORD":
                if token.value == "say":
                    code.append(self.parse_say())

                elif token.value == "get":
                    code.append(self.parse_get())

                elif token.value == "check":
                    code.append(self.parse_check())
                
                elif token.value == "loop":
                    code.append(self.parse_loop())

                elif token.value == "cut":
                    code.append(CutNode(None, self.token.row, self.token.col))
                    self.advance()

                elif token.value == "pot":
                    code.append(self.parse_pot())

                elif token.value == "bloom":
                    self.advance()
                    exp = self.parse_expression()
                    code.append(BloomNode(exp, token.row, token.col))
                    self.advance()


                if is_check:
                    if token.value == "instead":
                        branches[condition] = code
                        code                = []

                        self.advance()
                        condition = self.parse_condition()

                    elif token.value == "otherwise":
                        branches[condition] = code
                        code                = []

                        self.advance()
                        condition           = BoolNode(
                                    "ripe",
                                    self.token.row,
                                    self.token.col
                        )

            elif token.type == "IDENTIFIER":
                # print(self.token)
                if self.peek(1).type == "EQUAL":
                    code.append(self.parse_set_variable())
                    self.advance()
                elif self.peek(1).type == "LPARAM":
                    self.advance()

                    args = []

                    while True:
                        self.advance()

                        if self.token.type == "RPARAM":
                            self.advance()
                            break

                        args.append(self.token.value)

                    value = {
                        "action": "run",
                        "content": {
                            "name": token.value,
                            "args": args
                        }
                    }
                    print("GOLF")
                    code.append(VariableNode(value, token.row, token.col))
                    self.advance()
                else:
                    self.advance()

            else:
                self.advance()

        if is_check:
            branches[condition] = code
            return branches

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
        parsed = self.parse_code()

        return parsed
