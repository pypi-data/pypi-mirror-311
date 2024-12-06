import torch
import torch.nn.functional as F
from torch import optim

from cnn_candlestick_patterns_detector.GAN.architecture.generator_7 import Generator_7
from cnn_candlestick_patterns_detector.GAN.data_provider.discriminator_data_provider import load_examples
from cnn_candlestick_patterns_detector.preprocessing.candlestick_series_normalizer import CandlestickDenormalizer
from cnn_candlestick_patterns_detector.utils.common import set_up_folder, random_string, save_candlestick_chart, save_data_to_json


class GeneratorTrainingManager:
    def __init__(self, input_dim, output_shape, directory='out/generated'):
        self.generator = Generator_7(input_dim=input_dim, output_shape=output_shape)
        self.optimizer = optim.Adam(self.generator.parameters(), lr=1e-4)
        self.directory = directory
        self.input_dim = input_dim
        set_up_folder(self.directory)

    def pretrain_generator(self, data, epochs=100, batch_size=32):
        data_tensor = torch.tensor(data, dtype=torch.float32)
        self.generator.train()
        for epoch in range(epochs):
            avg_loss = self._shuffle_and_train(data_tensor, batch_size, epoch)
            print(f'Pretrain Epoch [{epoch + 1}/{epochs}], Average Loss: {avg_loss:.4f}')

    def _shuffle_and_train(self, data, batch_size, epoch):
        idx = torch.randperm(data.size(0))
        data_shuffled = data[idx]
        total_loss = 0
        total_samples = 0

        for i in range(0, data.size(0), batch_size):
            batch_data = data_shuffled[i:i + batch_size]
            noise = torch.randn(batch_data.size(0), self.input_dim)
            generated_data = self.generator(noise)
            loss = self._calculate_loss(generated_data, batch_data)

            total_loss += loss.item() * batch_data.size(0)
            total_samples += batch_data.size(0)

        avg_loss = total_loss / total_samples
        return avg_loss

    def _calculate_loss(self, generated_data, real_data):
        self.optimizer.zero_grad()
        loss = F.l1_loss(generated_data, real_data) + 0.5 * F.mse_loss(generated_data, real_data)
        loss.backward()
        self.optimizer.step()
        return loss

    def generate_and_save_examples(self, num_examples=2):
        noise = torch.randn(num_examples, self.input_dim)
        generated_data = self.generator(noise)
        denormalizer = CandlestickDenormalizer()

        for tensor in generated_data:
            normalized_data = tensor.detach().cpu().numpy().reshape(4, 7)
            denormalized_data = denormalizer.denormalize(normalized_data)
            self.save_results(denormalized_data, 'generated')

    def save_results(self, example, prefix):
        random_code = random_string()
        save_data_to_json(example, self.directory, f'{prefix}_{random_code}.json')
        save_candlestick_chart(example, self.directory, f'{prefix}_{random_code}.png')
        config_data = [{"label": "0", "probability": 0}]
        save_data_to_json(config_data, self.directory, f'{prefix}_{random_code}_config.json')


if __name__ == "__main__":
    input_dim = 100
    output_shape = (1, 4, 7)

    trainer = GeneratorTrainingManager(input_dim, output_shape)
    randomized_examples = load_examples(f'D:\WORK\cnn-candlestick-patterns-labeling\\utils\\randomized_examples')
    trainer.pretrain_generator(randomized_examples, epochs=110, batch_size=32)
    # 100 = P_80
    # 80 = P_70
    # 60 = P_60
    # 50 = P_50
    # 40 = P_40
    # 30 = P_30
    # 20 = P_20
    # 10 = P_10
    for _ in range(20):
        trainer.generate_and_save_examples()
