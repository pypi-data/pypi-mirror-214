import torch
import torchtrain
from torch import nn
import torch.nn.functional as F

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
