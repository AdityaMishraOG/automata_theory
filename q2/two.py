##################### BOILERPLATE BEGINS ############################

# Token types enumeration
##################### YOU CAN CHANGE THE ENUMERATION IF YOU WANT #######################
import sys


class TokenType:
    IDENTIFIER = "IDENTIFIER"
    KEYWORD = "KEYWORD"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    SYMBOL = "SYMBOL"


# Token hierarchy dictionary
token_hierarchy = {
    "if": TokenType.KEYWORD,
    "else": TokenType.KEYWORD,
    "print": TokenType.KEYWORD
}


# helper function to check if it is a valid identifier
def is_valid_identifier(lexeme):
    if not lexeme:
        return False

    # Check if the first character is an underscore or a letter
    if not (lexeme[0].isalpha() or lexeme[0] == '_'):
        return False

    # Check the rest of the characters (can be letters, digits, or underscores)
    for char in lexeme[1:]:
        if not (char.isalnum() or char == '_'):
            return False

    return True


# Tokenizer function
def tokenize(source_code):
    tokens = []
    position = 0

    while position < len(source_code):
        # Helper function to check if a character is alphanumeric
        def is_alphanumeric(char):
            return char.isalpha() or char.isdigit() or (char == '_')

        char = source_code[position]

        # Check for whitespace and skip it
        if char.isspace():
            position += 1
            continue

        # Identifier recognition
        if char.isalpha():
            lexeme = char
            position += 1
            while position < len(source_code) and is_alphanumeric(source_code[position]):
                lexeme += source_code[position]
                position += 1

            if lexeme in token_hierarchy:
                token_type = token_hierarchy[lexeme]
            else:
                # check if it is a valid identifier
                if is_valid_identifier(lexeme):
                    token_type = TokenType.IDENTIFIER
                else:
                    raise ValueError(f"Invalid identifier: {lexeme}")

        # Integer or Float recognition
        elif char.isdigit():
            lexeme = char
            position += 1

            is_float = False
            while position < len(source_code):
                next_char = source_code[position]
                # checking if it is a float, or a full-stop
                if next_char == '.':
                    if (position + 1 < len(source_code)):
                        next_next_char = source_code[position+1]
                        if next_next_char.isdigit():
                            is_float = True

                # checking for illegal identifier
                elif is_alphanumeric(next_char) and not next_char.isdigit():
                    while position < len(source_code) and is_alphanumeric(source_code[position]):
                        lexeme += source_code[position]
                        position += 1
                    if not is_valid_identifier(lexeme):
                        raise ValueError(
                            f"Invalid identifier: {str(lexeme)}\nIdentifier can't start with digits")

                elif not next_char.isdigit():
                    break

                lexeme += next_char
                position += 1

            token_type = TokenType.FLOAT if is_float else TokenType.INTEGER

        # Symbol recognition
        else:
            lexeme = char
            position += 1
            token_type = TokenType.SYMBOL

        tokens.append((token_type, lexeme))

    return tokens


########################## BOILERPLATE ENDS ###########################

ALL = {
    "S": ["IA", "SS", "y"],
    "A": ["CS", "CT"],
    "T": ["SU"],
    "U": ["ES"],
    "C": ["r", "y", "XY"],
    "Y": ["OX"],
    "O": ["+", "-", "*", "/", "^", ">", "<", "="],
    "I": ["if"],
    "E": ["else"],
    "X": ["r", "XY", "y"],
}


def checkGrammar(tokens):
    # write the code the syntactical analysis in this function
    # You CAN use other helper functions and create your own helper functions if needed

    n = len(tokens)

    list_of_tokens = []
    for i in range(n):
        token_type = tokens[i][0]

        if token_type == TokenType.IDENTIFIER or token_type == TokenType.INTEGER or token_type == TokenType.FLOAT or tokens[i][1] == "print":
            list_of_tokens.append("y")
        else:
            list_of_tokens.append(tokens[i][1])

    print(list_of_tokens)

    dp = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(set())
        dp.append(row)

    for i in range(n):
        for lhs in ALL.keys():
            if list_of_tokens[i] in ALL[lhs]:
                dp[i][i].add(lhs)

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            for k in range(i, j):
                for lhs, rhs_items in ALL.items():
                    for rhs in rhs_items:
                        if len(rhs) == 2 and rhs[0] != 'i':
                            left = rhs[0]
                            right = rhs[1]
                            if left in dp[i][k] and right in dp[k + 1][j]:
                                dp[i][j].add(lhs)

    if len(dp[0][n-1]) != 0:
        print("Accepted: The input sequence is valid according to the grammar.")
    else:
        print("Rejected: The input sequence is not valid according to the grammar.")


# Test the tokenizer
if __name__ == "__main__":
    # source_code = "if 2+xi > 0 print 2.0 else print -1;"
    source_code = input()
    if source_code == "":
        print("Syntax Error")
        sys.exit()
    # source_code = "if 2 + print print 5"

    tokens = tokenize(source_code)

    for token in tokens:
        print(f"Token Type: {token[0]}, Token Value: {token[1]}")

    # You are tasked with implementing the function checkGrammar
    logs = checkGrammar(tokens)
