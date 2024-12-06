from torch import nn
from ._generate import get_batch
import torch

def model(path, kernel_size, device):
    try:
        model = torch.load(path)
    except FileNotFoundError:
        model = nn.Sequential(
            nn.Conv2d(3, kernel_size ** 2, kernel_size),
            nn.ReLU(),
            nn.Conv2d(kernel_size ** 2, 3, 1),
            nn.Sigmoid(),
        ).to(device)

        torch.save(model, path)

    return model


def train(model, kernel_size, device, path, max_epochs=-1):
    optim = torch.optim.Adam(model.parameters())
    loss_fn = nn.MSELoss()

    best = 1
    remaining = 1000

    epoch = 0
    while remaining:
        epoch += 1
        if max_epochs != -1 and epoch > max_epochs:
            torch.save(model, path)
            break

        input, output = get_batch(kernel_size)
        input = torch.tensor(input).to(device).permute(0, 3, 2, 1).float()
        output = torch.tensor(output).to(device).float()

        out = model(input)
        loss = loss_fn(out, output[:, :, None, None])

        remaining -= 1
        if loss < best:
            remaining += 10
            best = loss
            torch.save(model, path)

        optim.zero_grad()
        loss.backward()
        optim.step()

    return model
