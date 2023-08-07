import torch
import torchtrain
from torch import nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np


class DeepLogTimedelta(torchtrain.Module):
    def __init__(self, input_size, hidden_size, output_size, num_layers=2):
        super().__init__()

        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.num_layers = num_layers

        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.out = nn.Linear(hidden_size, output_size)

    def forward(self, X):
        hidden = self._get_initial_state(X)
        state = self._get_initial_state(X)

        X = X.reshape(X.shape[0], 1, X.shape[1])
        out, hidden = self.lstm(X, (hidden, state))

        out = self.out(out[:, -1, :])
        out = F.relu(out)

        # Return result
        return out

    def _get_initial_state(self, X):
        """Return a given hidden state for X."""
        return torch.zeros(
            self.num_layers,
            X.size(0),
            self.hidden_size
        ).to(X.device)

    def fit_predict(self, X, y,
                    epochs=10,
                    batch_size=32,
                    learning_rate=0.01,
                    criterion=nn.NLLLoss,
                    optimizer=optim.SGD,
                    by_method='abs'):
        """Train the module with given parameters

            Parameters
            ----------
            X : torch.Tensor
                Tensor to train with

            y : torch.Tensor
                Target tensor

            epochs : int, default=10
                Number of epochs to train with

            batch_size : int, default=32
                Default batch size to use for training

            learning_rate : float, default=0.01
                Learning rate to use for optimizer

            criterion : nn.Loss, default=nn.NLLLoss
                Loss function to use

            optimizer : optim.Optimizer, default=optim.SGD
                Optimizer to use for training

            by_method: str, method use for implement result
            Returns
            -------
            result : torch.Tensor
                Resulting prediction
            """
        return self.fit(X,
                        batch_size,
                        ).predict(X=X, batch_size=batch_size)

    def result_abs(self, y_true, y_pred):
        result = np.abs(y_true - y_pred)
        return result

    def result_std(self, y_true, y_pred, koef=2):
        flatten_y = y_true.flatten()
        std_2 = torch.std(flatten_y).item() * koef
        result = []
        y_pred = y_pred.flatten()
        for i in range(len(y_pred)):
            if y_true[i] - std_2 <= y_pred[i] <= y_true[i] + std_2:
                result.append(1)
            else:
                result.append(0)
        return result

    def result_std_mean(self, y_true, koef=2, window=20):
        y_true = y_true.flatten()
        result = [0 for i in range(window)]
        for i in range(window, len(y_true) - window):
            temp_values = y_true[i - window:i + window + 1]
            temp_std = torch.std(temp_values).item()
            temp_mean = torch.mean(temp_values).item()
            if y_true[i] > temp_mean + temp_std * koef:
                result.append(1)
            else:
                result.append(0)
        for i in range(window):
            result.append(0)
        return result

    # mean , get point by window, find mean and std, get koef and x20>mean+std*koef
