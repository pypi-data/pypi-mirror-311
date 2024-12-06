import json
import math

import numpy as np
import torch
from pkg_resources import resource_filename

from cnn_candlestick_patterns_detector.preprocessing.candlestick_series_normalizer import CandlestickNormalizer
from cnn_candlestick_patterns_detector.s7.architecture.candles_patterns_7 import CandlesPatterns_7


class CNNSoftLabelsMulticlassClassifierS7:
    def __init__(self, config_path):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_classes = {}
        self.normalizer = CandlestickNormalizer()

        with open(config_path, 'r') as file:
            class_models_dict = json.load(file)

        for class_name, model_data in class_models_dict.items():
            models = []
            for model_path in model_data['models_paths']:
                model = CandlesPatterns_7()
                full_model_path = resource_filename(__name__, model_path)
                state_dict = torch.load(full_model_path, map_location=self.device)
                model.load_state_dict(state_dict)
                model.eval()
                model.to(self.device)
                models.append(model)
                print(f'Loaded model for {class_name} from {model_path}')
            self.model_classes[class_name] = models

    def _to_tensor(self, series):
        normalized_series = self.normalizer.normalize(series)
        normalized_series = np.expand_dims(normalized_series, axis=0)
        normalized_series = np.expand_dims(normalized_series, axis=0)
        return torch.tensor(normalized_series, dtype=torch.float32).to(self.device)

    @staticmethod
    def _probabilities_to_2d_vector(probabilities):
        angles_deg = [0, 72, 144, 216, 288, 360]
        angles_rad = [math.radians(angle) for angle in angles_deg]

        x, y = 0, 0

        for i in range(len(probabilities)):
            x += probabilities[i] * math.cos(angles_rad[i])
            y += probabilities[i] * math.sin(angles_rad[i])

        return x, y

    def classify_by_class(self, class_name, series):
        tensor_series = self._to_tensor(series)
        models = self.model_classes.get(class_name, [])
        if not models:
            print(f'No models found for class {class_name}')
            return None

        probabilities = []
        with torch.no_grad():
            for model in models:
                output = model(tensor_series)
                prob = torch.sigmoid(output).cpu().numpy()[0, 0]
                probabilities.append(prob)

        average_probability = float(np.mean(probabilities))
        rounded_probability = round(average_probability, 2)

        # print(
        #     f'Class {class_name}: Average Probability = {average_probability}, Rounded Probability = {rounded_probability}')
        return rounded_probability

    def classify(self, series):
        results = []
        for class_name in self.model_classes.keys():
            rounded_probability = self.classify_by_class(class_name, series)
            if rounded_probability is not None:
                results.append({
                    "label": class_name,
                    "probability": rounded_probability
                })

        return results

    def classify_2d(self, series):
        predicted = self.classify(series)
        probabilities = [item['probability'] for item in predicted]
        vector_x, vector_y = self._probabilities_to_2d_vector(probabilities)

        return vector_x, vector_y
