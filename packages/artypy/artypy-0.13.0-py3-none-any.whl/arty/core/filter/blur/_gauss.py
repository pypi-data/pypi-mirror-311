import numpy as np


def gauss(image: np.ndarray, kernel_size: int = 3, sigma: float = 1.0) -> np.ndarray:
    kernel = np.zeros((kernel_size, kernel_size))
    for x in range(kernel_size):
        for y in range(kernel_size):
            kernel[y, x] = np.exp(-((x - kernel_size // 2) ** 2 + (y - kernel_size // 2) ** 2) / (2 * sigma ** 2)) / (
                    2 * np.pi * sigma ** 2)
    kernel /= kernel.sum()

    kernel = np.array([
        [1, 2, 1],
        [2, 4, 2],
        [1, 2, 1]
    ]) / 16

    h, w, c = image.shape
    n = kernel_size
    new = image.copy()
    for y in range(n // 2, h - (n + 1) // 2):
        for x in range(n // 2, w - (n + 1) // 2):
            new[y, x] = [i.sum() for i in image[y - n // 2:y + (n + 1) // 2, x - n // 2:x + (n + 1) // 2].T * kernel]
    return new.astype('uint8')
