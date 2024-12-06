import os

import joblib

from cnn_candlestick_patterns_detector.preprocessing import CandlestickNormalizer
from cnn_candlestick_patterns_detector.utils.common import save_data_to_json, random_string, \
    save_candlestick_chart, set_up_folder


class RandomForestSearcher:
    def __init__(self, model_path):
        """
        Initialize the searcher with the model path and minimum probability threshold for the single class.
        """
        self.model = joblib.load(model_path)
        self.results_folder = 'out/random_forest_findings_v1/'
        set_up_folder(self.results_folder)

    def predict_and_save(self, ohlc_series):
        """
        Process each series in ohlc_series, predict and save if probability meets threshold.
        """
        normalizer = CandlestickNormalizer()
        for i, series in enumerate(ohlc_series):
            normalized_series = normalizer.normalize(series).flatten()
            normalized_series = normalized_series.reshape(1, -1)

            probability = self.model.predict(normalized_series)[0]
            rounded_probability = round(probability, 2)
            probability_folder = f'p_{rounded_probability}'
            results_folder = os.path.join(self.results_folder, probability_folder)

            if not os.path.exists(results_folder):
                os.makedirs(results_folder, exist_ok=True)

            print(f'{i} of {len(ohlc_series)} probability {rounded_probability}')
            random_code = random_string()
            save_data_to_json(series, results_folder,
                              f'series_p_{rounded_probability}_{random_code}.json')
            save_candlestick_chart(series, results_folder,
                                   f'series_p_{rounded_probability}_{random_code}.png')
            config_data = [{"label": "0", "probability": rounded_probability}]
            save_data_to_json(config_data, results_folder,
                              f'series_p_{rounded_probability}_{random_code}_config.json')
