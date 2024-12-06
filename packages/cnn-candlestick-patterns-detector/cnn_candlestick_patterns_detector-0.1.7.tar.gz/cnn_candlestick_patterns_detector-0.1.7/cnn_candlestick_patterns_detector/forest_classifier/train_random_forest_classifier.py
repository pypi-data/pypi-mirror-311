import os

import numpy as np
from joblib import dump
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, make_scorer
from sklearn.model_selection import KFold, cross_val_score, train_test_split

from cnn_candlestick_patterns_detector.provider.soft_labels_data_provider import SoftLabelsDataProvider
from cnn_candlestick_patterns_detector.utils.common import random_string, save_calculate_calibration_curve, \
    save_prediction_error_analysis


class TrainClassifier:
    def __init__(self, data_path, model_dir="out/models", report_dir="out/reports"):
        self.model_id = random_string()
        self.data_path = data_path
        self.model_dir = model_dir
        self.report_dir = report_dir
        self.model = RandomForestRegressor(n_estimators=300, random_state=42)
        os.makedirs(self.model_dir, exist_ok=True)
        os.makedirs(self.report_dir, exist_ok=True)

    def load_and_prepare_data(self):
        provider = SoftLabelsDataProvider()
        provider.extract_json_data(self.data_path)
        data, labels, raw_data = provider.read_json_data()
        labels = np.array([label[0] for label in labels])
        data = np.array(data)
        data = np.array(data).reshape(data.shape[0], -1)
        return train_test_split(data, labels, test_size=0.2, random_state=42)

    def cross_validate(self, data, labels):
        kf = KFold(n_splits=5, shuffle=True, random_state=42)
        mse_scores = cross_val_score(self.model, data, labels, cv=kf, scoring=make_scorer(mean_squared_error))
        r2_scores = cross_val_score(self.model, data, labels, cv=kf, scoring='r2')
        print("MSE по кросс-валидации:", mse_scores)
        print("Средний MSE:", np.mean(mse_scores))
        print("R² по кросс-валидации:", r2_scores)
        print("Средний R²:", np.mean(r2_scores))

    def fit_model(self, data, labels):
        self.model.fit(data, labels)

    def save_model(self):
        model_filename = f"random_forest_model_{self.model_id}.joblib"
        model_path = os.path.join(self.model_dir, model_filename)
        dump(self.model, model_path)
        print(f"Модель сохранена по пути: {model_path}")
        return model_path

    def analyze_feature_importances(self, data, labels):
        feature_importances = self.model.feature_importances_
        importance_groups = {
            "relative_ratios_l": np.sum(feature_importances[0:7]),
            "relative_ratios_h": np.sum(feature_importances[7:14]),
            "candle_size": np.sum(feature_importances[14:21]),
            "gap_percentage": np.sum(feature_importances[21:28]),
            "o": np.sum(feature_importances[28:35]),
        }
        print("Суммарная важность признаков для каждой группы:")
        for group, importance in importance_groups.items():
            print(f"{group}: {importance:.4f}")


prep_and_train = TrainClassifier('../s7/datasets/softlabels_class_0.7z')
train_data, val_data, train_labels, val_labels = prep_and_train.load_and_prepare_data()
prep_and_train.cross_validate(train_data, train_labels)
prep_and_train.fit_model(train_data, train_labels)
model_path = prep_and_train.save_model()
prep_and_train.analyze_feature_importances(train_data, train_labels)

val_predictions = prep_and_train.model.predict(val_data)
save_calculate_calibration_curve(val_predictions, val_labels, prep_and_train.report_dir,
                                 f"calibration_curve_{prep_and_train.model_id}.png")
save_prediction_error_analysis(val_predictions, val_labels, prep_and_train.report_dir,
                               f'prediction_error_analysis_{prep_and_train.model_id}.png')
