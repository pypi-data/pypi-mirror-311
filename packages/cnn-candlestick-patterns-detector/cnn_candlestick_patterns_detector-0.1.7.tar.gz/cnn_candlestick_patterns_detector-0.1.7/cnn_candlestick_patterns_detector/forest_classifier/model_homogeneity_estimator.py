import json
import os

import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.ensemble import IsolationForest

from cnn_candlestick_patterns_detector.preprocessing.candlestick_series_normalizer import CandlestickNormalizer
from cnn_candlestick_patterns_detector.utils.common import set_up_folder


class ModelHomogeneityEstimator:
    def __init__(self, data_path, contamination=0.2):
        self.data_path = data_path
        self.contamination = contamination
        self.report_dir = "out/isolation_forest_model_estimator"
        set_up_folder(self.report_dir)
        self.model = IsolationForest(n_estimators=500, contamination=contamination, random_state=42)
        self.normalizer = CandlestickNormalizer()

    def analyze_group(self, data):
        self.model.fit(data)
        anomaly_scores = self.model.decision_function(data)
        return anomaly_scores

    def plot_histogram(self, scores, title):
        plt.hist(scores, bins=20, edgecolor='black')
        plt.title(title)
        plt.xlabel('Anomaly Score')
        plt.ylabel('Frequency')
        plt.show()

    def evaluate_group(self, data):
        scores = self.analyze_group(data)
        self.plot_histogram(scores, "Распределение оценок аномальности")
        mean_score = np.mean(scores)
        print(f"Средняя оценка аномальности: {mean_score:.4f}")
        return scores

    def plot_density(self, scores_group_1, scores_group_2, ticket_group_1, ticket_group_2):
        file_name = f'{ticket_group_1}_vs_{ticket_group_2}.png'
        sns.kdeplot(scores_group_1, shade=True, color="blue", label=f"Group {ticket_group_1}")
        sns.kdeplot(scores_group_2, shade=True, color="red", label=f"Group {ticket_group_2}")
        plt.title(f"Density Plot of Anomaly groups {ticket_group_1} VS {ticket_group_2}")
        plt.xlabel("Anomaly Score")
        plt.ylabel("Density")
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(self.report_dir, file_name))
        plt.close()

    def load_group(self, group):
        group_patch = os.path.join(self.data_path, group)
        json_files = [f for f in os.listdir(group_patch) if f.endswith('.json') and '_config.json' not in f]

        data = []
        for file_name in json_files:
            file_path = os.path.join(group_patch, file_name)
            with open(file_path, 'r') as json_file:
                json_data = json.load(json_file)
                normalized_series_data = self.normalizer.normalize(json_data)
                data.append(normalized_series_data)

        data = np.array(data)
        data = np.array(data).reshape(data.shape[0], -1)

        return data

    def train_isolation_forest(self, data):
        model = IsolationForest(n_estimators=100, contamination=self.contamination, random_state=42)
        model.fit(data)
        return model

    def apply_model(self, model, data):
        scores = model.decision_function(data)
        return scores

    def compare_groups(self, ticket_group_1, ticket_group_2):
        print(f'compare {ticket_group_1} vs {ticket_group_2}')
        data_group_1 = self.load_group(ticket_group_1)
        data_group_2 = self.load_group(ticket_group_2)
        self.model = self.train_isolation_forest(data_group_1)
        scores_group_2_from_model_1 = self.apply_model(self.model, data_group_2)
        scores_group_1_from_model_1 = self.apply_model(self.model, data_group_1)

        self.plot_density(scores_group_1_from_model_1, scores_group_2_from_model_1, ticket_group_1, ticket_group_2)


estimator = ModelHomogeneityEstimator(
    "D:\\WORK\\cnn_candlestick_patterns_detector\cnn_candlestick_patterns_detector\\searching\\findings_soft_multiple_model_CNN")
estimator.compare_groups('p_0.9', 'p_0.8')
estimator.compare_groups('p_0.8', 'p_0.7')
estimator.compare_groups('p_0.7', 'p_0.6')
estimator.compare_groups('p_0.6', 'p_0.5')
estimator.compare_groups('p_0.5', 'p_0.4')
estimator.compare_groups('p_0.4', 'p_0.3')
estimator.compare_groups('p_0.3', 'p_0.2')
estimator.compare_groups('p_0.2', 'p_0.1')
estimator.compare_groups('p_0.1', 'p_0.0')
