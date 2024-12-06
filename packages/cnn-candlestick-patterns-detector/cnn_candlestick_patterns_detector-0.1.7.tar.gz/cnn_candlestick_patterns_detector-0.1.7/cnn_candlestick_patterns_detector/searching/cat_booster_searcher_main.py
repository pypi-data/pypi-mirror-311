from datetime import datetime

from providers.stock_series_data_provider import StockSeriesDataProvider

from cnn_candlestick_patterns_detector.searching.cat_booster_searcher import CatBoosterSearcher

searcher = CatBoosterSearcher(
    model_path='../cnn_candlestick_patterns_detector/forest_classifier/out/models/catboost_model_MYTBZD.cbm',
)

splitted_ohlc_series = StockSeriesDataProvider(['AMD'],
                                   datetime(2024, 9, 1),
                                   datetime(2024, 9, 10)).get_all_instruments_sliced_by_window(7)

searcher.predict_and_save(splitted_ohlc_series)
