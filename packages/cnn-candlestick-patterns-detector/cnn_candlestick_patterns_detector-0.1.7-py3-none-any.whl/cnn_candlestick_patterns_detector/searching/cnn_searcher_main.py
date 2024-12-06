import random
from datetime import datetime

from providers.stock_series_data_provider import StockSeriesDataProvider

from cnn_candlestick_patterns_detector.searching.cnn_searcher import \
    CNNSearcher

searcher = CNNSearcher(
    models_paths=['../s7/out/models/CandlesPatterns_7_6fb3d132-5407-4c29-9c66-5c306da198be.pth',
                  '../s7/out/models/CandlesPatterns_7_17729f01-75d0-4a51-af87-b0b9765f0cfa.pth',
                  '../s7/out/models/CandlesPatterns_7_fb664d4d-f3e1-4cbd-a6d4-35f1fd746b88.pth',
                  ]
)

splitted_ohlc_series = StockSeriesDataProvider(['AAPL', 'AMZN'],
                                   datetime(2024, 9, 1),
                                   datetime(2024, 9, 10)).get_all_instruments_sliced_by_window(7)
random.shuffle(splitted_ohlc_series)
searcher.predict_and_save(splitted_ohlc_series)
