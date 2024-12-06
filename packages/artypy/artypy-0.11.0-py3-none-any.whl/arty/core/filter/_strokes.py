import numpy as np
from ._points import points
from ..edge import gradient
import pygame


def strokes(image: np.ndarray, angles: np.ndarray, mx_length=10) -> np.ndarray:
    pts = points(image, 7, 1, 0)
    grad = gradient(image) / 765
    image = 1 - image.mean(axis=2) / 255
    h, w = pts.shape

    surf = pygame.Surface((w, h))
    surf.fill((255, 255, 255))

    angles[grad < 0.3] = np.random.random(angles.shape)[grad < 0.3] * 180
    angles = np.radians(angles)
    X, Y = np.cos(angles), np.sin(angles)
    for y in range(h):
        for x in range(w):
            if pts[y, x]: continue
            ln = image[y, x] * grad[y, x] * mx_length / 2
            dx, dy = X[y, x], Y[y, x]
            pygame.draw.aaline(surf, (50, 50, 50), (x + ln * dy, y + ln * dx), (x - ln * dy, y - ln * dx))
    return pygame.surfarray.pixels3d(surf).transpose(1, 0, 2)
