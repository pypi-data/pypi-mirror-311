import numpy as np
from ._points import Points
from ..core.angle import GradientTruth
import cv2


class Strokes:
    def __init__(self, mx_length: int = 10):
        self.mx_length = mx_length

    def process(self, image: np.ndarray, angles: np.ndarray = None, points: np.ndarray = None) -> np.ndarray:
        image = image.astype(int)
        h, w, c = image.shape
        if angles is None:
            angles = GradientTruth().predict(image)
        if points is None:
            points = Points(7, 1, 0).process(image)
        pts = points
        gx = np.concatenate((np.abs(image[:, 1:] - image[:, :-1]).sum(axis=2), np.zeros((h, 1), dtype=int)), axis=1)
        gy = np.concatenate((np.abs(image[1:, :] - image[:-1, :]).sum(axis=2), np.zeros((1, w), dtype=int)), axis=0)
        grad = np.maximum(gx, gy) / 765
        surf = np.ones_like(image) * 255
        image = 1 - image.mean(axis=2) / 255
        h, w = pts.shape

        angles[grad < 0.05] = np.random.random(angles.shape)[grad < 0.05] * 180
        angles = np.radians(angles)
        X, Y = np.cos(angles), np.sin(angles)
        for y in range(h):
            for x in range(w):
                if pts[y, x]: continue
                ln = image[y, x] * self.mx_length / 2
                dx, dy = X[y, x], Y[y, x]
                cv2.line(surf, (int(x + ln * dy), int(y + ln * dx)), (int(x - ln * dy), int(y - ln * dx)), (50, 50, 50),
                         1)
        return surf
