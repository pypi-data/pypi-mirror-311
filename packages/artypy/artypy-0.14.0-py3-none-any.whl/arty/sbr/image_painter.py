import scipy
import bisect

from arty.core.brush import Brush
from arty.core.color import generate_color_set, extend_color_set
from arty.core.edge.gradient import Gradient

import random

from random import shuffle

import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
from tqdm import tqdm


class RandomGrid:
    def __init__(self, height, width, scale):
        """
        Initialize the random grid.
        :param height: height of the image
        :param width: width of the image
        :param scale: scale of the grid
        """
        self.height = height
        self.width = width
        self.scale = scale

    def generate(self):
        """
        Generate a random grid.
        :return: list of grid points
        """
        radius = self.scale // 2

        grid = [
            ((y + random.randint(-radius, radius)) % self.height,
             (x + random.randint(-radius, radius)) % self.width)
            for y in range(0, self.height, self.scale)
            for x in range(0, self.width, self.scale)
        ]

        random.shuffle(grid)

        return grid


class ImagePainter:
    def __init__(self, image, preset):
        """
        Initialize the image painter.
        :param image: input image as numpy array
        :param preset: preset object
        """
        self.image = image
        self.preset = preset
        self.brush = Brush(self.preset.brush_type)
        self.stroke_scale = self._compute_stroke_scale()
        self.gradient_smoothing_radius = self._compute_smoothing_radius()
        self.color_set = None
        self.gradient = None
        self.k = 9
        self.result = None
        self.gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        self.luminance = 0.299 * image[:, :, 2] + 0.587 * image[:, :, 1] + 0.114 * image[:, :, 0]

    def _compute_stroke_scale(self):
        return int(
            math.ceil(max(self.image.shape) / 1000)) if self.preset.stroke_scale == 0 else self.preset.stroke_scale

    def _compute_smoothing_radius(self):
        return int(round(
            max(self.image.shape) / 50)) if self.preset.gradient_smoothing_radius == 0 else self.preset.gradient_smoothing_radius

    def prepare_color_set(self):
        """Generate and extend the color set."""
        print("Computing color set...")
        image = self.gray_image if self.preset.grayscale else self.image
        max_img_size = 200
        self.color_set = generate_color_set(image, self.preset.palette_size, max_img_size)
        print("Extending color color set...")

        if not self.preset.grayscale:
            self.color_set = extend_color_set(self.color_set, [(0, 50, 0), (15, 30, 0), (-15, 30, 0)])

    def compute_gradient(self, type="gray"):
        """Compute the gradient of the image."""
        print("Computing gradient...")
        if type == "gray":
            image = self.gray_image
        elif type == "luminance":
            image = self.luminance
            print("luminance")
        else:
            raise ValueError(f"Invalid gradient type: {type}")
        self.gradient = Gradient(image, self.preset.gradient_type, self.preset.gradient_smoothing_type,
                                 self.gradient_smoothing_radius)

    def _color_probabilities(self, pixels):
        """
        Compute color probabilities for the given pixels.
        :param pixels: list of pixels
        :return: color probabilities
        """
        distances = scipy.spatial.distance.cdist(pixels, self.color_set)
        inverted_distances = np.max(distances, axis=1, keepdims=True) - distances
        normalized_distances = inverted_distances / inverted_distances.sum(axis=1, keepdims=True)
        scaled_distances = np.exp(self.k * len(self.color_set) * normalized_distances)
        probabilities = scaled_distances / scaled_distances.sum(axis=1, keepdims=True)

        return np.cumulative_sum(probabilities, axis=1, dtype=np.float32)

    def _get_color(self, probabilities):
        """
        Select a color from the set based on probabilities.
        :param probabilities: color probabilities
        :return: selected color
        """
        r = random.uniform(0, 1)
        i = bisect.bisect_left(probabilities, r)

        return self.color_set[i] if i < len(self.color_set) else self.color_set[-1]

    def paint(self):
        """
        Perform the painting operation in multiple layers.
        :return: painted image
        """
        print("Painting image with multiple layers...")

        self.prepare_color_set()
        self.compute_gradient(type="gray")

        # Initialize the result with a blank canvas
        if self.preset.has_cardboard:
            result = cv2.medianBlur(self.image, 11) if not self.preset.grayscale else cv2.medianBlur(self.gray_image,
                                                                                                     11)
        else:
            result = np.full_like(self.image, 255, dtype=np.uint8)

        # Define stroke scales for multiple layers
        layer_stroke_scales = [self.stroke_scale * factor for factor in self.preset.layer_scales]

        for layer_index, stroke_scale in enumerate(layer_stroke_scales):
            print(f"Painting layer {layer_index + 1} with stroke scale {stroke_scale}...")
            grid = RandomGrid(self.image.shape[0], self.image.shape[1], scale=stroke_scale).generate()

            batch_size = 10000

            for h in tqdm(range(0, len(grid), batch_size)):
                batch = grid[h:min(h + batch_size, len(grid))]
                pixels = np.array([self.image[y, x] for y, x in batch])
                color_probabilities = self._color_probabilities(pixels)

                for i, (y, x) in enumerate(batch):
                    color = self._get_color(color_probabilities[i])
                    angle = math.degrees(self.gradient.angle(y, x)) + 90

                    if self.preset.length_type == "base":
                        length = max(int(round(stroke_scale + stroke_scale * math.sqrt(
                            self.gradient.strength(y, x))) * self.preset.length_scale), 1)
                    elif self.preset.length_type == "inverse":
                        length = max(
                            1,
                            int(1 / round(stroke_scale + stroke_scale * math.sqrt(
                                self.gradient.strength(y, x))) ** 1.9 * 10 * self.preset.length_scale)
                        )
                    else:
                        raise ValueError(f"Invalid length function: {self.preset.length_type}")

                    self.brush.apply(result, (x, y), length, color, stroke_scale, angle, self.preset.length_first_flag)

            self.result = result
            self.show_result()

        self.result = result

        return result

    def show_result(self):
        """Shows the result."""
        plt.figure(figsize=(10, 10))
        plt.subplot(1, 1, 1)

        if self.preset.grayscale:
            plt.imshow(self.result)
        else:
            plt.imshow(cv2.cvtColor(self.result, cv2.COLOR_BGR2RGB))

        plt.show()


class IrregularBrushImagePainter(ImagePainter):
    def __init__(self, image, preset, preset_adv):
        """
        Initialize the advanced image painter with multi-layer support.
        :param image: Input image as a numpy array
        :param preset: Preset object containing parameters
        :param preset_adv: Advanced preset object containing additional parameters like brush sizes and blur factors
        """
        super().__init__(image, preset)
        self.brush_sizes = preset_adv.brush_sizes
        self.blur_factor = preset_adv.blur_factor
        self.min_stroke_length = preset_adv.min_stroke_length
        self.max_stroke_length = preset_adv.max_stroke_length
        self.strokes = []

        # Precompute luminance for the whole image (used in gradients)
        self.luminance = 0.299 * image[:, :, 2] + 0.587 * image[:, :, 1] + 0.114 * image[:, :, 0]
        self.gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        print("Smoothing: ", self.preset.gradient_smoothing_type)

    def blur_image(self, image, blur_radius):
        """
        Apply Gaussian blur to the image.
        :param image: Input image
        :param blur_radius: Blur radius
        :return: Blurred image
        """
        return cv2.GaussianBlur(image, (0, 0), blur_radius)

    def plan_layer(self, canvas, brush_radius, ref_image, grid_spacing, threshold, mask=None):
        """
        Plan a single layer with strokes based on the reference image, optionally restricted by a mask.
        :param canvas: The current canvas
        :param brush_radius: Radius of the brush for this layer
        :param ref_image: The blurred reference image for this layer
        :param grid_spacing: Spacing of the grid used for stroke placement
        :param threshold: Error threshold for painting strokes
        :param mask: Optional binary mask (same size as the image). If provided, restrict strokes to masked areas.
        """
        height, width = (mask.shape if mask is not None else ref_image.shape[:2])

        # Create a grid of coordinates for faster processing
        grid_x, grid_y = np.meshgrid(np.arange(0, width, grid_spacing),
                                     np.arange(0, height, grid_spacing))
        grid_points = np.vstack((grid_x.ravel(), grid_y.ravel())).T

        # Filter grid points based on the mask, if provided
        if mask is not None:
            grid_points = [point for point in grid_points if mask[point[1], point[0]] > 0]

        # Calculate error and plan strokes for the grid points
        for point in tqdm(grid_points):
            x, y = point

            # Define the neighborhood (centered at the current grid point)
            x_min = max(0, x - grid_spacing // 2)
            x_max = min(width, x + grid_spacing // 2)
            y_min = max(0, y - grid_spacing // 2)
            y_max = min(height, y + grid_spacing // 2)

            # Calculate error for the neighborhood
            region_canvas = canvas[y_min:y_max, x_min:x_max]
            region_ref = ref_image[y_min:y_max, x_min:x_max]
            region_error = np.linalg.norm(region_canvas - region_ref, axis=2)

            # Find the point with the maximum error in the neighborhood
            max_error_idx = np.unravel_index(np.argmax(region_error), region_error.shape)
            max_error_point = (x_min + max_error_idx[1], y_min + max_error_idx[0])

            # If the error exceeds the threshold, paint a stroke
            if region_error[max_error_idx] > threshold:
                self.plan_stroke(canvas, (x, y), max_error_point, brush_radius, ref_image)
                # color = ref_image[y, x]
                # stroke = np.array([point, max_error_point], dtype=np.int32)
                # self.strokes.append((stroke, color, brush_radius))

    def plan_stroke(self, canvas, start_point, second_point, brush_radius, ref_image):
        """
        Plan a curved brush stroke based on minimizing color error.
        :param canvas: Current canvas (result image)
        :param start_point: Starting point of the stroke
        :param second_point: Second point of the stroke (for initial direction)
        :param brush_radius: Radius of the brush
        :param ref_image: Reference blurred image for this layer
        """
        # Initialize stroke
        stroke_color = ref_image[start_point[1], start_point[0]]
        stroke = np.array([start_point, second_point], dtype=np.int32)
        current_point = second_point

        previous_direction = None

        for _ in range(self.max_stroke_length):

            # Compute direction of the next stroke point
            gradient_angle = self.gradient.angle(current_point[1], current_point[0])
            normal_angle = gradient_angle + np.pi / 2

            # Calculate next direction based on brush_radius
            dx = int(np.round(brush_radius * np.cos(normal_angle)))
            dy = int(np.round(brush_radius * np.sin(normal_angle)))

            # If the stroke direction is not continuing properly, adjust
            if previous_direction is not None:
                vi = np.array([dx, dy])
                vi = (0.5 * vi + 0.5 * previous_direction).astype(int)  # Filter stroke direction
                dx, dy = vi[0], vi[1]

            # Compute next point candidate
            candidates = [
                (current_point[0] + dx, current_point[1] + dy),
                (current_point[0] - dx, current_point[1] - dy)
            ]

            best_point = None
            min_error = float('inf')

            # Evaluate color error for both candidate points
            for candidate in candidates:
                if (0 <= candidate[0] < canvas.shape[1] and 0 <= candidate[1] < canvas.shape[0]):
                    next_color = ref_image[candidate[1], candidate[0]]
                    color_error = np.linalg.norm(next_color - stroke_color)

                    if color_error < min_error:  # Minimize error
                        min_error = color_error
                        best_point = candidate

            # If a valid best point is found, move to it
            if best_point is not None and min_error < 60:  # Optional threshold for stopping
                current_point = best_point
                stroke = np.vstack((stroke, best_point))  # Add next point to stroke
                previous_direction = np.array([dx, dy])
            else:
                break

        self.strokes.append((stroke, stroke_color, brush_radius))

    def render_layer(self, canvas):
        """
        Go through the list of strokes and render them on the canvas.
        """
        shuffle(self.strokes)
        for stroke, stroke_color, brush_radius in self.strokes:
            self.brush.apply_spline(canvas, stroke, stroke_color, brush_radius)
        # clear the strokes for the next layer
        self.strokes = []
        self.result = canvas

    def paint(self, mask=None):
        """
        Perform multi-layer painting with progressively smaller brushes.
        Optionally use a mask for the final layer.
        :param mask: Optional binary mask (same size as the image).
                     Non-zero areas indicate where painting should occur in the final layer.
        :return: Painted image
        """
        print("Painting with multiple layers...")
        canvas = np.full_like(self.image, 255, dtype=np.uint8)

        self.compute_gradient(type="luminance")

        for i, brush_radius in enumerate(self.brush_sizes):
            print(f"Painting layer {i + 1} with brush size {brush_radius}...")
            blur_radius = self.blur_factor * brush_radius
            ref_image = self.blur_image(self.image, blur_radius)

            # Plan the layer
            grid_spacing = brush_radius

            if i == len(self.brush_sizes) - 1 and mask is not None:
                self.plan_layer(canvas, brush_radius, ref_image, grid_spacing, threshold=5, mask=mask)
            else:
                self.plan_layer(canvas, brush_radius, ref_image, grid_spacing, threshold=5)

            self.render_layer(canvas)
            self.show_result()

        self.result = canvas
        return canvas
