"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                Programmer: Aaron "A.J." Cassell. (@BrotatoBoi)
                        Program Name: Spud Language.
                     Description: My custom language.
                           File: tokenizer.py
                            Date: 2026/01/02
                        Version: 0.0-2026.01.02

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


class Tokenizer:
    def __init__(self):
        pass

    def tokenize(self, code):
        index = 0
        ident = ""
        tokens = []
        in_comment = False
        in_string = False

        while index < len(code):
            token = code[index]

            if token.isalpha():
                if in_comment or in_string:
                    while True:
                        if not (token == " " and (code[index+1] == '"' or code[index+1] == "~")):
                            ident += token
                        index += 1
                        token = code[index]

                        if token == '"' or token == "~" and code[index+1] == ")":
                            break
                else:
                    ident += token

            if token == "(" and code[index+1] == "~":
                index += 1
                in_comment = True

            elif token == "~" and code[index+1] == ")":
                in_comment = False
                tokens.append(f"COMMENT({ident})")
                ident = ""
                index += 1

            elif token == '"':
                if not in_string:
                    in_string = True
                else:
                    tokens.append(f"STRING({ident})")
                    ident = ""
                    in_string = False

            elif ident == "say":
                tokens.append(f"SAY")
                ident = ""

            index += 1

        return tokens

