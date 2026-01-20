"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                Programmer: Aaron "A.J." Cassell. (@BrotatoBoi)
                        Program Name: Spud Language.
                     Description: My custom language.
                             File: nodes.py
                            Date: 2026/01/02
                        Version: 2.0.7-2026.01.20

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


from memory import Environment


def join_parts(parts, memory):
    """
    ~ Join the parts of the expression. ~

    Arguments:
        - parts                 (Node) : The parts of the expression.
        - memory         (Environment) : The memory environment.

    Returns:
        - String                       : The joined expression.
    """

    if not parts:
        return None

    return parts.execute(memory)


class Node:
    """
    ~ Represents a node in the AST. ~

    Functions:
        - __init__                     : Initializes the node.
        - execute                      : Executes the node.
    """

    def __init__(self, value, row, column):
        """
        ~ Initialize the Node. ~

        Arguments:
            - value          (Unknown) : The value of the node.
            - row                (Int) : The row number of the node.
            - column             (Int) : The column number of the node

        Attributes:
            - value           (String) : The value of the node.
        """

        self.value  = value
        self.row    = row
        self.column = column

    def execute(self, memory):
        """
        ~ Execute the node. ~

        Arguments:
            - memory     (Environment) : The memory environment.
        """

        pass


class IntegerNode(Node):
    """
    ~ Represents an integer node in the AST. ~

    Functions:
        - __init__                     : Initializes the integer node.
        - execute                      : Executes the integer node.
    """

    def __init__(self, value, row, column):
        """
        ~ Initialize the IntegerNode. ~

        Arguments:
            - value           (String) : The value of the integer node.
            - row                (Int) : The row number of the integer node.
            - column             (Int) : The column number of the integer node.
        """

        super().__init__(value, row, column)

    def execute(self, memory):
        """
        ~ Execute the integer node. ~

        Arguments:
            - memory     (Environment) : The memory environment.

        Returns:
            - Int                      : The value of the integer node.
        """

        return int(self.value)


class StringNode(Node):
    """
    ~ Represents a string node in the AST. ~

    Functions:
        - __init__                     : Initializes the string node.
        - execute                      : Executes the string node.
    """

    def __init__(self, value, row, column):
        """
        ~ Initialize the StringNode. ~

        Arguments:
            - value           (String) : The value of the string node.
            - row                (Int) : The row number of the string node.
            - column             (Int) : The column number of the string node.
        """

        super().__init__(value, row, column)

    def execute(self, memory):
        """
        ~ Execute the string node. ~

        Arguments:
            - memory     (Environment) : The memory environment.

        Returns:
            - String                   : The value of the string node.
        """

        return str(self.value)


class BinOperNode(Node):
    """
    ~ Represents a binary operation node in the AST. ~

    Functions:
        - __init__                     : Initializes the binary operation node.
        - execute                      : Executes the binary operation node.
    """

    def __init__(self, value, left, right, row, column):
        """
        ~ Initialize the BinOperNode. ~

        Arguments:
            - value           (String) : The value of the node.
            - left              (Node) : The left child of the node.
            - right             (Node) : The right child of the node.
            - row                (Int) : The row number of the node.
            - column             (Int) : The column number of the  node.

        Attributes:
            - left              (Node) : The left child of the node.
            - right             (Node) : The right child of the node.
        """

        super().__init__(value, row, column)

        self.left  = left
        self.right = right

    def execute(self, memory):
        """
        ~ Execute the BinOperNode. ~

        Arguments:
            - memory     (Environment) : The memory environment.

        Returns:
            - Any                      : The value of the node.
        """

        left  = self.left.execute(memory)
        right = self.right.execute(memory)

        if self.value == "+":
            if isinstance(left, int) and isinstance(right, int):
                return int(left) + int(right)

            return str(left) + str(right)

        elif self.value == "-":
            if isinstance(left, int) and isinstance(right, int):
                return int(left) - int(right)

            error = "Cannot subtract strings"
            location = f"row: {self.row} ; Column:{self.col}"

            raise ValueError("Error: " + error + "\n" + location)

        elif self.value == "*":
            if isinstance(left, int) and isinstance(right, int):
                return int(left) * int(right)

            elif isinstance(left, str) and isinstance(right, int):
                return str(left) * int(right)

            error = "Cannot multiply strings"
            location = f"row: {self.row} ; Column:{self.col}"

            raise ValueError("Error: " + error + "\n" + location)

        elif self.value == "/":
            if isinstance(left, int) and isinstance(right, int):
                return int(left) / int(right)

            error = "Cannot divide strings"
            location = f"row: {self.row} ; Column:{self.col}"

            raise ValueError("Error: " + error + "\n" + location)
            
        elif self.value == "#":
            if isinstance(left, int) and isinstance(right, int):
                return int(left) // int(right)

            error = "Cannot mash strings together!"
            location = f"row: {self.row} ; Column:{self.col}"

            raise ValueError("Error: " + error + "\n" + location)

        elif self.value == "%":
            if isinstance(left, int) and isinstance(right, int):
                return int(left) % int(right)

            error = "Cannot get remainder of strings"
            location = f"row: {self.row} ; Column:{self.col}"

            raise ValueError("Error: " + error + "\n" + location)
            

        error = f"Invalid operator: {self.value}"
        location = f"row: {self.row}"

        raise ValueError("Error: " + error + "\n" + location)


class VariableNode(Node):
    """
    ~ Represents a variable node in the AST. ~

    Functions:
        - __init__                     : Initializes the variable node.
        - execute                      : Executes the variable node.
    """

    def __init__(self, value, row, column, value_parts=None):
        """
        ~ Initialize the VariableNode. ~

        Arguments:
            - value           (String) : The value of the variable node.
            - row                (Int) : The row number of the variable node.
            - column             (Int) : The column number of the node.
            - value_parts       (Node) : The value parts of the variable node.

        Attributes:
            - value_parts       (Node) : The value parts of the variable node.
        """

        super().__init__(value, row, column)

        self.value_parts = value_parts

    def execute(self, memory):
        """
        ~ Execute the VariableNode. ~

        Arguments:
            - memory     (Environment) : The memory environment.

        Returns:
            - Any                      : The value of the variable node.
        """

        
        if not self.value_parts:
            value = memory.get(self.value)

            if value is not None:
                if isinstance(value, PotNode):
                    return value.execute(memory)

                return value

            error = f"Variable {self.value} is not defined."
            location = f"row: {self.row} ; Column:{self.col}"

            raise ValueError("Error: " + error + "\n" + location)

        else:
            if isinstance(self.value_parts, PotNode):
                memory.set_var(self.value, self.value_parts)
            else:
                value = join_parts(self.value_parts, memory)
                memory.set_var(self.value, value)


class SayNode(Node):
    """
    ~ Represents a say node in the AST. ~

    Functions:
        - __init__                     : Initializes the say node.
        - execute                      : Executes the say node.
    """

    def __init__(self, value, row, column):
        """
        ~ Initialize the SayNode. ~

        Arguments:
            - value             (Node) : The value of the say node.
            - row                (Int) : The row number of the say node.
            - column             (Int) : The column number of the say node
        """

        super().__init__(value, row, column)

    def execute(self, memory):
        """
        ~ Execute the SayNode. ~

        Arguments:
            - memory     (Environment) : The memory environment.
        """

        prompt = join_parts(self.value, memory)

        print(prompt, end="", flush=True)


class GetNode(Node):
    """
    ~ Represents a get node in the AST. ~

    Functions:
        - __init__                     : Initializes the get node.
        - execute                      : Executes the get node.
    """

    def __init__(self, value, prompt, row, column):
        """
        ~ Initialize the GetNode. ~

        Arguments:
            - value           (String) : The value of the get node.
            - prompt            (Node) : The prompt of the get node.
            - row                (Int) : The row number of the get node.
            - column             (Int) : The column number of the get node

        Attributes:
            - prompt            (Node) : The prompt of the get node.
        """

        super().__init__(value, row, column)

        self.prompt = prompt

    def execute(self, memory):
        """
        ~ Execute a GetNode.~

        Arguments:
            - memory     (Environment) : The memory environment.
        """

        is_num = True
        prompt = join_parts(self.prompt, memory) if self.prompt else ""
        value  = input(prompt)

        if not value:
            error = "No value provided."
            location = f"row: {self.row} ; Column:{self.col}"

            raise ValueError("Error: " + error + "\n" + location)

        for val in value:
            if not val.isdigit():
                is_num = False
                break

        if is_num:
            value = int(value)

        memory.set_var(self.value, value)


class BoolNode(Node):
    """
    ~ Represents a boolean node in the AST. ~

    Functions:
        - __init__                     : Initializes the boolean node.
        - execute                      : Executes the boolean node.
    """

    def __init__(self, value, row, column, left=None, right=None):
        """
        ~ Initialize the BoolNode. ~

        Arguments:
            - left              (Node) : The left side of the bool node.
            - right             (Node) : The right side of the bool node.

        Returns:
            - Boolean                  : The value of the bool node.
        """

        super().__init__(value, row, column)

        self.left  = left
        self.right = right

    def execute(self, memory):
        if self.value == "equals":
            return self.left.execute(memory) == self.right.execute(memory)
        elif self.value == "not":
            return not self.left.execute(memory) == self.right.execute(memory)
        elif self.value == "below":
            return self.left.execute(memory) < self.right.execute(memory)
        elif self.value == "above":
            return self.left.execute(memory) > self.right.execute(memory)
        elif self.value == "ripe" or self.value == "true":
            return True
        elif self.value == "rotten" or self.value == "false":
            return False


class LogicNode(Node):
    """
    ~ Represents a logic node in the AST. ~

    Functions:
        - __init__                     : Initializes the logic node.
        - execute                      : Executes the logic node.
    """

    def __init__(self, value, row, column):
        """
        ~ Initialize the LogicNode. ~

        Returns:
            - String                   : The value of the logic node.
        """

        super().__init__(value, row, column)

    def execute(self, memory):
        return self.value


class CheckNode(Node):
    """
    ~ Represents a check node in the AST. ~

    Functions:
        - __init__                     : Initializes the check node.
        - execute                      : Executes the check node.
    """

    def __init__(self, value, row, column):
        super().__init__(value, row, column)

    def execute(self, memory):
        run = None

        for condition, code in self.value.items():
            if condition.execute(memory):
                run = code

                break

        if run:
            for node in run:
                node.execute(memory)

class CutNode(Node):
    def __init__(self, value, row, column):
        super().__init__(value, row, column)

    def execute(self, memory):
        raise Exception()

class LoopNode(Node):
    """
    ~ Represents a loop node in the AST. ~

    Functions:
        - __init__                     : Initializes the loop node.
        - execute                      : Executes the loop node.
    """

    def __init__(self, value, row, column):
        super().__init__(value, row, column)

    def execute(self, memory):
        condition = self.value[0]
        code      = self.value[1]
        run_code = True

        while True:
            for node in code:
                try:
                    node.execute(memory)
                except Exception:
                    run_code = False
                    break

            if not condition.execute(memory) or not run_code:
                break


class PotNode(Node):
    """
    ~ Represents a pot node in the AST. ~

    Functions:
        - __init__                     : Initializes the pot node.
        - execute                      : Executes the pot node.
    """

    def __init__(self, value, row, column):
        super().__init__(value, row, column)

    def execute(self, memory):
        env = Environment()
        env.parent = memory

        for node in self.value:
            node.execute(env)

