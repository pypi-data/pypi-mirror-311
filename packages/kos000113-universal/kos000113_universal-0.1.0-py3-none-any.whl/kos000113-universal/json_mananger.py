import json
from typing import Union, Dict, Any

def update_data(file_path: str, what_data: str, sama_data: Any) -> Union[str, None]:
    """Обновление данных в указанном JSON-файле по пути к файлу."""
    try:
        with open(file_path, "r", encoding="utf-8") as json_file:
            dict_data = json.load(json_file)

        dict_data[what_data] = sama_data

        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(dict_data, json_file, ensure_ascii=False, indent=4)

        return "Data updated successfully."
    except FileNotFoundError:
        return "Error: File not found."
    except json.JSONDecodeError:
        return "Error: Failed to decode JSON."
    except Exception as e:
        return f"An unexpected error occurred: {e}"


def get_data(file_path: str) -> Union[Dict[str, Any], str]:
    """Получение данных из указанного JSON-файла по пути к файлу."""
    try:
        with open(file_path, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return "Error: File not found."
    except json.JSONDecodeError:
        return "Error: Failed to decode JSON."
    except Exception as e:
        return f"An unexpected error occurred: {e}"