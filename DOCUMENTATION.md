*Note:* All time is in **UTC**.

---

## Weekly Plan
    *Week Date:* 2026-01-05/2026-01-09

    Expected output:
        Able to run the test file and have each line function as intended.

        test.pot:
        ```
        (~ This is a comment. ~)
        count = 10
        say "The result of 'count' is: " count + 1
        say "throw an error here
        ```

        When that is done I can move on to the next version of the interpreter.

    Path:
        Start off with comments (DONE)
        Then move onto the `say` keyword and allowing strings (DONE)
        Then allow for setting and manipulating variables (IN-PROGESS)
        Introduce variable expansions (DONE)
        Have string concationation and allow for int to string conversion (IN-PROGRESS)
        Allow for error handling (IN-PROGRESS)

    What is next?
        Loops

        While loops are the first thing to start with.

---

## Developers Log
2026-01-02:
    19:18
        Initially creating the programs structure.

    19:43
        Created the initial structure and the skeleton for the `main.py` file.

    19:48
        The skeleton for the `tokenizer.py` file is complete.

    19:50
        Both files `executor.py` and `parser.py` have base skeletons.

2026-01-03:
    04:46
        Test files have been written for the tokenizer.

    05:32
        The tokenizer is capable of tokenizing a comment, the `say` keyword and strings.

    19:06
        Fixed aome identifier errors like double spaces and root words. (i.e.: say -> saying)

2026-01-04:
    19:45
        Updated the say function so that it is now able to handle string concatenation and integers.

2026-01-05:
    05:52
        Created the GetNode so now input can be received from the user.
        I suspect the VARIABLE handling may be fragile, but I will cross that bridge when I come to it.

    15:14
        Started to plan out how the VARIABLES are going to be set.

    17:27
        Basic variables can be created: `var_name = value`.
        Need to make it more robust though.

    18:20
        Created a part iterator helpr method in `nodes.py` to help with variable expansion.

2026-01-06:
    14:57
        Started to work on enforcing string concatenation so I can add functionality to keywords later. I need to test if this works for other keywords and such.

2026-01-07:
    16:25
        Noticed there was an error with the update running the examples, but patched them.
        The `parse_set_variable` method was not sending Nodes, and that broke functionality.
        Now it is handled a bit better and can pass the existing examples.

    16:47
        Created a new example file to display math with variables.
        It currently has issues with type conversion but that should be an easy fix!

    19:22
        Fixed the `join_parts` method to allow mathematical equations - Addition.
        Need to add more operators in the future.
        The math example now functions as intended!
        I need to have the math expanded `5 + 2 + 3` etc.
---

# TO-DO:
    ***** FIRST ERROR SHOULD BE UNCLOSED QUOTE.
    *** Make errors fully understandable.
    *** Have parts helper method in `nodes.py` rewritten to force string concatenation: `"string" + variable` instead of `"string" variable` (IN-PROGRESS)
    ** Make larger mathematical expressions work: `5 + 2 + 3` etc.
    * Handle variables: set them and manipulate them. (IN-PROGRESS)
