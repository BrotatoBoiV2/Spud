# Spud Language

## Summary
Spud is an experimental programming language. Currently, it is a high-level interpreted language designed for ease of use. The long-term roadmap is to evolve Spud into a low-level, self-hosted systems language capable of building operating systems and low-level graphical software.

## Current Features (v1.1)
  * Recursive Expression Parsing: Supports complex mathematical operations including addition and string concatenation.
  * Operation Grouping: Full support for parentheses `( )` to control operator precedence.
  * Variable Scoping: Implements a Lexical Environment system via `memory.py` for robust variable management.
  * Dynamic Type Coercion: Automatically handles integer and string conversions for seamless `say` output.
  * Interactive Input: Capture user input with the `get` keyword, featuring automatic numeric detection.
  * Informative Error Handling: Detects unterminated strings and unclosed comments (`(~` `~)`) during tokenization.

---

## Additional Information
See the [LICENSE](LICENSE) for licensing details.  
Documentation is available in the [DOCUMENTATION](docs/DOCUMENTATION.md) and recent changes can be found in the [CHANGELOG](docs/CHANGELOG.md).

## Important Notes
This project is created by a human developer and supported with AI-assisted tooling.
