import json
import os

import numpy as np

from cnn_candlestick_patterns_detector.preprocessing.candlestick_series_normalizer import CandlestickPercentageNormalizer


def load_examples(directory):
    normalizer = CandlestickPercentageNormalizer()
    data = []
    for filename in os.listdir(directory):
        if filename.endswith(".json") and not filename.endswith("_config.json"):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                json_data = json.load(file)
                normalized_data = normalizer.normalize(json_data)
                normalized_data = np.expand_dims(normalized_data, axis=0)
                data.append(normalized_data)
    return np.array(data)
