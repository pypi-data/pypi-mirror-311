import numpy as np
import pygame
from math import radians, cos, sin


def lines(image: np.ndarray, angles: np.ndarray, edges: np.ndarray) -> np.ndarray:
    priority = [(edges[y, x], (x, y)) for y in range(len(edges)) for x in range(len(edges[y]))]
    h, w, c = image.shape
    new = pygame.Surface((w, h))
    for _, (x, y) in priority[::-1]:
        if new.get_at((x, y)) != (0, 0, 0, 255): continue
        angle = radians(angles[y, x])
        dy, dx = cos(angle) * 5, sin(angle) * 5
        pygame.draw.line(new, image[y, x], (x - dx, y - dy), (x + dx, y + dy), 3)
    return pygame.surfarray.pixels3d(new).transpose(1, 0, 2)
