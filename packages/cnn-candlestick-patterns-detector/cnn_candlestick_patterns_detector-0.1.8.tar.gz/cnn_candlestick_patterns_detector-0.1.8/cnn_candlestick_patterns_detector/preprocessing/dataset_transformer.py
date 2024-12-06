import json
import os

from cnn_candlestick_patterns_detector.preprocessing.candlestick_series_normalizer import CandlestickNormalizer
from cnn_candlestick_patterns_detector.utils.common import save_candlestick_chart


def _finalize_candles(deviations, start_price=100):
    previous_mid_price = start_price
    results = []

    for i in range(len(deviations['direction'])):
        mid_change_decimal = deviations['mid_changes'][i] / 100
        top_deviation_decimal = deviations['top_deviation'][i] / 100
        bottom_deviation_decimal = deviations['bottom_deviation'][i] / 100
        high_deviation_decimal = deviations['high_deviation'][i] / 100
        low_deviation_decimal = deviations['low_deviation'][i] / 100

        if i == 0:
            mid_price = start_price
        else:
            mid_price = previous_mid_price * (1 + mid_change_decimal)

        top_body_price = mid_price * (1 + top_deviation_decimal)
        bottom_body_price = mid_price * (1 - bottom_deviation_decimal)

        high_price = mid_price * (1 + high_deviation_decimal)
        low_price = mid_price * (1 - low_deviation_decimal)

        if deviations['direction'][i] == 1:
            open_price = bottom_body_price
            close_price = top_body_price
        else:
            open_price = top_body_price
            close_price = bottom_body_price

        results.append({
            'open': open_price,
            'close': close_price,
            'high': high_price,
            'low': low_price
        })

        previous_mid_price = mid_price

    return results


def _invert_candle_data(candle_percentages):
    inverted_data = {}
    inverted_data['direction'] = [-x for x in candle_percentages['direction']]
    inverted_data['top_deviation'] = candle_percentages['bottom_deviation']
    inverted_data['bottom_deviation'] = candle_percentages['top_deviation']
    inverted_data['high_deviation'] = candle_percentages['low_deviation']
    inverted_data['low_deviation'] = candle_percentages['high_deviation']
    inverted_data['mid_changes'] = [-x for x in candle_percentages['mid_changes']]

    return inverted_data


def _invert_candles(candle_percentages):
    invert_candle_percentages = _invert_candle_data(candle_percentages)
    return _finalize_candles(invert_candle_percentages)


def _reverse_and_recalculate_mid_changes(candle_percentages, start_price=100):
    reversed_candles = {
        'direction': candle_percentages['direction'][::-1],  # Инвертируем направления
        'top_deviation': candle_percentages['bottom_deviation'][::-1],  # Меняем bottom на top
        'bottom_deviation': candle_percentages['top_deviation'][::-1],  # Меняем top на bottom
        'low_deviation': candle_percentages['high_deviation'][::-1],  # Меняем high на low
        'high_deviation': candle_percentages['low_deviation'][::-1]  # Меняем low на high
    }

    recalculated_mid_changes = [0]
    previous_mid_price = start_price

    mid_changes_reversed = candle_percentages['mid_changes'][::-1]

    for i in range(1, len(reversed_candles['direction'])):
        mid_change = mid_changes_reversed[i - 1]
        current_mid_price = previous_mid_price * (1 + mid_change / 100)
        change = (current_mid_price - previous_mid_price) / previous_mid_price * 100
        recalculated_mid_changes.append(change)
        previous_mid_price = current_mid_price

    reversed_candles['mid_changes'] = recalculated_mid_changes

    return _finalize_candles(reversed_candles)


def _validate_high_low_candles(raw_candles, name):
    print(f'For name {name}')
    for i, candle in enumerate(raw_candles):
        open_price = candle['open']
        close_price = candle['close']
        high_price = candle['high']
        low_price = candle['low']

        prices = [open_price, close_price, high_price, low_price]

        max_price = max(prices)
        if high_price != max_price:
            print(
                f"Ошибка в свече {i}: значение 'high' ({high_price}) не является максимальным (максимум {max_price}).")

        min_price = min(prices)
        if low_price != min_price:
            print(f"Ошибка в свече {i}: значение 'low' ({low_price}) не является минимальным (минимум {min_price}).")


def _transform_candles(raw_candles):
    _validate_high_low_candles(raw_candles, "raw_candles")

    candle_percentages = CandlestickNormalizer.convert_candle_data_to_percentages(raw_candles)
    inverted_candles = _invert_candles(candle_percentages)
    _validate_high_low_candles(inverted_candles, "inverted_candles")
    reverse_candles = _reverse_and_recalculate_mid_changes(candle_percentages)
    _validate_high_low_candles(reverse_candles, "reverse_candles")
    candle_percentages = CandlestickNormalizer.convert_candle_data_to_percentages(reverse_candles)
    inverted_reverse_candles = _invert_candles(candle_percentages)
    _validate_high_low_candles(inverted_reverse_candles, "inverted_reverse_candles")

    return {
        "inverted_candles": inverted_candles,
        "reverse_candles": reverse_candles,
        "inverted_reverse_candles": inverted_reverse_candles
    }


def transform_candles_to(directory, transform_to):
    json_files = set()
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.json') and '_config.json' not in file:
                json_files.add(file)

    for json_file in json_files:
        json_path = os.path.join(directory, json_file)

        with open(json_path, 'r') as f:
            raw_candles = json.load(f)

        result = _transform_candles(raw_candles)
        raw_candles = result[transform_to]

        with open(json_path, 'w') as f:
            json.dump(raw_candles, f, indent=4)
        save_candlestick_chart(raw_candles, directory, f'{os.path.splitext(json_file)[0]}.png')

# raw_candles = [{"datetime": "2023-06-22 18:48:00", "open": 261.44, "high": 261.7, "low": 261.24, "close": 261.5899, "volume": 296525}, {"datetime": "2023-06-22 18:49:00", "open": 261.585, "high": 262.38, "low": 261.5649, "close": 262.369, "volume": 677390}, {"datetime": "2023-06-22 18:50:00", "open": 262.38, "high": 262.8, "low": 262.37, "close": 262.54, "volume": 564628}, {"datetime": "2023-06-22 18:51:00", "open": 262.53, "high": 262.8, "low": 262.51, "close": 262.6, "volume": 398230}, {"datetime": "2023-06-22 18:52:00", "open": 262.6001, "high": 262.8, "low": 262.55, "close": 262.6, "volume": 404303}, {"datetime": "2023-06-22 18:53:00", "open": 262.62, "high": 262.97, "low": 262.5801, "close": 262.81, "volume": 486107}, {"datetime": "2023-06-22 18:54:00", "open": 262.78, "high": 262.83, "low": 262.2771, "close": 262.3843, "volume": 499281}]
# result = modify_candles(raw_candles)
#
# random = random_string()
# directory = 'out/inverted_patterns'
# set_up_folder(directory)
# save_candlestick_chart(raw_candles, directory,
#                        f'original_{random}_c.png')
# # save_candlestick_chart(result["inverted_candles"], directory,
# #                        f'inverted_{random}.png')
# save_candlestick_chart(result["reverse_candles"], directory,
#                        f'reverse_{random}_c.png')
# # save_candlestick_chart(result["inverted_reverse_candles"], directory,
# #                        f'inverted_reverse_{random}.png')
# save_data_to_json(raw_candles, directory, f'original_{random}.json')
# save_data_to_json(result["reverse_candles"], directory, f'reverse_{random}.json')
#
# normalizer = CandlestickNormalizer()
# n_original_candles = normalizer.normalize(raw_candles)
# n_revert_candles= normalizer.normalize(result["reverse_candles"])
#
# save_multiple_line_plots(n_original_candles, directory, f'original_{random}.png')
# save_multiple_line_plots(n_revert_candles, directory, f'reverse_{random}.png')
#
# save_candlestick_chart(result["reverse_candles"]+raw_candles, directory, f'compare_{random}.json')
