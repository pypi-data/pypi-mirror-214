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

    def predict(self, X, y,
                epochs=10,
                batch_size=32,
                learning_rate=0.01,
                criterion=nn.NLLLoss,
                optimizer=optim.SGD,
                by_method='abs'):
        methods = ['abs', 'std']
        if by_method not in methods:
            raise ValueError(f'method must be {methods}')
        result = super().predict(X, y, epochs, batch_size, learning_rate, criterion, optimizer)

        if by_method == 'abs':
            return self.result_abs(y,result)
        elif by_method == 'std':
            return self.result_std(y,result)

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
        return self.fit(X, y,
                        epochs,
                        batch_size,
                        learning_rate,
                        criterion,
                        optimizer,
                        ).predict(X, y, epochs, batch_size, learning_rate, criterion, optimizer, by_method='abs')

    def result_abs(self,y_true,y_pred):
        result = np.abs(y_true - y_pred)
        return result

    def result_std(self,y_true,y_pred):
        std_2 = np.std(y_true,axis = 0) * 2
        vfunc = np.vectorize(lambda x: 1 if x in range(x-std_2,x+std_2+1) else 0)
        result = vfunc(y_pred)
        return result
