import cv2
import numpy as np
import math
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


def variate_color(img: np.ndarray, hue_shift: int = 0, saturation_shift: int = 0,
                  luminosity_shift: int = 0) -> np.ndarray:
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV_FULL)
    shifts = [hue_shift, saturation_shift, luminosity_shift]

    for i, shift in enumerate(shifts):
        if shift != 0:
            hsv[:, :, i] = np.clip((hsv[:, :, i].astype(np.int16) + shift), 0, 255).astype(np.uint8)

    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR_FULL)


def generate_color_set(img: np.ndarray, n: int, max_img_size: int = 200) -> np.ndarray:
    ratio = min(1.0, float(max_img_size) / img.shape[1], float(max_img_size) / img.shape[0])
    resized_img = cv2.resize(img, (int(img.shape[1] * ratio), int(img.shape[0] * ratio),), interpolation=cv2.INTER_AREA)
    clt = KMeans(n_clusters=n, n_init=10)
    clt.fit(resized_img.reshape(-1, 3))

    return clt.cluster_centers_


def extend_color_set(colors: np.ndarray, extensions: list[tuple[int, int, int]]) -> np.ndarray:
    reshaped_colors = colors.reshape((1, len(colors), 3)).astype(np.uint8)
    extended_colors = [variate_color(reshaped_colors, *x).reshape((-1, 3)) for x in extensions]
    all_colors = np.vstack([colors.reshape((-1, 3))] + extended_colors)

    return all_colors


def visualize_color_set(colors: np.ndarray, cell_size: int = 80) -> np.ndarray:
    n = len(colors)
    cols = 10
    rows = math.ceil(n / cols)
    res = np.full((rows * cell_size, cols * cell_size, 3), 255, dtype=np.uint8)

    for i, color in enumerate(colors):
        y, x = divmod(i, cols)
        y0, y1 = y * cell_size, (y + 1) * cell_size
        x0, x1 = x * cell_size, (x + 1) * cell_size
        res[y0:y1, x0:x1] = color

    plt.figure(figsize=(10, 4))
    plt.imshow(cv2.cvtColor(res, cv2.COLOR_BGR2RGB))
    plt.show()

    return res


if __name__ == "__main__":
    img = cv2.imread("../../../_demo/images/img.png")
    colors = generate_color_set(img, 10)
    extended_colors = extend_color_set(colors, [(0, 50, 0), (15, 30, 0), (-15, 30, 0)])
    visualize_color_set(extended_colors)

    print("Done")
