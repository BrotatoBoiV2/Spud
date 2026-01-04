*Note:* All time is in **UTC**.

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
        Start off with comments
        Then move onto the `say` keyword and allowing strings
        Then allow for setting variables
        Introduce variable expansions
        Have string concationation and allow for int to string conversion
        Allow for error handling

    What is next?
        Loops

        While loops are the first thing to start with.

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


# TO-DO:
    * Handle user input
    * Handle variables
    * Make the parser return Nodes to process.
