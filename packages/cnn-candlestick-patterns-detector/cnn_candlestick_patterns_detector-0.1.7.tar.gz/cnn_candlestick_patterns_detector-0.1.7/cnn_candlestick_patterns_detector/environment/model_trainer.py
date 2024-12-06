import torch

from cnn_candlestick_patterns_detector.config.logger_config import LoggerConfig


class ModelTrainer:
    def __init__(self, model_id, model, train_loader, epochs, criterion, optimizer):
        self.logger = LoggerConfig.get_logger(model_id)
        self.model_id = model_id
        self.model = model
        self.train_loader = train_loader
        self.optimizer = optimizer
        self.criterion = criterion
        self.epochs = epochs
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def train(self):
        self.model.train()
        avg_loss = 0.0
        for epoch in range(self.epochs):
            total_loss = 0
            total_samples = 0

            for data, target in self.train_loader:
                data, target = data.to(self.device), target.to(self.device).float()
                self.optimizer.zero_grad()
                output = self.model(data)
                loss = self.criterion(output.view(-1), target.view(-1))
                loss.backward()
                self.optimizer.step()

                total_loss += loss.item()
                total_samples += target.size(0)

            avg_loss = total_loss / len(self.train_loader)

            if epoch % 10 == 0:
                print(f'Epoch [{epoch}/{self.epochs}], Avg Loss: {avg_loss:.4f}')

        self.logger.info(
            f"Training completed for model ID {self.model_id}: Avg Loss = {avg_loss:.4f}")
