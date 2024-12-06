import torch
import torch.nn as nn
import torch.nn.functional as F

class Generator_7(nn.Module):
    def __init__(self, input_dim, output_shape):
        super(Generator_7, self).__init__()
        self.output_shape = output_shape

        self.fc1 = nn.Linear(input_dim, 256 * 2 * 4)

        self.deconv1 = nn.ConvTranspose2d(256, 128, kernel_size=(3, 3), stride=(2, 2), padding=1, output_padding=(1, 1))
        self.bn1 = nn.BatchNorm2d(128)

        self.deconv2 = nn.ConvTranspose2d(128, 64, kernel_size=(3, 3), stride=(1, 1), padding=1)

        self.conv = nn.Conv2d(64, output_shape[0], kernel_size=(1, 2), stride=(1, 1), padding=(0, 0))

    def forward(self, x):
        x = F.leaky_relu(self.fc1(x), 0.01)
        x = x.view(-1, 256, 2, 4)

        x = F.leaky_relu(self.bn1(self.deconv1(x)), 0.01)
        x = F.leaky_relu(self.deconv2(x), 0.01)

        x = torch.tanh(self.conv(x))

        return x
