import os

from catboost import CatBoostRegressor

from cnn_candlestick_patterns_detector.preprocessing import CandlestickNormalizer
from cnn_candlestick_patterns_detector.utils.common import save_data_to_json, random_string, \
    save_candlestick_chart, set_up_folder


class CatBoosterSearcher:
    def __init__(self, model_path):
        """
        Initialize the searcher with the model path and minimum probability threshold for the single class.
        """
        self.model = CatBoostRegressor().load_model(model_path, format='cbm')
        self.results_folder = 'out/findings_soft_cat_boost/'
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
            rounded_probability = max(0.0, round(probability, 2))
            # if rounded_probability > 0.1:
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
