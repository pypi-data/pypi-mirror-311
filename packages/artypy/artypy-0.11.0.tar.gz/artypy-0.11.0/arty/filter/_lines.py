import numpy as np
from math import radians, cos, sin
import cv2
from ..core.angle import GradientTruth


class Lines:
    def __init__(self, thickness: int = 3, max_length: int = 10, noise_intensity=20):
        self.thickness = thickness
        self.max_length = max_length
        self.noise_intensity = noise_intensity

    def process(self, image: np.ndarray, angles: np.ndarray = None) -> np.ndarray:
        image = image.astype(int)
        h, w, c = image.shape
        if angles is None:
            angles = GradientTruth().predict(image)
        gx = np.concatenate((np.abs(image[:, 1:] - image[:, :-1]).sum(axis=2), np.zeros((h, 1), dtype=int)), axis=1)
        gy = np.concatenate((np.abs(image[1:, :] - image[:-1, :]).sum(axis=2), np.zeros((1, w), dtype=int)), axis=0)
        edges = np.maximum(gx, gy)
        image = np.clip(image + (np.random.random(image.shape) - 0.5) * self.noise_intensity, 0, 255)
        priority = [(edges[y, x], (x, y)) for y in range(len(edges)) for x in range(len(edges[y]))]
        priority.sort(reverse=True)
        new = np.zeros_like(image)
        for _, (x, y) in priority:
            if new[y, x].max() != 0: continue
            angle = radians(angles[y, x])
            dy, dx = int(cos(angle) * self.max_length / 2), int(sin(angle) * self.max_length / 2)
            cv2.line(new, (x - dx, y - dy), (x + dx, y + dy), image[y, x].tolist(), self.thickness)
        return new.astype('uint8')
