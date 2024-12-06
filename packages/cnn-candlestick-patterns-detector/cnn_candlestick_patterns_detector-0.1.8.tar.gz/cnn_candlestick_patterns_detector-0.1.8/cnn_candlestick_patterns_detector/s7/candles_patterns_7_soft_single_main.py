import argparse
import os
import uuid
from multiprocessing import Process

import numpy as np
import shap
import torch
from torch import optim
from torch.nn import BCEWithLogitsLoss

from cnn_candlestick_patterns_detector.environment.model_tester import ModelTester
from cnn_candlestick_patterns_detector.environment.model_trainer import ModelTrainer
from cnn_candlestick_patterns_detector.provider.soft_labels_data_provider import SoftLabelsDataProvider
from cnn_candlestick_patterns_detector.s7.architecture.candles_patterns_7 import CandlesPatterns_7
from cnn_candlestick_patterns_detector.utils.common import save_prediction_error_analysis, save_shap_summary


def analyze_shap(model_id, model, test_loader, reports_dir):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    all_shap_values = []

    for inputs, _ in test_loader:
        inputs = inputs.to(device)
        print('shap analyze next batch')
        explainer = shap.GradientExplainer(model, inputs)
        shap_values = explainer.shap_values(inputs)
        shap_values_flat = shap_values.reshape(shap_values.shape[0], -1)
        all_shap_values.append(shap_values_flat)

    all_shap_values = np.vstack(all_shap_values)
    save_shap_summary(all_shap_values, reports_dir, f"shap_summary_{model_id}.png")
    print(f'Save shap summary {model_id}')

def save_model_and_calibrator(model, model_id, model_dir, calibrator=None):
    model_filename = f"{model.__class__.__name__}_{model_id}.pth"
    model_path = os.path.join(model_dir, model_filename)
    torch.save(model.state_dict(), model_path)

    # calibrator_filename = f"{model.__class__.__name__}_{model_id}_calibrator.joblib"
    # calibrator_path = os.path.join(model_dir, calibrator_filename)
    # joblib.dump(calibrator, calibrator_path)

def train_and_test_model(model_dir, reports_dir):
    train_loader, test_loader, label_stats = SoftLabelsDataProvider().get_dataloaders()
    model_id = str(uuid.uuid4())
    model = CandlesPatterns_7()
    optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-4)
    loss = BCEWithLogitsLoss()
    trainer = ModelTrainer(model_id, model, train_loader, epochs=50, criterion=loss, optimizer=optimizer)
    trainer.train()

    tester = ModelTester(model_id, model, test_loader, criterion=loss)
    all_predictions, all_targets, avg_loss = tester.test()

    save_prediction_error_analysis(all_predictions, all_targets, reports_dir,
                                   f'prediction_error_analysis_{model_id}.png')
    analyze_shap(model_id, model, test_loader, reports_dir)
    save_model_and_calibrator(model, model_id, model_dir)


def main(target_class='softlabels_class_0'):
    model_dir = "out/models"
    reports_dir = "out/reports"
    os.makedirs(model_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)

    SoftLabelsDataProvider().extract_json_data(f'./data_provider/data/{target_class}.7z')

    for _ in range(3500):
        process_count = 25
        processes = []

        for _ in range(process_count):
            process = Process(target=train_and_test_model, args=(model_dir, reports_dir))
            process.start()
            processes.append(process)

        for process in processes:
            process.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Запуск модели с указанием target_class.")
    parser.add_argument('--target_class', type=str, required=True,
                        help='Название целевого класса, например softlabels_class_1')
    args = parser.parse_args()

    main(args.target_class)