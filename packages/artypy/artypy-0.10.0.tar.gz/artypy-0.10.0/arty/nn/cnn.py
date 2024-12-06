import numpy as np
import torch

from arty.core.angle import cnn



class CNN:
    def __init__(self, kernel_size: int = 5, path: str = ''):
        """
        Initialize CNN model for angle prediction. If the model exists, it will be loaded, otherwise, it will be created and saved.
        :param kernel_size: kernel size of the convolutional neural network
        :param path: path to the model, if not provided, it will be saved as '{kernel_size}.pt'
        """
        self.kernel_size = kernel_size
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

        self.path = path
        if self.path == '':
            self.path = f'{kernel_size}.pt'

        self.model = cnn.model(self.path, kernel_size, device=self.device)

    def fit(self, max_epochs: int = -1):
        """
        Train the model.
        :param max_epochs: maximum number of epochs, if -1, the model will be trained until the loss stops decreasing
        """
        self.model = cnn.train(self.model, self.kernel_size, self.device, self.path, max_epochs)

    def predict(self, image: np.ndarray) -> np.ndarray:
        """
        Predict the angles of the image.
        :param image: input image
        :return: angles of the image as numpy array
        """
        h, w, c = image.shape
        s, e = (self.kernel_size - 1) // 2, self.kernel_size // 2
        img = np.zeros((h + s + e, w + s + e, c))
        img[s:-e, s:-e] = image

        img = torch.tensor(img).to(self.device).float().T / 255

        angle = self.model(img).T
        shape = angle.shape[:-1]
        angle = angle.reshape(-1, 3).cpu().detach().numpy()
        angle = cnn.array2angle(angle).reshape(shape)

        return angle
