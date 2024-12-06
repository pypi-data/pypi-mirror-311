import numpy as np


def noise(image: np.ndarray, intensity: int = 20) -> np.ndarray:
    return np.clip(image + np.random.randint(-intensity, intensity, image.shape), 0, 255)
