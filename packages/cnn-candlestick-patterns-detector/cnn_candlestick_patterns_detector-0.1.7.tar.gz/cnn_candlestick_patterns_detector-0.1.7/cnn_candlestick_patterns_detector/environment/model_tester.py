import numpy as np
import torch

from cnn_candlestick_patterns_detector.config.logger_config import LoggerConfig


class ModelTester:
    def __init__(self, model_id, model, test_loader, criterion):
        self.logger = LoggerConfig.get_logger(model_id)
        self.model_id = model_id
        self.model = model
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.test_loader = test_loader
        self.criterion = criterion

    def test(self):
        self.model.eval()
        total_loss = 0.0
        total_samples = 0
        all_predictions = []
        all_targets = []

        with torch.no_grad():
            for data, target in self.test_loader:
                data, target = data.to(self.device), target.to(self.device).float()
                output = self.model(data)
                loss = self.criterion(output.view(-1), target.view(-1))
                total_loss += loss.item()
                total_samples += target.size(0)

                probs = torch.sigmoid(output)
                all_predictions.append(probs.cpu().numpy())
                all_targets.append(target.cpu().numpy())

        avg_loss = total_loss / len(self.test_loader)

        print(f"Testing Complete model {self.model_id}: Avg Loss = {avg_loss:.4f}")
        self.logger.info(
            f"Testing Complete model {self.model_id}: Avg Loss = {avg_loss:.4f}")

        all_predictions = np.concatenate(all_predictions)
        all_targets = np.concatenate(all_targets)

        return all_predictions, all_targets, avg_loss
