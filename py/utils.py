import json
import sys
import time
from typing import Union


def save_json_response(json_response: Union[str, dict], file_name: str) -> None:
    """
    Saves a JSON response from an API into a file.

    Args:
        json_response (Union[str, dict]): The JSON response from the API, either as a string or a dictionary.
        file_name (str): The name of the file to save the JSON data to (e.g., "data.json").
    """
    # If the response is a string, convert it to a dictionary
    if isinstance(json_response, str):
        data: dict = json.loads(json_response)
    else:
        data = json_response

    # Save the data to a JSON file
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print(f"JSON data saved to {file_name}")


def sbyPrint(text: str) -> None:
    """Prints text with inline color specifications.

    Args:
        text (str): The text to print, with inline markers for color changes.

    This function uses ANSI color codes to print colored text in the terminal.
    """

    color_codes = {
        "red": "91",
        "green": "92",
        "yellow": "93",
        "blue": "94",
        "magenta": "95",
        "cyan": "96",
        "white": "97",
        "bgred": "101",
        "bggreen": "102",
        "bgyellow": "103",
        "bgblue": "104",
        "bgmagenta": "105",
        "bgcyan": "106",
        "bgwhite": "107",
        "bgreset": "49"
    }
    parts = text.split("{")
    final_text = ""
    for part in parts:
        if "}" in part:
            color_name, text_segment = part.split("}", 1)
            color_code = color_codes.get(color_name.lower(), "97")
            final_text += f"\033[{color_code}m{text_segment}"
        else:
            final_text += part
    final_text += "\033[0m"
    print(final_text)


def coloredBar(percentage):
    """
    A function that generates a colored progress bar based on the completion percentage.

    Parameters:
    - percentage (int): The completion percentage of the progress bar.

    Returns:
    - bar (str): A string representing the colored progress bar.
    """

    bar_length = 50  # Length of the progress bar
    filled_length = int(bar_length * percentage // 100)

    # ANSI escape codes for colors
    RED = '\033[91m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    RESET = '\033[0m'

    # Change color based on completion percentage
    if percentage < 33:
        color = RED
    elif percentage < 66:
        color = YELLOW
    else:
        color = GREEN

    bar = color + '▓' * filled_length + '░' * (bar_length - filled_length) + RESET
    return bar


# @myLogger
def countdown(secs):
    """
    A function that performs a countdown for the given number of seconds.

    :param secs: An integer representing the total number of seconds to count down.
    :return: None
    """

    total = secs
    while secs >= 0:
        pct_complete = 100 * (total - secs) / total
        bar = coloredBar(pct_complete)

        mins, secs_remaining = divmod(secs, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs_remaining)
        sys.stdout.write(f'\r<<< Sleeping to avoid rate limits... |{bar}| {timeformat} >>> ')
        sys.stdout.flush()

        time.sleep(1)
        secs -= 1
