import numpy as np
import torch

from cnn_candlestick_patterns_detector.provider.soft_labels_data_provider import SoftLabelsDataProvider
from cnn_candlestick_patterns_detector.utils.common import set_up_folder, save_candlestick_chart, random_string, save_data_to_json


class CNNSoftLabelsDatasetChecker:
    def __init__(self, model_type, models_paths, dataset_path, target_probability, threshold):
        self.threshold = threshold
        self.dataset_path = dataset_path
        self.results_folder = 'out/dataset_checking/'
        self.target_probability = float(target_probability)
        set_up_folder(self.results_folder)
        self.models = []
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        for path in models_paths:
            model = model_type()
            state_dict = torch.load(path, map_location=self.device)
            model.load_state_dict(state_dict)
            model.eval()
            model.to(self.device)
            self.models.append(model)
            print(f'Loaded model {path}')

    def _extract_data(self):
        filtered_normalized_data = []
        filtered_raw_data = []
        provider = SoftLabelsDataProvider()
        provider.extract_json_data(self.dataset_path)
        normalized_data, targets, raw_data = provider.read_json_data()
        for nd, tg, rd in zip(normalized_data, targets, raw_data):
            if round(tg[0], 2) == self.target_probability:
                filtered_normalized_data.append(nd)
                filtered_raw_data.append(rd)

        return filtered_normalized_data, filtered_raw_data

    def check_and_save(self):
        filtered_normalized_data, filtered_raw_data = self._extract_data()
        print(f'Target {self.target_probability} - examples {len(filtered_normalized_data)}')
        out_of_threshold = []

        for nd, rd in zip(filtered_normalized_data, filtered_raw_data):
            normalized_series = np.expand_dims(nd, axis=0)
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
            if not (
                    self.target_probability - self.threshold <= average_probability <= self.target_probability + self.threshold):
                out_of_threshold.append(average_probability)
                random = random_string()
                save_candlestick_chart(rd, self.results_folder,
                                       f'p_{rounded_probability}_{random}.png')
                save_data_to_json(rd, self.results_folder, f'p_{rounded_probability}_{random}.json')
                config_data = [{"label": "0", "probability": 0}]
                save_data_to_json(config_data, self.results_folder,
                                  f'p_{rounded_probability}_{random}_config.json')

        percentage = (len(out_of_threshold) / len(filtered_normalized_data)) * 100
        print(f'Failed {len(out_of_threshold)} all {len(filtered_normalized_data)} ({percentage:.2f}%)')
