import numpy as np
from scipy.signal import convolve2d


class GradientTruth:
    def __init__(self, kernel_size: int = 7):
        self.kernel_size = kernel_size

    def predict(self, image: np.ndarray) -> np.ndarray:
        image = image.astype(int)
        h, w, c = image.shape
        image = image.astype(int)
        gx = np.concatenate(((image[:, 1:] - image[:, :-1]).sum(axis=2), np.zeros((h, 1), dtype=int)), axis=1)
        gy = np.concatenate(((image[1:, :] - image[:-1, :]).sum(axis=2), np.zeros((1, w), dtype=int)), axis=0)

        n = self.kernel_size

        dx = convolve2d(gx, np.ones((n, n)), mode='same')
        dy = convolve2d(gy, np.ones((n, n)), mode='same')
        res = -np.degrees(np.arctan2(dy, dx)) % 180
        return res
