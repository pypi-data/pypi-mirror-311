import json
import os

from cnn_candlestick_patterns_detector.utils.json_comparison import are_similar


def _remove_color(data):
    was_updated = False
    for item in data:
        if 'color' in item:
            was_updated = True
            del item['color']
    return data, was_updated


def _remove_datetime(data):
    was_updated = False
    for item in data:
        if 'datetime' in item:
            was_updated = True
            del item['datetime']
    return data, was_updated


def _fix_high_low_candles(raw_candles):
    was_fixed = False
    for i, candle in enumerate(raw_candles):
        open_price = float(candle['open'])
        close_price = float(candle['close'])
        high_price = float(candle['high'])
        low_price = float(candle['low'])

        max_price = max(open_price, close_price, high_price, low_price)
        min_price = min(open_price, close_price, high_price, low_price)

        if high_price != max_price:
            candle['high'] = max_price
            was_fixed = True
            print(f"Исправлено High в свече {i}: старое значение {high_price}, новое значение {max_price}.")

        if low_price != min_price:
            candle['low'] = min_price
            was_fixed = True
            print(f"Исправлено Low в свече {i}: старое значение {low_price}, новое значение {min_price}.")

    return raw_candles, was_fixed


def fix_json_files(directory):
    files = os.listdir(directory)
    for i, filename in enumerate(files):
        if filename.endswith(".json") and not filename.endswith("_config.json"):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            modified_data, was_color_removed = _remove_color(data)
            modified_data, was_datetime_removed = _remove_datetime(modified_data)
            modified_data, was_high_low_fixed = _fix_high_low_candles(modified_data)

            if was_color_removed or was_datetime_removed or was_high_low_fixed:
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(modified_data, file, ensure_ascii=False, indent=4)
                    print(f'Файл обновлён: {file_path}')

def _load_json_files(directory):
    json_data = {}
    for file_name in os.listdir(directory):
        if file_name.endswith('.json') and not file_name.endswith('_config.json'):
            file_path = os.path.join(directory, file_name)
            with open(file_path, 'r') as file:
                data = json.load(file)
                json_data[file_name] = data
    return json_data


def _find_identical_objects(data, directory):
    identical_files = []
    processed_files = set()
    processed_count = 0
    for src_name, src_content in data.items():
        print(f'processed {processed_count}')
        processed_count = processed_count + 1
        if src_name in processed_files:
            continue

        for tgt_name, tgt_content in data.items():
            if are_similar(src_content, tgt_content) and not (src_name == tgt_name):
                identical_files.append(os.path.join(directory, tgt_name))
                processed_files.add(tgt_name)
                break
    return identical_files


def _delete_files(file_list):
    for file_path in file_list:
        if os.path.exists(file_path):
            json_file = file_path
            json_config_file = file_path.replace(".json", "_config.json")
            png_file = file_path.replace(".json", ".png")
            os.remove(json_file)
            os.remove(json_config_file)
            os.remove(png_file)
            print(f"Deleted: {file_path}")


def remove_duplicates(source_directory):
    source_data = _load_json_files(source_directory)

    identical_files = _find_identical_objects(source_data, source_directory)
    _delete_files(identical_files)