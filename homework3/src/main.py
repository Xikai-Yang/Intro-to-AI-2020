import pandas as pd
import numpy as np

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from src.model import *
import gc


torch.device("cuda")
from torch.autograd import Variable

# ================== Data Preparation ==================================


class MNISTDataset(Dataset):
    """MNIST dtaa set"""

    def __init__(self, dataframe,
                 transform=transforms.Compose([transforms.ToPILImage(),
                                               transforms.ToTensor(),
                                               transforms.Normalize(mean=(0.5,), std=(0.5,))])
                 ):
        df = dataframe
        # for MNIST dataset n_pixels should be 784
        self.n_pixels = 784

        if len(df.columns) == self.n_pixels:
            # test data
            self.X = df.values.reshape((-1, 28, 28)).astype(np.uint8)[:, :, :, None]
            self.y = None
        else:
            # training data
            self.X = df.iloc[:, 1:].values.reshape((-1, 28, 28)).astype(np.uint8)[:, :, :, None]
            self.y = torch.from_numpy(df.iloc[:, 0].values)

        self.transform = transform

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        if self.y is not None:
            return self.transform(self.X[idx]), self.y[idx]
        else:
            return self.transform(self.X[idx])


def get_dataset(dataframe, dataset=MNISTDataset,
                transform=transforms.Compose([transforms.ToPILImage(),
                                              transforms.ToTensor(),
                                              transforms.Normalize(mean=(0.5,), std=(0.5,))])):
    return dataset(dataframe, transform=transform)


def split_dataframe(dataframe=None, fraction=0.9, rand_seed=1):
    df_1 = dataframe.sample(frac=fraction, random_state=rand_seed)
    df_2 = dataframe.drop(df_1.index)
    return df_1, df_2


train = pd.read_csv(r"../input/digit-recognizer/train.csv", dtype=np.float32)
train_df, val_df = split_dataframe(train)
val_test_transforms = transforms.Compose(
    [transforms.ToPILImage(),
     transforms.ToTensor(),
     transforms.Normalize(mean=(0.5,), std=(0.5,))])
train_transforms = transforms.Compose(
    [transforms.ToPILImage(), transforms.ToTensor(), transforms.Normalize(mean=(0.5,), std=(0.5,))])
batch_size = 100

train_dataset = get_dataset(train_df, transform=train_transforms)
val_dataset = get_dataset(val_df, transform=val_test_transforms)

train_loader = torch.utils.data.DataLoader(dataset=train_dataset,
                                           batch_size=batch_size, shuffle=False)
val_loader = torch.utils.data.DataLoader(dataset=val_dataset,
                                         batch_size=batch_size, shuffle=False)

# ==================================================================


def train(model, train_loader, val_loader, num_epochs, optimizer):
    error = nn.CrossEntropyLoss()
    count = 0
    loss_list = []
    iteration_list = []
    accuracy_list = []

    for epoch in range(num_epochs):
        for i, (images, labels) in enumerate(train_loader):

            train = Variable(images.view(-1, 1, 28, 28)).cuda()
            labels = Variable(labels).type(torch.LongTensor).cuda()

            # Clear gradients
            optimizer.zero_grad()

            # Forward propagation
            outputs = model(train)

            # Calculate softmax and ross entropy loss
            loss = error(outputs, labels)

            # Calculating gradients
            loss.backward()

            # Update parameters
            optimizer.step()

            count += 1
            if count % 50 == 0:
                # Calculate Accuracy
                correct = 0
                total = 0
                # Iterate through test dataset
                for images, labels in val_loader:
                    test = Variable(images.view(-1, 1, 28, 28)).cuda()
                    labels = labels.type(torch.LongTensor).cuda()

                    # Forward propagation
                    outputs = model(test)

                    # Get predictions from the maximum value
                    predicted = torch.max(outputs.data, 1)[1]

                    # Total number of labels
                    total += len(labels)

                    correct += (predicted == labels).sum()
                accuracy = 100 * correct / float(total)
                loss_list.append(loss.data)
                iteration_list.append(count)
                accuracy_list.append(accuracy)
            if count % 500 == 0:
                # Print Loss
                print('Iteration: {}  Loss: {}  Accuracy: {} %'.format(count, loss.data, accuracy))

    return iteration_list, accuracy_list, loss_list




# ================= Hyperparamater tuning =========================


def tensor2Series(ans_list):
    return pd.Series([ans_list[i].tolist() for i in range(len(ans_list))])


def hyperparameters_tuning(num_epochs, write_file=True):
    optim_type = ["Adam", "SGD"]
    learning_rate_list = [0.001, 0.01, 0.1]
    accu_dict = {}
    loss_dict = {}
    for optim in optim_type:
        for lr in learning_rate_list:
            key = optim + "_" + str(lr)
            print(key)
            model = MnistNet().cuda()
            if optim == "SGD":
                optimizer = torch.optim.SGD(model.parameters(), lr=lr)
            if optim == "Adam":
                optimizer = torch.optim.Adam(model.parameters(), lr=lr)
            _, temp_accu_list, temp_loss_list = train(model, train_loader, val_loader, num_epochs, optimizer)
            accu_dict[key] = tensor2Series(temp_accu_list)
            loss_dict[key] = tensor2Series(temp_loss_list)
            del model
            gc.collect()
    if write_file:
        pd.DataFrame(loss_dict).to_csv("optimizer_loss.csv")
        pd.DataFrame(accu_dict).to_csv("optimizer_accu.csv")


hyperparameters_tuning(20, False)

# ================================================================

# ================= Train the model ===============================


model = MnistNet().cuda()
num_epochs = 50
optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
orig_iteration_list, orig_accu_list, orig_loss_list = train(model, train_loader, val_loader,num_epochs, optimizer)

# ================================================================

# =================================== prediction ===============================

test_features = pd.read_csv("../input/digit-recognizer/test.csv", dtype=np.float32)

test_dataset = get_dataset(test_features, transform=val_test_transforms)

test_loader = torch.utils.data.DataLoader(dataset=test_dataset,
                                          batch_size=batch_size, shuffle=False)
test_pred = torch.LongTensor().cuda()

for images in test_loader:

    test = Variable(images.view(batch_size,1,28,28)).cuda()

    # Forward propagation
    outputs = model(test)

    # Get predictions from the maximum value
    predicted = torch.max(outputs.data, 1)[1]

    test_pred = torch.cat((test_pred, predicted), dim = 0)

index = pd.Series(list(range(1, test_pred.size()[0]+1)), name = "ImageId")
ans = pd.Series(test_pred.tolist(), name = "Label")
submission = pd.concat([index, ans], axis = 1)

# ===============================================================================
