import re


def input_to_int(input: str) -> int:
    """removes all non numeric characters from a string
    @input: str
    @returns: int"""
    return int(re.sub("[^0-9]", "", input))
