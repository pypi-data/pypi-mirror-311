import json
import os
import random
import shutil

from cnn_candlestick_patterns_detector.utils.common import random_string, save_data_to_json, save_candlestick_chart


class PatternRandomizer:
    def __init__(self, input_file, num_copies, change_percentage, sensitivity):
        self.input_data = self._load_json_file(input_file)
        self.num_copies = num_copies
        self.change_percentage = change_percentage
        self.sensitivity = sensitivity
        self.prepare_directory()

    def prepare_directory(self):
        self.results_folder = 'randomized_examples/'
        if os.path.exists(self.results_folder):
            shutil.rmtree(self.results_folder)
        os.makedirs(self.results_folder, exist_ok=True)

    def randomize_series(self):
        randomized_examples = []
        example = self.input_data
        total_values = len(example)
        num_to_change = int(total_values * self.change_percentage)
        changes = random.sample(range(total_values), num_to_change)
        for i in range(self.num_copies):
            new_example = []
            for j, candle in enumerate(example):
                new_candle = candle.copy()
                if j in changes:
                    trend_change = random.choice([-1, 1])
                    new_candle['open'] = self._randomize(candle['open'], trend_change, self.sensitivity)
                    new_candle['high'] = self._randomize(candle['high'], trend_change, self.sensitivity)
                    new_candle['low'] = self._randomize(candle['low'], trend_change, self.sensitivity)
                    new_candle['close'] = self._randomize(candle['close'], trend_change, self.sensitivity)

                new_candle['high'] = max(new_candle['open'], new_candle['high'], new_candle['close'])
                new_candle['low'] = min(new_candle['open'], new_candle['low'], new_candle['close'])
                new_candle['color'] = 'green' if new_candle['close'] > new_candle['open'] else 'red'
                new_example.append(new_candle)

            randomized_examples.append(new_example)

        return randomized_examples

    def _randomize(self, value, trend_change, sensitivity):
        if trend_change == 1:
            return round(value * (1 + random.uniform(0, sensitivity)), 4)
        else:
            return round(value * (1 - random.uniform(0, sensitivity)), 4)

    @staticmethod
    def _load_json_file(input_file):
        with open(input_file, 'r') as file:
            data = json.load(file)
        return data

    def save_results(self, randomized_examples):
        for i, example in enumerate(randomized_examples):
            random_code = random_string()
            print(f'save {i} of {len(randomized_examples)}')
            save_data_to_json(example, self.results_folder, f'randomized_{random_code}.json')
            save_candlestick_chart(example, self.results_folder, f'randomized_{random_code}.json')
            config_data = [{"label": "0", "probability": 0}]
            save_data_to_json(config_data, self.results_folder,
                              f'randomized_{random_code}_config.json')


input_file = f'D:\WORK\cnn_candlestick_patterns_detector\cnn_candlestick_patterns_detector\s7\data_provider\data\INTRESTING\series_p_0.29_QFVFQB.json'
randomizer = PatternRandomizer(
    input_file=input_file,
    num_copies=100,
    change_percentage=0.8,
    sensitivity=0.0004)

randomized_examples = randomizer.randomize_series()
randomizer.save_results(randomized_examples)
