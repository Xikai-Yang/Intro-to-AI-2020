import torch
import torch.nn as nn
import torch.nn.functional as F
torch.device("cuda")
from torch.autograd import Variable


class MnistNet(nn.Module):
    def __init__(self):
        super(MnistNet, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=(5, 5))  # 28*28
        self.bn1 = nn.BatchNorm2d(32)
        self.conv2 = nn.Conv2d(32, 32, kernel_size=(5, 5))  # 24
        self.bn2 = nn.BatchNorm2d(32)
        self.conv2_drop = nn.Dropout2d(p=0.2)
        self.fc1 = nn.Linear(128, 100)
        self.fc2 = nn.Linear(100, 10)
        self.conv3 = nn.Conv2d(32, 64, kernel_size=(3, 3))
        self.bn3 = nn.BatchNorm2d(64)
        self.conv4 = nn.Conv2d(64, 64, kernel_size=(3, 3))
        self.bn4 = nn.BatchNorm2d(64)
        self.conv5 = nn.Conv2d(64, 128, kernel_size=(3, 3))
        self.bn5 = nn.BatchNorm2d(128)
        self.conv6 = nn.Conv2d(128, 128, kernel_size=(1, 1))
        self.bn6 = nn.BatchNorm2d(128)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = self.bn1(x)

        x = F.relu(self.conv2(x))
        x = self.conv2_drop(F.max_pool2d(self.bn2(x), 2))  # 10 * 10 * 32

        x = F.relu(self.conv3(x))  # 8 * 8 * 64
        x = self.bn3(x)

        x = F.relu(self.conv4(x))  # 6 * 6 * 64
        x = self.bn4(x)
        x = F.max_pool2d(x, 2)  # 3 * 3 * 64
        x = self.conv2_drop(x)

        x = F.relu(self.conv5(x))  # 1 * 1 * 128
        x = self.bn5(x)

        x = F.relu(self.conv6(x))  # 1 * 1 * 128
        x = self.bn6(x)
        size = x.size()[1] * x.size()[2] * x.size()[3]

        x = x.view(-1, size)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x


class ANN(nn.Module):
    def __init__(self, input_dim=784, output_dim=10):
        super(ANN, self).__init__()

        # Input Layer (784) -> 784
        self.fc1 = nn.Linear(input_dim, 784)
        # 784 -> 128
        self.fc2 = nn.Linear(784, 128)
        # 128 -> 128
        self.fc3 = nn.Linear(128, 128)
        # 128 -> 64
        self.fc4 = nn.Linear(128, 64)
        # 64 -> 64
        self.fc5 = nn.Linear(64, 64)
        # 64 -> 32
        self.fc6 = nn.Linear(64, 32)
        # 32 -> 32
        self.fc7 = nn.Linear(32, 32)
        # 32 -> output layer(10)
        self.output_layer = nn.Linear(32, 10)
        # Dropout Layer (20%) to reduce overfitting
        self.dropout = nn.Dropout(0.2)

    def forward(self, x):
        # flatten image input
        x = x.view(-1, 28 * 28)

        # Add ReLU activation function to each layer
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        # Add dropout layer
        x = self.dropout(x)
        x = F.relu(self.fc4(x))
        x = F.relu(self.fc5(x))
        x = self.dropout(x)
        x = F.relu(self.fc6(x))
        x = F.relu(self.fc7(x))
        x = self.dropout(x)
        # Don't add any ReLU activation function to Last Output Layer
        x = self.output_layer(x)

        # Return the created model
        return x


class LeNet(nn.Module):

    def __init__(self):
        super(LeNet, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 6, kernel_size=5),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2),  # 12*12
            nn.Conv2d(6, 16, kernel_size=5),  # 16* 8 * 8
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2),  # 4*4*16
        )

        self.model = nn.Sequential(

            nn.Linear(256, 120),
            nn.ReLU(),
            nn.Linear(120, 84),  # (N, 120) -> (N, 84)
            nn.ReLU(),
            nn.Linear(84, 10)
        )

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.model(x)
        return x


class AlexNet(nn.Module):
    def __init__(self, num_classes=10):
        super(AlexNet, self).__init__()
        self.feature = nn.Sequential(
            nn.Conv2d(1, 96, kernel_size=3, stride=2, padding=1, bias=False),  # 14 * 14 * 96
            nn.BatchNorm2d(96),
            nn.ReLU(True),
            nn.MaxPool2d(kernel_size=2, stride=2),  # 7 * 7 * 96
            nn.Conv2d(96, 256, kernel_size=3, stride=1, padding=1, bias=False),  # 7*7*256
            nn.BatchNorm2d(256),
            nn.ReLU(True),
            nn.Conv2d(256, 384, kernel_size=3, stride=2, padding=1, bias=False),  # 4*4*384
            nn.BatchNorm2d(384),
            nn.ReLU(True),
            nn.Conv2d(384, 384, kernel_size=3, stride=2, padding=1, bias=False),  # 2*2*384
            nn.BatchNorm2d(384),
            nn.ReLU(True),
            nn.Conv2d(384, 384, kernel_size=3, stride=1, padding=1, bias=False),  # 2*2*384
            nn.BatchNorm2d(384),
            nn.ReLU(True),
            nn.Conv2d(384, 256, kernel_size=3, stride=1, padding=1, bias=False),  # 2*2*256
            nn.BatchNorm2d(256),
            nn.ReLU(True),
            nn.MaxPool2d(kernel_size=2, stride=2)  # 1*1*256
        )
        self.classifier = nn.Sequential(
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, num_classes)
        )

    def forward(self, x):
        out = self.feature(x)
        out = out.view(out.size(0), -1)
        out = self.classifier(out)
        return out



