import numpy as np


class Points:
    def __init__(self, max_distance: int = 7, gradient_scaler: float = 0, darkness_scaler: float = 0):
        self.max_distance = max_distance
        self.gradient_scaler = gradient_scaler
        self.darkness_scaler = darkness_scaler

    def process(self, image: np.ndarray) -> np.ndarray:
        gradient_scaler = np.exp(self.gradient_scaler)
        darkness_scaler = np.exp(self.darkness_scaler)

        image = image.astype(int)
        h, w, c = image.shape
        gx = np.concatenate((np.abs(image[:, 1:] - image[:, :-1]).sum(axis=2), np.zeros((h, 1), dtype=int)), axis=1)
        gy = np.concatenate((np.abs(image[1:, :] - image[:-1, :]).sum(axis=2), np.zeros((1, w), dtype=int)), axis=0)
        edges = np.maximum(gx, gy) / 765
        priority = [(edges[y, x], (x, y)) for y in range(len(edges)) for x in range(len(edges[y]))]
        priority.sort(reverse=True)

        image = image.mean(axis=2) / 255

        h, w = image.shape
        pts = np.zeros((h + self.max_distance * 2, w + self.max_distance * 2))

        y, x = np.mgrid[-self.max_distance:self.max_distance + 1, -self.max_distance:self.max_distance + 1]
        dist = (x ** 2 + y ** 2) ** 0.5
        d = np.ones_like(pts) * 10 * self.max_distance

        for edge, (x, y) in priority:
            r = max(1, self.max_distance * (1 - edge) ** gradient_scaler * image[y, x] ** darkness_scaler)
            if d[y + self.max_distance, x + self.max_distance] > r:
                pts[y + self.max_distance, x + self.max_distance] = 1
                d[y:y + self.max_distance * 2 + 1, x:x + self.max_distance * 2 + 1] = np.minimum(
                    d[y:y + self.max_distance * 2 + 1, x:x + self.max_distance * 2 + 1], dist)
        pts = pts[self.max_distance:-self.max_distance, self.max_distance:-self.max_distance]
        return 255 - pts * 255
