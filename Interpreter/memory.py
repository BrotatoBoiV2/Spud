"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                Programmer: Aaron "A.J." Cassell. (@BrotatoBoi)
                        Program Name: Spud Language.
                     Description: My custom language.
                             File: memory.py
                            Date: 2026/01/08
                        Version: 1.9.7-2026.01.20

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


class Environment:
    """
    ~ Represents the variable environment in the AST. ~

    Functions:
        - __init__                     : Initializes the environment.
        - get                          : Get a variable from the environment.
        - set_var                      : Set a variable in the environment.
    """

    def __init__(self, parent=None):
        """
        ~ Initialize the Environment. ~

        Arguments:
            - parent     (Environment) : The parent environment.

        Attributes:
            - variables         (Dict) : The variables in the environment.
            - parent     (Environment) : The parent environment.
        """

        self.variables = {}
        self.parent    = parent

    def get(self, name):
        """
        ~ Get a variable from the environment. ~

        Arguments:
            - name            (String) : The name of the variable.

        Returns:
            - Any                      : The value of the variable.
        """

        if name in self.variables:
            return self.variables[name]

        if self.parent:
            return self.parent.get(name)

        raise NameError(f"Variable '{name}' not found.")

    def set_var(self, name, value):
        """
        ~ Set a variable in the environment. ~

        Arguments:
            - name            (String) : The name of the variable.
            - value              (Any) : The value of the variable.
        """

        self.variables[name] = value
