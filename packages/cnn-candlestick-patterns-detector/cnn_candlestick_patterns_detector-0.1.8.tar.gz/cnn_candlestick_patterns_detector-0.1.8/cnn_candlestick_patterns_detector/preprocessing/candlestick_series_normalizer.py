import numpy as np


class CandlestickNormalizer:
    @staticmethod
    def normalize(candles):

        percentages = CandlestickNormalizer.convert_candle_data_to_percentages(candles)

        return np.vstack([
            CandlestickNormalizer._standardize_with_zero(percentages['mid_changes']),
            CandlestickNormalizer._standardize(percentages['top_deviation']),
            np.array(percentages['direction'])
        ])

    @staticmethod
    def _standardize(data):
        data_array = np.array(data)
        max_val = np.max(np.abs(data_array))

        if max_val != 0:
            normalized_data = data_array / max_val
        else:
            normalized_data = np.zeros_like(data_array)

        return normalized_data

    @staticmethod
    def _standardize_with_zero(data):
        data_array = np.array(data[1:])
        max_val = np.max(np.abs(data_array))

        if max_val != 0:
            normalized_data = data_array / max_val
        else:
            normalized_data = np.zeros_like(data_array)

        return np.concatenate(([0], normalized_data))

    @staticmethod
    def _calculate_mid_prices(candles):
        return [(candle['open'] + candle['close']) / 2 for candle in candles]

    @staticmethod
    def _calculate_price_changes(prices):
        changes = [0]
        for i in range(1, len(prices)):
            if prices[i - 1] != 0:
                change = (prices[i] - prices[i - 1]) / prices[i - 1] * 100
            else:
                change = 0
            changes.append(change)
        return changes

    @staticmethod
    def _calculate_extreme_prices(candles, key):
        return [max(candle['open'], candle['close']) if key == 'top' else min(candle['open'], candle['close']) for
                candle in candles]

    @staticmethod
    def _calculate_deviation(prices, compare_prices, key):
        deviations = []
        for price, compare_price in zip(prices, compare_prices):
            if price != 0:
                if key == 'top' or key == 'high':
                    deviation = ((compare_price - price) / price) * 100
                elif key == 'bottom' or key == 'low':
                    deviation = ((price - compare_price) / price) * 100
            else:
                deviation = 0
            deviations.append(deviation)
        return deviations

    @staticmethod
    def _calculate_candle_direction(candles):
        return [1 if candle['close'] > candle['open'] else (-1 if candle['close'] < candle['open'] else 0) for candle in
                candles]

    @staticmethod
    def convert_candle_data_to_percentages(candles):
        mid_prices = CandlestickNormalizer._calculate_mid_prices(candles)
        mid_changes = CandlestickNormalizer._calculate_price_changes(mid_prices)
        top_prices = CandlestickNormalizer._calculate_extreme_prices(candles, 'top')
        bottom_prices = CandlestickNormalizer._calculate_extreme_prices(candles, 'bottom')
        high_prices = [candle['high'] for candle in candles]
        low_prices = [candle['low'] for candle in candles]

        top_deviation = CandlestickNormalizer._calculate_deviation(mid_prices, top_prices, 'top')
        bottom_deviation = CandlestickNormalizer._calculate_deviation(mid_prices, bottom_prices, 'bottom')
        high_deviation = CandlestickNormalizer._calculate_deviation(mid_prices, high_prices, 'high')
        low_deviation = CandlestickNormalizer._calculate_deviation(mid_prices, low_prices, 'low')
        direction = CandlestickNormalizer._calculate_candle_direction(candles)

        return {
            "mid_changes": mid_changes,
            "top_deviation": top_deviation,
            "bottom_deviation": bottom_deviation,
            "high_deviation": high_deviation,
            "low_deviation": low_deviation,
            "direction": direction
        }


class CandlestickPercentageNormalizer:
    def normalize(self, raw_candles):
        normalized_relative_ratios_h = [
            ((candle['high'] - candle['close']) / candle['close'] * 100) if candle['close'] >= candle['open'] else
            ((candle['high'] - candle['open']) / candle['open'] * 100) for candle in raw_candles]

        normalized_relative_ratios_l = [
            ((candle['open'] - candle['low']) / candle['open'] * 100) if candle['close'] >= candle['open'] else
            ((candle['close'] - candle['low']) / candle['close'] * 100) for candle in raw_candles]

        normalized_candle_size = [
            (candle['close'] - candle['open']) / candle['open'] * 100 if candle['open'] != 0 else 0 for
            candle in raw_candles]
        normalized_o = self._calculate_open_percentage(raw_candles)

        return np.vstack([
            normalized_relative_ratios_l,
            normalized_relative_ratios_h,
            normalized_candle_size,
            normalized_o
        ])

    def _calculate_open_percentage(self, raw_candles):
        o_values = [0]
        for i in range(1, len(raw_candles)):
            previous_open = raw_candles[i - 1]['open']
            current_open = raw_candles[i]['open']
            o_change = (current_open - previous_open) / previous_open * 100 if previous_open != 0 else 0
            o_values.append(o_change)
        return o_values


class CandlestickDenormalizer:
    def denormalize(self, normalized_data, initial_price=100):
        normalized_relative_ratios_l = normalized_data[0]
        normalized_relative_ratios_h = normalized_data[1]
        normalized_candle_size = normalized_data[2]
        normalized_o = normalized_data[3]

        absolute_candles = []
        current_open_price = initial_price

        for i in range(len(normalized_o)):
            if i == 0:
                current_open_price = current_open_price  # Для первой свечи используем начальную цену
            else:
                current_open_price = current_open_price * (
                        1 + normalized_o[i] / 100)  # Рассчитываем новую цену открытия

            change = current_open_price * (normalized_candle_size[i] / 100)
            close_price = current_open_price + change
            high = close_price if normalized_candle_size[i] >= 0 else current_open_price
            high += abs(high) * (normalized_relative_ratios_h[i] / 100)
            low = close_price if normalized_candle_size[i] < 0 else current_open_price
            low -= abs(low) * (normalized_relative_ratios_l[i] / 100)

            absolute_candles.append({
                'open': current_open_price,
                'high': high,
                'low': low,
                'close': close_price
            })

        return absolute_candles

# original = [{"datetime": "2023-06-22 18:48:00", "open": 261.44, "high": 261.7, "low": 261.24, "close": 261.5899, "volume": 296525}, {"datetime": "2023-06-22 18:49:00", "open": 261.585, "high": 262.38, "low": 261.5649, "close": 262.369, "volume": 677390}, {"datetime": "2023-06-22 18:50:00", "open": 262.38, "high": 262.8, "low": 262.37, "close": 262.54, "volume": 564628}, {"datetime": "2023-06-22 18:51:00", "open": 262.53, "high": 262.8, "low": 262.51, "close": 262.6, "volume": 398230}, {"datetime": "2023-06-22 18:52:00", "open": 262.6001, "high": 262.8, "low": 262.55, "close": 262.6, "volume": 404303}, {"datetime": "2023-06-22 18:53:00", "open": 262.62, "high": 262.97, "low": 262.5801, "close": 262.81, "volume": 486107}, {"datetime": "2023-06-22 18:54:00", "open": 262.78, "high": 262.83, "low": 262.2771, "close": 262.3843, "volume": 499281}]
# reversed = [{"open": 100.07534784828289, "close": 99.92465215171708, "high": 100.11617316714023, "low": 99.90561049180226}, {"open": 99.91328932101356, "close": 99.9855744667412, "high": 100.000754347344, "low": 99.85241761934817}, {"open": 99.99320258948607, "close": 99.99316451135793, "high": 100.01224165355907, "low": 99.91704633319411}, {"open": 99.9932008127128, "close": 100.01986261919929, "high": 100.0274802781954, "low": 99.9170242227515}, {"open": 100.01604540412245, "close": 100.07703544629281, "high": 100.08084732392845, "low": 99.91693658559561}, {"open": 100.08101646527855, "close": 100.38097065572823, "high": 100.38866080780481, "low": 100.07680792434114}, {"open": 100.3793068584544, "close": 100.4368606302494, "high": 100.51365018567967, "low": 100.33703420819003}]
# normalizer = CandlestickNormalizer()
# n_original = normalizer.normalize(original)
# n_reversed = normalizer.normalize(reversed)
#
# directory = 'out/normalized'
# set_up_folder(directory)
#
# save_multiple_line_plots(n_original, directory, f'original.png')
# save_multiple_line_plots(n_reversed, directory, f'reverse.png')
# save_candlestick_chart(original, directory, f'c_original.png')
# save_candlestick_chart(reversed, directory, f'c_reversed.png')


# ################################################
# example_bad = [{"datetime": "2024-08-09 01:59:00", "open": 199.98, "high": 200, "low": 199.95, "close": 200, "volume": 1666}, {"datetime": "2024-08-09 02:00:00", "open": 199.98, "high": 200.04, "low": 199.92, "close": 200, "volume": 10370}, {"datetime": "2024-08-09 02:01:00", "open": 200.1, "high": 200.2, "low": 200.1, "close": 200.2, "volume": 3351}, {"datetime": "2024-08-09 02:02:00", "open": 200.1, "high": 200.2, "low": 200.1, "close": 200.2, "volume": 1858}, {"datetime": "2024-08-09 02:03:00", "open": 200.1999, "high": 200.25, "low": 200.1993, "close": 200.25, "volume": 5094}, {"datetime": "2024-08-09 02:04:00", "open": 200.25, "high": 200.3398, "low": 200.25, "close": 200.3398, "volume": 1858}, {"datetime": "2024-08-09 02:05:00", "open": 200.23, "high": 200.32, "low": 200.15, "close": 200.15, "volume": 1573}]
# example_good = [{"datetime": "2022-07-05 18:41:00", "open": 138.5601, "high": 138.72, "low": 138.53, "close": 138.6538, "volume": 95000}, {"datetime": "2022-07-05 18:42:00", "open": 138.66, "high": 138.82, "low": 138.66, "close": 138.815, "volume": 148042}, {"datetime": "2022-07-05 18:43:00", "open": 138.82, "high": 138.98, "low": 138.82, "close": 138.88, "volume": 169909}, {"datetime": "2022-07-05 18:44:00", "open": 138.88, "high": 139.0899, "low": 138.86, "close": 139.0702, "volume": 181746}, {"datetime": "2022-07-05 18:45:00", "open": 139.07, "high": 139.23, "low": 139, "close": 139.21, "volume": 148295}, {"datetime": "2022-07-05 18:46:00", "open": 139.21, "high": 139.32, "low": 139.1732, "close": 139.29, "volume": 232628}, {"datetime": "2022-07-05 18:47:00", "open": 139.29, "high": 139.4742, "low": 139.26, "close": 139.4093, "volume": 150816}]
# normalizer = CandlestickNormalizer()
# n_example_bad = normalizer.normalize(example_bad)
# n_example_good = normalizer.normalize(example_good)
# directory = 'out/normalized'
# set_up_folder(directory)
#
# save_multiple_line_plots(n_example_bad, directory, f'example_bad.png')
# save_multiple_line_plots(n_example_good, directory, f'example_good.png')
# save_candlestick_chart(example_bad, directory, f'c_example_bad.png')
# save_candlestick_chart(example_good, directory, f'c_example_good.png')
