import json
import os

from cnn_candlestick_patterns_detector.utils.json_comparison import are_similar


def _load_json_data(directory):
    json_files = [f for f in os.listdir(directory) if f.endswith('.json') and not f.endswith('_config.json')]
    json_data = {}
    for json_file in json_files:
        with open(os.path.join(directory, json_file), 'r') as file:
            try:
                json_data[json_file] = json.load(file)
            except json.JSONDecodeError:
                print(f"Error decoding JSON from {json_file}")
    return json_data


def _delete_files(filename, directory):
    base_name = filename[:-5]
    for extension in ['.json', '.png', '_config.json']:
        file_path = os.path.join(directory, base_name + extension)
        if os.path.exists(file_path):
            os.remove(file_path)


def compare_and_delete(dir_copy, dir_original):
    json_data_copy = _load_json_data(dir_copy)
    json_data_original = _load_json_data(dir_original)
    print(f'In source dir {dir_original} before {len(json_data_original)}')
    print(f'In copy dir {dir_copy} before {len(json_data_copy)}')

    files_to_delete = set()

    for file_copy, data_copy in json_data_copy.items():
        for file_original, data_original in json_data_original.items():
            if are_similar(data_copy, data_original):
                files_to_delete.add((file_original, dir_original))

    deleted_count = 0
    for file_original, dir_original in files_to_delete:
        _delete_files(file_original, dir_original)
        deleted_count += 1

    print(f'All deleted {deleted_count}')