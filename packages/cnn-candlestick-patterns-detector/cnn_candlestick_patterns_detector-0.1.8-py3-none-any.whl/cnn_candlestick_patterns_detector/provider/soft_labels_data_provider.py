import json
import os
from pathlib import Path

import numpy as np
import py7zr
import torch
from sklearn.model_selection import train_test_split
from torch.utils.data import TensorDataset, DataLoader

from cnn_candlestick_patterns_detector.preprocessing.candlestick_series_normalizer import CandlestickNormalizer


class SoftLabelsDataProvider:
    def __init__(self, test_size=0.20, batch_size=32, normalizer=CandlestickNormalizer()):
        self.test_size = test_size
        self.batch_size = batch_size
        self.normalizer = normalizer
        self.temp_dir = self._get_temp_dir()

    @staticmethod
    def _print_label_statistics(labels):
        label_counts = {}

        for label in labels:
            label_str = str(label)
            if label_str in label_counts:
                label_counts[label_str] += 1
            else:
                label_counts[label_str] = 1

        sorted_label_counts = dict(sorted(label_counts.items(), key=lambda item: item[0]))

        total_count = 0
        for label, count in sorted_label_counts.items():
            print(f'Probability: {label}, Count: {count}')
            total_count += count

        print(f'Total Count: {total_count}')

    def get_dataloaders(self):
        data, labels, raw_data = self.read_json_data()
        labels = np.array(labels)
        data = np.array(data)
        data = np.expand_dims(data, axis=1)

        label_stats = self._calculate_probability_stats(labels)
        x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=self.test_size, random_state=42)

        x_train = torch.tensor(x_train, dtype=torch.float32)
        x_test = torch.tensor(x_test, dtype=torch.float32)
        y_train = torch.tensor(y_train, dtype=torch.float32)
        y_test = torch.tensor(y_test, dtype=torch.float32)

        train_dataset = TensorDataset(x_train, y_train)
        test_dataset = TensorDataset(x_test, y_test)

        train_loader = DataLoader(train_dataset, batch_size=self.batch_size, shuffle=True)
        test_loader = DataLoader(test_dataset, batch_size=self.batch_size, shuffle=False)

        return train_loader, test_loader, label_stats

    def _calculate_probability_stats(self, labels):
        flat_labels = np.concatenate(labels)
        values, counts = np.unique(flat_labels, return_counts=True)
        probability_stats = dict(zip(values, counts))
        return probability_stats

    def extract_json_data(self, archive_path):
        self._clear_temp_dir()

        with py7zr.SevenZipFile(archive_path, mode='r') as archive:
            archive.extractall(path=self.temp_dir)

    def read_json_data(self):
        normalized_data = []
        labels = []
        raw_data = []

        for file in self.temp_dir.glob('*.json'):
            if 'config' not in file.stem:
                conf_file = file.with_name(f'{file.stem}_config.json')

                with open(file, 'r') as f:
                    series = json.load(f)
                    normalized_series_data = self.normalizer.normalize(series)

                label_vector = []
                with open(conf_file, 'r') as f:
                    conf_data = json.load(f)
                    for label_info in conf_data:
                        label_vector.append(float(label_info['probability']))

                normalized_data.append(normalized_series_data)
                raw_data.append(series)
                labels.append(label_vector)

        self._print_label_statistics(labels)

        return normalized_data, labels, raw_data

    def _get_temp_dir(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        temp_dir = os.path.join(current_dir, 'data', 'temp_extracted')
        os.makedirs(temp_dir, exist_ok=True)
        return Path(temp_dir)

    def _clear_temp_dir(self):
        for root, dirs, files in os.walk(self.temp_dir, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))
