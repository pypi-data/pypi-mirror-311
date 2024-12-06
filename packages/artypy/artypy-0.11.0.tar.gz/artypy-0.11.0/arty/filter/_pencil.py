import numpy as np
import cv2
from ..core.angle import GradientTruth


class Pencil:
    def __init__(self, edge_scaler: float = 0.7, bg_scaler: float = 0.7, max_length: int = 7, noise_intensity=100):
        self.edge_scaler = edge_scaler
        self.bg_scaler = bg_scaler
        self.max_length = max_length
        self.noise_intensity = noise_intensity

    def process(self, image: np.ndarray, angles: np.ndarray = None) -> np.ndarray:
        image = image.astype(int)
        h, w, c = image.shape
        if angles is None:
            angles = GradientTruth().predict(image)
        gx = np.concatenate((np.abs(image[:, 1:] - image[:, :-1]).sum(axis=2), np.zeros((h, 1), dtype=int)), axis=1)
        gy = np.concatenate((np.abs(image[1:, :] - image[:-1, :]).sum(axis=2), np.zeros((1, w), dtype=int)), axis=0)
        edges = np.maximum(gx, gy) / 765
        edges = np.clip(edges + (np.random.random(edges.shape) - 0.5) * 0.01, 0, 1)
        image = np.clip(image + (np.random.random(image.shape) - 0.5) * self.noise_intensity, 0, 255)
        color = (255 - image.mean(axis=2))
        color = np.maximum(color * self.bg_scaler, edges ** (1 - self.edge_scaler) * 255)

        angles = np.radians(angles)
        dx, dy = np.cos(angles) * self.max_length, np.sin(angles) * self.max_length
        dx, dy = dx * (1 - color / 255), dy * (1 - color / 255)
        dx, dy = dx.astype(int), dy.astype(int)
        surf = np.zeros_like(image)
        priority = [(color[y, x], (x, y)) for y in range(len(edges)) for x in range(len(edges[y]))]
        priority.sort()
        for col, (x, y) in priority:
            cv2.line(surf, (x + dy[y, x], y + dx[y, x]), (x - dy[y, x], y - dx[y, x]), (col, col, col), 1)
        return (255 - surf).astype("uint8")
