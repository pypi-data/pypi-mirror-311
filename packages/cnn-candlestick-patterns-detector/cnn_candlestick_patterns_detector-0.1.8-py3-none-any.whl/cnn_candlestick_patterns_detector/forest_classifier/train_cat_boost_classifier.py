import os

import numpy as np
from catboost import CatBoostRegressor, Pool, cv
from sklearn.model_selection import train_test_split

from cnn_candlestick_patterns_detector.provider.soft_labels_data_provider import SoftLabelsDataProvider
from cnn_candlestick_patterns_detector.utils.common import random_string, save_calculate_calibration_curve, \
    save_prediction_error_analysis


class TrainClassifier:
    def __init__(self, data_path, model_dir="out/models", report_dir="out/reports"):
        self.model_id = random_string()
        self.data_path = data_path
        self.model_dir = model_dir
        self.report_dir = report_dir
        self.model = CatBoostRegressor(iterations=3000,
                                       depth=8,
                                       learning_rate=0.06,
                                       loss_function='RMSE',
                                       random_seed=42,
                                       verbose=False)
        os.makedirs(self.model_dir, exist_ok=True)
        os.makedirs(self.report_dir, exist_ok=True)

    def load_and_prepare_data(self):
        provider = SoftLabelsDataProvider()
        provider.extract_json_data(self.data_path)
        data, labels, raw_data = provider.read_json_data()
        labels = np.array([label[0] for label in labels])
        data = np.array(data)
        data = data.reshape(data.shape[0], -1)
        return train_test_split(data, labels, test_size=0.2, random_state=42)

    def cross_validate(self, data, labels):
        cv_data = Pool(data, labels)
        params = self.model.get_params()
        params.update({'custom_metric': ['RMSE', 'R2']})
        cv_results = cv(cv_data, params, fold_count=5, seed=42, shuffle=True, plot=False)
        print("Средний RMSE на кросс-валидации:", np.mean(cv_results['test-RMSE-mean']))
        print("Средний R² на кросс-валидации:", np.mean(cv_results.get('test-R2-mean', [])))

    def fit_model(self, data, labels):
        train_data = Pool(data, labels)
        self.model.fit(train_data)

    def save_model(self):
        model_filename = f"catboost_model_{self.model_id}.cbm"
        model_path = os.path.join(self.model_dir, model_filename)
        self.model.save_model(model_path, format="cbm")
        print(f"Модель сохранена по пути: {model_path}")
        return model_path

    def analyze_feature_importances(self):
        feature_importances = self.model.get_feature_importance()
        print("Важность признаков:")
        for i, score in enumerate(feature_importances):
            print(f"Признак {i}: {score:.4f}")


prep_and_train = TrainClassifier('../s7/datasets/softlabels_class_1.7z')
train_data, val_data, train_labels, val_labels = prep_and_train.load_and_prepare_data()
prep_and_train.cross_validate(train_data, train_labels)
prep_and_train.fit_model(train_data, train_labels)
prep_and_train.analyze_feature_importances()
model_path = prep_and_train.save_model()

val_predictions = prep_and_train.model.predict(val_data)
save_calculate_calibration_curve(val_predictions, val_labels, prep_and_train.report_dir,
                                 f"calibration_curve_{prep_and_train.model_id}.png")
save_prediction_error_analysis(val_predictions, val_labels, prep_and_train.report_dir,
                               f'prediction_error_analysis_{prep_and_train.model_id}.png')
