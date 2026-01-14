**Note:** All time is in *UTC*.

---

## Weekly Plan
**Week Date:** *2026-01-12/2026-01-16*

Essentially all I need to do is refactor the code and make sure
the examples work as intended.

**Next Plan:**
*** Conditionals (Next Week)
** Loops (After Conditionals)
* Functions (After Loops)

---

## Developers Log
*2026-01-02:*
* 19:18
    - Initially creating the programs structure.
* 19:43
    - Created the initial structure and the skeleton 
        for the `main.py` file.
* 19:48
    - The skeleton for the `tokenizer.py` file is complete.
* 19:50
    - Both files `executor.py` and `parser.py` have base skeletons.

*2026-01-03:*
* 04:46
    - Test files have been written for the tokenizer.
* 05:32
    - The tokenizer is capable of tokenizing a comment, 
        the `say` keyword and strings.
* 19:06
    - Fixed aome identifier errors like double spaces and root words.
            (i.e.: say -> saying)

*2026-01-04:*
* 19:45
    - Updated the say function so that it is now able to handle string
        concatenation and integers.

*2026-01-05:*
* 05:52
    - Created the GetNode so now input can be received from the user.
    - I suspect the VARIABLE handling may be fragile,
        but I will cross that bridge when I come to it.
* 15:14
    - Started to plan out how the VARIABLES are going to be set.
* 17:27
    - Basic variables can be created: `var_name = value`.
    - Need to make it more robust though.
* 18:20
    - Created a part iterator helper method in `nodes.py` to help with
        variable expansion.

*2026-01-06:*
* 14:57
    - Started to work on enforcing string concatenation so I can add 
        functionality to keywords later. I need to test if this
        works for other keywords and such.

*2026-01-07:*
* 16:25
    - Noticed there was an error with the update running the examples, 
        but patched them.
    - The `parse_set_variable` method was not sending Nodes, 
        and that broke functionality.
    - Now it is handled a bit better and can pass the existing examples.
* 16:47
    - Created a new example file to display math with variables.
    - It has issues with type conversion but that should be an easy fix!
* 19:22
    - Fixed the `join_parts` method to allow mathematical equations.
    - Need to add more operators in the future.
    - The math example now functions as intended!
    - I need to have the math expanded `5 + 2 + 3` etc.
* 20:32
    - Made the math expressions a bit more robust for the following code:
            '''spud
            `say "2 + 2 = " + 2+2`
            '''
* 20:40
    - Updated to version 0.8-2026.01.07 in the Changelogs and filestamps.

*2026-01-08:*
* 04:08
    - Introduced the first error of an unterminated string.
* 04:50
    - Updated errors and how their output is returned to the screen.
* 17:50
    - Included a '--debug' flag to allow for more verbose output.
    - Some errors were introduced like Unknown Identifiers and such.
* 20:20
    - `OperatorNode` was replaced by a more robust `BinOperNode` which
        also simplified the 'join_parts' method.
    - I need to allow for chaining of operators like `5 + 2 + 3 + 4 + 1`
* 21:02
    - Comments are now enforced to be closed. Also, pretty sure I got
        a majority of the possible errors, but I need to test more.
* 21:13
    - Existing keywords are not not allowed to be assigned to.
* 21:20
    - Created the `memory.py` file to handle variable memory.

*2026-01-09:*
* 04:46
    - Created a memory environment to handle variable memory, 
        so it is no longer fragile.
* 04:50
    - Updated to version 1.0-2026.01.09 in the Changelogs and filestamps.
* 18:58
    - Updated the parser to allow for cleaner code and chained 
        mathematical operations.
* 19:44
    - Included parentheses for more complex mathematical operations.

*2026-01-12:*
* 15:20
    - Cleaned and rewritten `main.py`, moving onto the `tokenizer.py` file.
* 16:50
    - Finished refactoring the `tokenizer.py` file, will move on to the
        `parser.py` file after a break.
* 17:50
    - Changed error output to the prefered version:
        ```
        Error: {error}
        Row: {row} ; Column: {column}
        ```
      Need to add output for the line in question.
* 19:32
    - Refactored the `parser.py` file, now going to the `nodes.py` file.
*20:10
    - Finished refactoring the `nodes.py` file.
*20:20
    - Entire codebase has now been refactored and is ready to be tested.
    - Updated changelog to version 1.1.1-2026.01.12 and in the filestamps.

*2026-01-13:*
* 14:50
    - Started to clean up the docstrings and comments while linting the code with:
        [Black Formatter](https://github.com/microsoft/vscode-black-formatter)
* 15:09
    - Cleaned both the `main.py` and `parser.py` files.
    - Moving onto the `tokenizer.py` file now.
* 15:11
    - It was already cleaned and up to par, but I need to add more comments.
    - Perhaps most of the modules could benefit from more comments.
    - Moving onto the `nodes.py` file, then afterward 
      the `memory.py` file and a short break.
* 15:23
    - `nodes.py` was linted and cleaned, now the final one before a line check.
* 15:26
    - All files have been cleaned and linted, now for the line check.
* 15:35
    - All modules seem to have no lines exceeding 80 characters long.
    - Now pushing, taking a short break and planning out
      the next feature - Conditionals.

*2026-01-14*
* 05:15
    - Implemented a basic conditional statement.
* 06:18
    - Fixed tildentation.
    - Need to add 'but' keyword.
* 17:03
    - Starting to implement the `but` keyword.
* 18:00
    - The `but` keyword is now working, but the logic is slightly flawed.
       (All `check-but-otherwise` all run instead of only one at a time)
* 21:20
    - The check node now processes as a normal `if-elif-else` conditional.
    - Implemented the `otherwise` keyword as a fallback condition.
---

# TO-DO:
\*\*\*Add Line output to the errors.\*\*\*
\*Include a bit more commentation.\*
    
