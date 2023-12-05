import argparse
import pytest
import json
from random import choices


def generate(pfsa: dict[str, dict[str, float]], word_count: int) -> str:
    """Takes in the PFSA and generates a string of `word_count` number of words
    The following string is when the input has only "Cat" as in it's PFSA with
    count of 4.
    """
    if "*" not in pfsa:
        return None

    list_of_words = []

    for blenk in range(word_count):
        state = "*"
        while (1):
            list_of_next_states = list(pfsa[state].keys())
            transition_probabilities = list(pfsa[state].values())
            next_state = choices(list_of_next_states,
                                 weights=transition_probabilities)[0]
            # print(f"next_state = {next_state}")
            # print(f"next_state[-1] = {next_state[-1]}")
            if next_state.endswith("*"):
                break
            state = next_state

        list_of_words.append(state)

    generated_text = ""
    for word in list_of_words:
        generated_text += word + " "

    generated_text = generated_text.rstrip()
    # print(f"generated_text = {generated_text}")
    return generated_text


def main():
    """
    The command for running is `python generator.py text.json 5`. This will
    generate a file `text_sample.txt` which has 5 randomly sampled words.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help="Name of the text file")
    parser.add_argument("count", type=int, help="Sample size to gen")
    args = parser.parse_args()

    with open(args.file, "r") as file:
        data = json.load(file)
        output = generate(data, args.count)

    name = args.file.split(".")[0]

    with open(f"{name}_sample.txt", "w") as file:
        file.write(output)


if __name__ == "__main__":
    main()


DICTIONARIES = [
    {
        "*": {"a": 1.0},
        "a": {"a*": 1.0},
    },
    {
        "*": {"a": 1.0},
        "a": {"a*": 1.0},
    },
    {
        "*": {"a": 1.0},
        "a": {"a*": 1.0},
    },
    {
        "*": {"c": 1.0},
        "c": {"ca": 1.0},
        "ca": {"cat": 1.0},
        "cat": {"cat*": 1.0},
    },
]
STRINGS = [
    "a",
    "a a a a a",
    "",
    "cat cat cat cat",
]
COUNT = [1, 5, 0, 4]

COMBINED = [(d, s, c) for d, (s, c) in zip(DICTIONARIES, zip(STRINGS, COUNT))]


@pytest.mark.parametrize("pfsa, string, count", COMBINED)
def test_output_match(pfsa, string, count):
    """
    To test, install `pytest` beforehand in your Python environment.
    Run `pytest pfsa.py` Your code must pass all tests. There are additional
    hidden tests that your code will be tested on during VIVA.
    """
    result = generate(pfsa, count)
    assert result == string
