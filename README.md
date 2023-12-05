# AUTOMATA THEORY
The repository contains the solutions to the programming assignment given as a part of the course **CS1.302 Automata Theory**.

1. ### PFSA - Probabilistic Finite State Automata
    - Python script `generator.py` to generate random words from a PFSA stored in JSON format.

2. ### Compiler with tokenization and CFG parsing
   - Python program `two.py` to check if string enterred by the user follows the rules of a context-free grammar. It is a syntax checker that verifies whether a given source code adheres to a specific context-free grammar. It includes a tokenizer function, token types enumeration, and helper functions for identifying valid identifiers and recognizing tokens.
  
   - It uses the `CYK Algorithm` with Time complexity `O(N`<sup>`3`</sup>`)` and Space complexity `O(N`<sup>`2`</sup>`)`   
   
   - We *assume* that the compiler can not handle negative numbers in the input strings.
