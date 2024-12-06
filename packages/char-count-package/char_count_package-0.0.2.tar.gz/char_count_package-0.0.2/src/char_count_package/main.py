"""
This program accepts command line arguments under the flags --string and/or --filepath.
The script counts the ocurrence of unique characters in the given string or file.
"""
from collections import Counter
import functools
import argparse
import pathlib


@functools.lru_cache()
def count_unique_characters(parameter):
    """Return the total number of characters that appears only once in the given string"""
    result = 0
    if not count_unique_characters.cache_info().hits:
        once_char_counter = 0
        chars_counter_dict = Counter(parameter)

        for value in map(lambda num: num == 1, chars_counter_dict.values()):
            if value:
                once_char_counter += 1
            result = once_char_counter
    return result


def read_file(filepath):
    """Open a file, read it and return its content"""
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()
        return content


def get_parser():
    """Return a parser"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--filepath", type=pathlib.Path, help="The input filepath")
    parser.add_argument("--string", type=str, help="The input string")
    return parser


def process_parameter():
    """Process the parameter from command line, giving higher priority to the parameter '--file'."""
    parser = get_parser()
    known_args, unknown_args = parser.parse_known_args()

    if known_args.filepath:
        if known_args.filepath.is_file():
            file_content = read_file(known_args.filepath)
            return count_unique_characters(file_content)
        return parser.error(f"Please review your parameter:"
                            f" {known_args.filepath}, it is not a file path.")
    elif known_args.string:
        return count_unique_characters(known_args.string)
    else:
        return parser.error("Error: Required arguments are missing.")


if __name__ == '__main__':
    print(process_parameter())
