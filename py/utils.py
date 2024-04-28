import json
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
