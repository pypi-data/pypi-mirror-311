from random import random
import numpy as np


def angle2line(angle):
    angle = np.radians(angle)
    x1, y1 = np.cos(angle), np.sin(angle)
    x2, y2 = -x1, -y1
    b = x2 - x1
    a = y1 - y2

    return a, b, random() - 0.5


def angle2array(angle):
    angle %= 180
    i1, i2, i3 = angle < 60, (60 <= angle) & (angle < 120), (120 <= angle) & (angle <= 180)
    array = np.zeros((angle.shape[0], 3))
    array[i1] = np.array([1 - angle / 60, angle / 60, angle * 0]).T[i1]

    angle -= 60
    array[i2] = np.array([angle * 0, 1 - angle / 60, angle / 60]).T[i2]

    angle -= 60
    array[i3] = np.array([angle / 60, angle * 0, 1 - angle / 60]).T[i3]

    return array


def array2angle(array):
    ind = array.argmin(1)
    array[np.arange(ind.size), ind] = 0
    array /= array.sum(1)[:, None]
    add = (ind + 1) % 3
    ind = (ind - 1) % 3
    angles = 60 * (add + array[np.arange(ind.size), ind])

    return angles


def draw(angles, colors, size):
    X, Y = (size - 1) / 2, (size - 1) / 2
    lines = sorted([angle2line(angle) for angle in angles], key=lambda line: line[-1])
    y, x = np.mgrid[0:size, 0:size]
    y, x = y - Y, x - X
    kernel = np.ones((size, size, 3)) * colors[0]

    for (a, b, c), color in zip(lines, colors[1:]):
        kernel[a * y + b * x + c * size < 0] = color

    kernel = np.clip(kernel + (np.random.random(kernel.shape) - 0.5) * 0.2, 0, 1)

    return kernel


def get_batch(kernel_size, batch_size=32):
    input, output = [], []

    for _ in range(batch_size):
        angle = random() * 180
        angles = [angle + (random() - 0.5) * 30]
        colors = [np.random.random(3), np.random.random(3)]

        while random() < 0.25:
            colors.append(np.random.random(3))
            angles.append(angle + (random() - 0.5) * 30)

        input.append(draw(angles, colors, kernel_size))
        output.append(sum(angles) / len(angles))

    input = np.array(input)
    output = np.array(output)
    output = angle2array(output)

    return input, output
