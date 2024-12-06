import cv2
import math
import numpy as np


class Gradient:
    def __init__(self, image, type="sharr", type_smoothing="gaussian", radius=1, smoothing_iterations=1):
        """
        :param image: np.ndarray or cv2.UMat, grayscale or RGB image
        :param type: "sharr", "sobel", default is "sharr"
        :param type_smoothing: "gaussian", "bilateral", "none", default is "gaussian"
        :param radius: radius of the smoothing kernel, default is 1
        :param smoothing_iterations: number of smoothing iterations, default is 1
        """
        self.type = type
        self.type_smoothing = type_smoothing
        self.radius = radius
        self.gray_image = image
        print(type, type_smoothing, radius, smoothing_iterations)

        # if image is np.ndarray, convert to cv2 image
        if isinstance(image, np.ndarray):
            if len(image.shape) == 2:
                gray_image = image
            elif len(image.shape) == 3:
                gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            else:
                raise ValueError(f"Invalid image shape: {image.shape}, m ust be (h, w) or (h, w, 3)")
        # elif image is cv2 image, make it grayscale
        elif isinstance(image, cv2.UMat):
            if image.channels == 1:
                gray_image = image
            elif image.channels == 3:
                gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            else:
                raise ValueError(f"Invalid image channels: {image.channels}, must be 1 or 3")
        else:
            raise ValueError(f"Invalid image type: {type(image)}, must be np.ndarray or cv2.UMat")

        if self.type == "sharr":
            self.grad_x = cv2.Scharr(self.gray_image, cv2.CV_64F, 1, 0)
            self.grad_y = cv2.Scharr(self.gray_image, cv2.CV_64F, 0, 1)
        elif self.type == "sobel":
            self.grad_x = cv2.Sobel(self.gray_image, cv2.CV_64F, 1, 0)
            self.grad_y = cv2.Sobel(self.gray_image, cv2.CV_64F, 0, 1)
        else:
            raise ValueError("Invalid gradient type: %s" % self.type)

        s = 2 * self.radius + 1
        for _ in range(smoothing_iterations):
            if self.type_smoothing == "gaussian":
                self.grad_x = cv2.GaussianBlur(self.grad_x, (s, s), 0)
                self.grad_y = cv2.GaussianBlur(self.grad_y, (s, s), 0)
            elif self.type_smoothing == "bilateral":
                self.grad_x = cv2.bilateralFilter(self.grad_x, s, 75, 75)
                self.grad_y = cv2.bilateralFilter(self.grad_y, s, 75, 75)
            elif self.type_smoothing == "none":
                pass
            else:
                raise ValueError("Invalid gradient smoothing type: %s" % self.type_smoothing)
        #
        self.gradient = np.maximum(np.abs(self.grad_x), np.abs(self.grad_y))

    def angle(self, i, j):
        return np.arctan2(self.grad_y[i, j], self.grad_x[i, j])

    def strength(self, i, j):
        return np.sqrt(self.grad_x[i, j] ** 2 + self.grad_y[i, j] ** 2)
