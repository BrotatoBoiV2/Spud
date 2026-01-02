# Spud Language

## Summary
Spud is going to be a low-level programming language with a high-level, developer-friendly syntax. The long-term goal is for Spud to become a fully self-hosted systems language capable of building everything from operating systems and VGA-level graphical software to AI tools and quantum-focused computation.  
Spud will eventually support importing its own source files as well as code written in other languages.

## Plan
The first milestone is a fully functional interpreted version of Spud supporting:
- Input
- Output
- Variables
- Expressions
- Loops
- Conditionals
- Imports
- Functions
- Error Handling

Once the interpreter is stable, the plan is to add an optimized memory buffer (`runtime/`) and transition Spud into a compiled language with an initial compiler written in C.  
After that, the compiler will be rewritten in Spud itself — completing the path to a fully self-hosted toolchain.

## Additional Information
See the [LICENSE](LICENSE) for licensing details.  
Documentation is available in the [DOCUMENTATION](docs/DOCUMENTATION.md) and recent changes can be found in the [CHANGELOG](docs/CHANGELOG.md).

## Important Notes
This project is created by a human developer and supported with AI-assisted tooling.
