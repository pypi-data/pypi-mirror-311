import torch.nn as nn
import torch.nn.functional as F


class CandlesPatterns_7(nn.Module):
    def __init__(self):
        super(CandlesPatterns_7, self).__init__()
        self.sequence_length = 7
        self.embed_dim = 32

        self.conv1 = nn.Conv2d(1, 8, kernel_size=(3, 1), padding=(1, 0))
        self.bn1 = nn.BatchNorm2d(8)

        self.conv2 = nn.Conv2d(8, 16, kernel_size=(3, 1), padding=(1, 0))
        self.bn2 = nn.BatchNorm2d(16)

        self.conv3 = nn.Conv2d(16, 32, kernel_size=(3, 1), padding=(1, 0))
        self.bn3 = nn.BatchNorm2d(32)

        self.shortcut = nn.Conv2d(8, 32, kernel_size=1)

        self.reduce_features = nn.Conv2d(32, 32, kernel_size=(3, 1), stride=1)

        self.attention = nn.MultiheadAttention(embed_dim=self.embed_dim, num_heads=16, batch_first=True)

        self.fc1 = nn.Linear(self.embed_dim * self.sequence_length, 80)
        self.dropout1 = nn.Dropout(0.1)
        self.fc2 = nn.Linear(80, 40)
        self.dropout2 = nn.Dropout(0.1)
        self.fc3 = nn.Linear(40, 20)
        self.dropout3 = nn.Dropout(0.1)
        self.fc4 = nn.Linear(20, 1)

    def forward(self, x):
        x1 = F.leaky_relu(self.bn1(self.conv1(x)), negative_slope=0.01)
        x2 = F.leaky_relu(self.bn2(self.conv2(x1)), negative_slope=0.01)
        x3 = F.leaky_relu(self.bn3(self.conv3(x2)), negative_slope=0.01)

        shortcut = self.shortcut(x1)
        x = x3 + shortcut

        x = self.reduce_features(x)

        batch_size, channels, features, sequence_length = x.size()

        x = x.permute(0, 3, 1, 2)  # [batch_size, sequence_length, channels, features]
        x = x.contiguous().view(batch_size, sequence_length, -1)  # [batch_size, sequence_length, embed_dim]

        assert x.size(2) == self.embed_dim, f"Expected embedding dimension {self.embed_dim}, got {x.size(2)}"

        x, _ = self.attention(x, x, x)

        x = x.contiguous().view(batch_size, -1)  # [batch_size, sequence_length * embed_dim]

        x = F.leaky_relu(self.fc1(x), negative_slope=0.01)
        x = self.dropout1(x)
        x = F.leaky_relu(self.fc2(x), negative_slope=0.01)
        x = self.dropout2(x)
        x = F.leaky_relu(self.fc3(x), negative_slope=0.01)
        x = self.dropout3(x)
        x = self.fc4(x)
        return x

