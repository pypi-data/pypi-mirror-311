import json
import os
import random
from unittest import TestCase

from matplotlib import pyplot as plt

from cnn_candlestick_patterns_detector.s7.cnn_soft_labels_multiclass_classifier import CNNSoftLabelsMulticlassClassifierS7


def set_up_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


class TestCNNSoftLabelsMulticlassValidator(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.results_folder = 'out/tests_results/'
        set_up_folder(cls.results_folder)

        cls.class_validator = CNNSoftLabelsMulticlassClassifierS7(
            config_path='../models/models_config.json'
        )

    def _read_and_validate(self, directory_path):
        print(f'read {directory_path}')
        vectors_group = []
        json_files = [f for f in os.listdir(directory_path) if f.endswith('.json') and '_config.json' not in f]

        for file_name in json_files[:100]:
            file_path = os.path.join(directory_path, file_name)

            with open(file_path, 'r') as file:
                data = json.load(file)

            vector = self.class_validator.classify_2d(data)
            vectors_group.append(vector)

        return vectors_group

    def _generate_random_color(self):
        return "#%06x" % random.randint(0, 0xFFFFFF)

    def test_validate_2d_plot_all_classes_09(self):
        vectors_groups = [
            self._read_and_validate('/\s7\datasets\softlabels_class_0\p_0.90'),
            self._read_and_validate('/\s7\datasets\softlabels_class_1\p_0.90'),
            self._read_and_validate('/\s7\datasets\softlabels_class_2\p_0.90'),
            self._read_and_validate('/\s7\datasets\softlabels_class_3\p_0.90'),
            self._read_and_validate('/\s7\datasets\softlabels_class_4\p_0.90'),
            self._read_and_validate('/\s7\datasets\softlabels_class_5\p_0.90')]

        group_colors = ['blue', 'green', 'red', 'purple', 'orange', 'cyan']
        plt.figure(figsize=(12, 8))
        for group_idx, vectors_group in enumerate(vectors_groups):
            color = group_colors[group_idx % len(group_colors)]
            for idx, vector in enumerate(vectors_group):
                plt.scatter(vector[0], vector[1], color=color, label=f'Group {group_idx}, Vector {idx}')

        plt.title('2D Vectors from Multiple Groups')
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.axhline(0, color='black', linewidth=0.5)
        plt.axvline(0, color='black', linewidth=0.5)
        plt.grid(True)

        result_path = os.path.join(self.results_folder, 'all_classes_09.png')
        plt.savefig(result_path)
        plt.close()

    def _all_probabilities(self, class_name):
        vectors_groups = [
            self._read_and_validate(f'/\s7\datasets\\{class_name}\p_0.00'),
            self._read_and_validate(f'/\s7\datasets\\{class_name}\p_0.05'),
            self._read_and_validate(f'/\s7\datasets\\{class_name}\p_0.10'),
            self._read_and_validate(f'/\s7\datasets\\{class_name}\p_0.15'),
            self._read_and_validate(f'/\s7\datasets\\{class_name}\p_0.20'),
            self._read_and_validate(f'/\s7\datasets\\{class_name}\p_0.25'),
            self._read_and_validate(f'/\s7\datasets\\{class_name}\p_0.30'),
            self._read_and_validate(f'/\s7\datasets\\{class_name}\p_0.35'),
            self._read_and_validate(f'/\s7\datasets\\{class_name}\p_0.40'),
            self._read_and_validate(f'/\s7\datasets\\{class_name}\p_0.45'),
            self._read_and_validate(f'/\s7\datasets\\{class_name}\p_0.50'),
            self._read_and_validate(f'/\s7\datasets\\{class_name}\p_0.55'),
            self._read_and_validate(f'/\s7\datasets\\{class_name}\p_0.60'),
            self._read_and_validate(f'/\s7\datasets\\{class_name}\p_0.65'),
            self._read_and_validate(f'/\s7\datasets\\{class_name}\p_0.70'),
            self._read_and_validate(f'/\s7\datasets\\{class_name}\p_0.75'),
            self._read_and_validate(f'/\s7\datasets\\{class_name}\p_0.80'),
            self._read_and_validate(f'/\s7\datasets\\{class_name}\p_0.85'),
            self._read_and_validate(f'/\s7\datasets\\{class_name}\p_0.90')]

        random_colors = [self._generate_random_color() for _ in range(len(vectors_groups))]
        plt.figure(figsize=(12, 8))

        for group_idx, vectors_group in enumerate(vectors_groups):
            color = random_colors[group_idx]
            for idx, vector in enumerate(vectors_group):
                plt.scatter(vector[0], vector[1], color=color)

        plt.title('2D Vectors from Multiple Groups')
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.axhline(0, color='black', linewidth=0.5)
        plt.axvline(0, color='black', linewidth=0.5)
        plt.grid(True)

        result_path = os.path.join(self.results_folder, f'all_probabilities_for_{class_name}.png')
        plt.savefig(result_path)
        plt.close()

    def test_validate_2d_plot_all_probabilities_for_classes(self):
        self._all_probabilities('softlabels_class_0')
        self._all_probabilities('softlabels_class_1')
        self._all_probabilities('softlabels_class_2')
        self._all_probabilities('softlabels_class_3')
        self._all_probabilities('softlabels_class_4')
        self._all_probabilities('softlabels_class_5')
