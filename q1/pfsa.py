import argparse
import pytest
import json
from collections import defaultdict


def starts_with_prefix(list_of_words, prefix):
    count = 0
    for word in list_of_words:
        if word.startswith(prefix):
            count += 1
    return count


def construct(file_str: str) -> dict[str, dict[str, float]]:

    list_of_words = file_str.lower().split()
    pfsa = defaultdict(lambda: defaultdict(float))

    for word in list_of_words:
        first_char = word[0]
        if first_char not in pfsa["*"]:
            # print(f"{first_char} is not in pfsa")
            pfsa["*"][first_char] = 0.0
        # print(f"value = ", pfsa["*"][first_char])
        pfsa["*"][first_char] += 1.0 / len(list_of_words)
        # print(f"fraction = ", 1.0/len(list_of_words))

    for word in list_of_words:
        for i in range(1, len(word)):
            prefix = word[:i]
            next_word = word[:i + 1]
            if prefix not in pfsa:
                pfsa[prefix] = {}
            if next_word not in pfsa[prefix]:
                pfsa[prefix][next_word] = 0.0
            pfsa[prefix][next_word] += 1.0 / \
                (starts_with_prefix(list_of_words, prefix))
        if word not in pfsa:
            pfsa[word] = {}
        next_word = word + "*"
        if next_word not in pfsa[word]:
            pfsa[word][next_word] = 0.0
        pfsa[word][next_word] += 1.0 / \
            (starts_with_prefix(list_of_words, prefix))

    return pfsa


def main():
    """
    The command for running is `python pfsa.py text.txt`. This will generate
    a file `text.json` which you will be using for generation.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help="Name of the text file")
    args = parser.parse_args()

    with open(args.file, "r") as file:
        contents = file.read()
        output = construct(contents)

    name = args.file.split(".")[0]

    with open(f"{name}.json", "w") as file:
        json.dump(output, file)


if __name__ == "__main__":
    main()


STRINGS = ["A cat", "A CAT", "", "A", "A A A A"]
DICTIONARIES = [
    {
        "*": {"a": 0.5, "c": 0.5},
        "a": {"a*": 1.0},
        "c": {"ca": 1.0},
        "ca": {"cat": 1.0},
        "cat": {"cat*": 1.0},
    },
    {
        "*": {"a": 0.5, "c": 0.5},
        "a": {"a*": 1.0},
        "c": {"ca": 1.0},
        "ca": {"cat": 1.0},
        "cat": {"cat*": 1.0},
    },
    {
        "*": {},
    },
    {
        "*": {"a": 1.0},
        "a": {"a*": 1.0},
    },
    {
        "*": {"a": 1.0},
        "a": {"a*": 1.0},
    },
]


@pytest.mark.parametrize("string, pfsa", list(zip(STRINGS, DICTIONARIES)))
def test_output_match(string, pfsa):
    """
    To test, install `pytest` beforehand in your Python environment.

    Run `pytest pfsa.py` Your code must pass all tests. There are additional
    hidden tests that your code will be tested on during VIVA.
    """
    result = construct(string)
    assert result == pfsa
