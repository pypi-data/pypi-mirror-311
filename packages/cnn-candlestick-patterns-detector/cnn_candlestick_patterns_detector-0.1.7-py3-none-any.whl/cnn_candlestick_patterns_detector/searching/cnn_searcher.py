import os

import numpy as np
import torch

from cnn_candlestick_patterns_detector.preprocessing import CandlestickNormalizer
from cnn_candlestick_patterns_detector.s7.architecture.candles_patterns_7 import CandlesPatterns_7
from cnn_candlestick_patterns_detector.utils.common import save_data_to_json, random_string, save_candlestick_chart, \
    set_up_folder


class CNNSearcher:
    def __init__(self, models_paths):
        self.results_folder = 'out/findings_soft_multiple_model_CNN/'
        set_up_folder(self.results_folder)
        self.models = []
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.probability_counts = {}
        for path in models_paths:
            model = CandlesPatterns_7()
            state_dict = torch.load(path, map_location=self.device)
            model.load_state_dict(state_dict)
            model.eval()
            model.to(self.device)
            self.models.append(model)
            print(f'Loaded model {path}')

    def predict_and_save(self, ohlc_series):
        normalizer = CandlestickNormalizer()
        for i, series in enumerate(ohlc_series):
            normalized_series = normalizer.normalize(series)
            normalized_series = np.expand_dims(normalized_series, axis=0)
            normalized_series = np.expand_dims(normalized_series, axis=0)
            tensor_series = torch.tensor(normalized_series, dtype=torch.float32).to(self.device)

            probabilities = []
            with torch.no_grad():
                for model in self.models:
                    output = model(tensor_series)
                    prob = torch.sigmoid(output).cpu().numpy()[0, 0]
                    probabilities.append(prob)

            average_probability = float(np.mean(probabilities))
            rounded_probability = round(average_probability, 2)
            probability_folder = f'p_{rounded_probability}'
            results_folder = os.path.join(self.results_folder, probability_folder)
            if not os.path.exists(results_folder):
                os.makedirs(results_folder, exist_ok=True)

            if self.probability_counts.get(rounded_probability, 0) >= 1000:
                continue

            if rounded_probability not in self.probability_counts:
                self.probability_counts[rounded_probability] = 0

            self.probability_counts[rounded_probability] += 1


            print(f'{i} of {len(ohlc_series)} probability {rounded_probability}')
            random_code = random_string()
            save_data_to_json(series, results_folder,
                              f'series_p_{rounded_probability}_{random_code}.json')
            save_candlestick_chart(series, results_folder,
                                   f'series_p_{rounded_probability}_{random_code}.png')
            config_data = [{"label": "0", "probability": rounded_probability}]
            save_data_to_json(config_data, results_folder,
                          f'series_p_{rounded_probability}_{random_code}_config.json')