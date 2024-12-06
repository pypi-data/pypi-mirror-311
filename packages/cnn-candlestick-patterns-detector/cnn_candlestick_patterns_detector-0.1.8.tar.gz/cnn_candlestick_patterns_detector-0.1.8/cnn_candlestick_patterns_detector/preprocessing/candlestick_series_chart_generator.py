import json
import os

from cnn_candlestick_patterns_detector.utils.common import save_candlestick_chart


def generate_chart(directory):
    print('Generate .png charts')
    json_files = set()

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.json') and '_config.json' not in file:
                json_files.add(file)

    for i, json_file in enumerate(json_files):
        print(f'chart image {i} of {len(json_files)}')
        json_path = os.path.join(directory, json_file)

        with open(json_path, 'r') as f:
            raw_candles = json.load(f)

        save_candlestick_chart(raw_candles, directory, f'{os.path.splitext(json_file)[0]}.png')