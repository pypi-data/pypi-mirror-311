import numpy as np
from math import degrees, atan2


class GradientTruth:
    def __init__(self, kernel_size: int = 7):
        self.kernel_size = kernel_size

    def predict(self, image: np.ndarray) -> np.ndarray:
        image = image.astype(int)
        h, w, c = image.shape
        image = image.astype(int)
        gx = np.concatenate(((image[:, 1:] - image[:, :-1]).sum(axis=2), np.zeros((h, 1), dtype=int)), axis=1)
        gy = np.concatenate(((image[1:, :] - image[:-1, :]).sum(axis=2), np.zeros((1, w), dtype=int)), axis=0)

        res = np.zeros_like(gx)
        n = self.kernel_size
        for y in range(h):
            for x in range(w):
                dx = gx[max(0, y - n // 2):y + (n + 1) // 2, max(0, x - n // 2):x + (n + 1) // 2 - 1].sum()
                dy = gy[max(0, y - n // 2):y + (n + 1) // 2 - 1, max(0, x - n // 2):x + (n + 1) // 2].sum()
                res[y, x] = -degrees(atan2(dy, dx)) % 180
        return res
