import json
import os

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.ensemble import IsolationForest

from cnn_candlestick_patterns_detector.preprocessing.candlestick_series_normalizer import CandlestickNormalizer
from cnn_candlestick_patterns_detector.utils.common import random_string, save_data_to_json, save_candlestick_chart, \
    set_up_folder


class GroupHomogeneityAnalyzer:
    def __init__(self, source_folder, contamination=0.2, n_estimators=5000):
        self.source_folder = source_folder
        self.n_estimators = n_estimators
        self.contamination = contamination
        self.model = None
        self.distribution_dir = "out/isolation_forest_model_estimator"
        set_up_folder(self.distribution_dir)

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

    def select_group(self, group):
        normalizer = CandlestickNormalizer()
        group_path = os.path.join(self.source_folder, group)
        json_files = [f for f in os.listdir(group_path) if f.endswith('.json') and not f.endswith('_config.json')]
        json_data = []
        for json_file in json_files:
            with open(os.path.join(group_path, json_file), 'r') as file:
                try:
                    json_data.append(json.load(file))
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from {json_file}")

        normalized_data = []
        for series in json_data:
            normalized_data.append(normalizer.normalize(series))

        normalized_data = np.array(normalized_data)
        normalized_data = np.array(normalized_data).reshape(normalized_data.shape[0], -1)

        return normalized_data, json_data

    def plot_density(self, scores_group_1, scores_group_2, ticket_group_1, ticket_group_2):
        file_name = f'{ticket_group_1}_vs_{ticket_group_2}.png'
        sns.kdeplot(scores_group_1, shade=True, color="blue", label=f"Group {ticket_group_1}")
        sns.kdeplot(scores_group_2, shade=True, color="red", label=f"Group {ticket_group_2}")
        plt.title(f"Density Plot of Anomaly groups {ticket_group_1} VS {ticket_group_2}")
        plt.xlabel("Anomaly Score")
        plt.ylabel("Density")
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(self.distribution_dir, file_name))
        plt.close()

    def compare_groups(self, ticket_group_1, ticket_group_2):
        data_group_1, raw_data_group_1 = analyzer.select_group(ticket_group_1)
        data_group_2, raw_data_group_2 = analyzer.select_group(ticket_group_2)
        self.model = self.train_isolation_forest(data_group_1)
        scores_group_2_from_model_1 = self.apply_model(self.model, data_group_2)
        scores_group_1_from_model_1 = self.apply_model(self.model, data_group_1)

        self.plot_density(scores_group_1_from_model_1, scores_group_2_from_model_1, ticket_group_1, ticket_group_2)

        return scores_group_2_from_model_1, raw_data_group_2

    def save_distribution(self, raw_data, folder_name, target_group):
        target_dir = os.path.join(self.distribution_dir, f'{target_group}', folder_name)
        os.makedirs(target_dir, exist_ok=True)
        for series in raw_data:
            r_string = random_string()
            save_data_to_json(series, target_dir, f'{r_string}.json')
            save_candlestick_chart(series, target_dir,
                                   f'{r_string}.png')
            config_data = [{"label": "0", "probability": 0}]
            save_data_to_json(config_data, target_dir,
                              f'{r_string}_config.json')

    def train_isolation_forest(self, data):
        model = IsolationForest(n_estimators=self.n_estimators, contamination=self.contamination, random_state=42)
        model.fit(data)
        return model

    def apply_model(self, model, data):
        scores = model.decision_function(data)
        return scores

    def split_and_save(self, source_group, target_group):
        scores_group_2_from_model_1, raw_data_group_2 = analyzer.compare_groups(source_group, source_group)
        below_threshold = np.where(scores_group_2_from_model_1 < 0)[0]
        filtered_raw_data = [raw_data_group_2[i] for i in below_threshold]
        self.save_distribution(filtered_raw_data, f'below_threshold', source_group)

        scores_group_2_from_model_1, raw_data_group_2 = analyzer.compare_groups(source_group, target_group)
        above_threshold = np.where(scores_group_2_from_model_1 >= 0)[0]
        filtered_raw_data = [raw_data_group_2[i] for i in above_threshold]
        self.save_distribution(filtered_raw_data, f'above_threshold', target_group)


source_group = 'p_0.65'
target_group = 'p_0.55'
source_dir = f'D:\WORK\cnn_candlestick_patterns_detector\cnn_candlestick_patterns_detector\searching\out\\NEW'
analyzer = GroupHomogeneityAnalyzer(source_dir)
analyzer.split_and_save(source_group=source_group, target_group=target_group)



dir1_path = f'D:\WORK\cnn_candlestick_patterns_detector\cnn_candlestick_patterns_detector\\forest-classifier\out\isolation_forest_model_estimator\\{target_group}\\above_threshold'
dir2_path = f'{source_dir}\\{target_group}'
dir3_path = f'D:\WORK\cnn_candlestick_patterns_detector\cnn_candlestick_patterns_detector\\forest-classifier\out\isolation_forest_model_estimator\\{source_group}\\below_threshold'
dir4_path = f'{source_dir}\\{source_group}'
# compare_and_delete(dir1_path, dir2_path)
# compare_and_delete(dir3_path, dir4_path)
# move_files(dir1_path, dir4_path)
# move_files(dir3_path, dir2_path)