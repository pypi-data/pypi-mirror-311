import numpy as np
from ..edge import gradient


def points(image: np.ndarray, max_distance: int = 7, gradient_scaler: float = 0,
           darkness_scaler: float = 0) -> np.ndarray:
    gradient_scaler = np.exp(gradient_scaler)
    darkness_scaler = np.exp(darkness_scaler)

    edges = _gradient(image) / 765
    priority = [(edges[y, x], (x, y)) for y in range(len(edges)) for x in range(len(edges[y]))]
    priority.sort(reverse=True)

    image = image.mean(axis=2) / 255

    h, w = image.shape
    pts = np.zeros((h + max_distance * 2, w + max_distance * 2))

    y, x = np.mgrid[-max_distance:max_distance + 1, -max_distance:max_distance + 1]
    dist = (x ** 2 + y ** 2) ** 0.5

    for edge, (x, y) in priority:
        r = max(1, max_distance * (1 - edge) ** gradient_scaler * image[y, x] ** darkness_scaler)

        area = pts[y:y + max_distance * 2 + 1, x:x + max_distance * 2 + 1] * dist
        area = area[np.nonzero(area)]

        if len(area) == 0 or area.min() > r:
            pts[y + max_distance, x + max_distance] = 1
    pts = pts[max_distance:-max_distance, max_distance:-max_distance]
    return 255 - pts * 255
