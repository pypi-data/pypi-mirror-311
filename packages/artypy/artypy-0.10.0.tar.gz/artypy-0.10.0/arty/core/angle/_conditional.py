import numpy as np
from queue import PriorityQueue
from . import GradientTruth


class Conditional:
    def predict(self, image: np.ndarray, angles: np.ndarray = None) -> np.ndarray:
        def closest(orig, angle):
            angles = [(abs(orig - i), i) for i in [angle - 180, angle, angle + 180]]
            return min(angles)[1]

        image = image.astype(int)
        h, w, c = image.shape
        if angles is None:
            angles = GradientTruth().predict(image)
        gx = np.concatenate((np.abs(image[:, 1:] - image[:, :-1]).sum(axis=2), np.zeros((h, 1), dtype=int)), axis=1)
        gy = np.concatenate((np.abs(image[1:, :] - image[:-1, :]).sum(axis=2), np.zeros((1, w), dtype=int)), axis=0)
        edges = np.maximum(gx, gy)
        edges = edges.copy()
        used = np.zeros_like(angles)
        q = PriorityQueue()
        for y in range(len(edges)):
            for x in range(len(edges[y])):
                q.put((-edges[y, x], (x, y)))
        while not q.empty():
            _, (x, y) = q.get()
            if used[y, x]: continue
            used[y, x] = 1
            edge = edges[y, x]
            angle = angles[y, x]
            for X in range(max(0, x - 1), min(x + 2, w)):
                for Y in range(max(0, y - 1), min(y + 2, h)):
                    if used[Y, X]: continue
                    ang = closest(angle, angles[Y, X])
                    ed = edges[Y, X]
                    ang = (ang + (angle - ang) * (edge - ed) / max(1, edge)) % 180
                    angles[Y, X] = ang
                    edges[Y, X] = (edge + ed) / 2
                    q.put((-edges[Y, X], (X, Y)))
        return angles
