import numpy as np
import math
import cv2


class Brush:
    def __init__(self, brush_type="circle", texture_image=None):
        self.brush_type = brush_type
        self.texture_image = texture_image

    def apply_spline(self, canvas, control_points, color, radius):
        """
        Draw a cubic spline on the canvas.
        :param canvas: Canvas image
        :param control_points: List of control points for the spline
        :param color: Color of the stroke
        :param radius: Radius of the brush
        """
        for i in range(len(control_points) - 1):
            cv2.line(canvas, control_points[i], control_points[i + 1], color.tolist(), radius)

    def apply(self, res, position, size, color, stroke_scale=1, angle=0, length_first_flag=True):
        brush_methods = {
            "square": self._square,
            "rectangle": self._rectangle,
            "star": self._star,
            "circle": self._circle,
            "ellipse": self._ellipse,
            "line": self._line,
            "texture": self._texture,
        }

        if self.brush_type in brush_methods:
            brush_methods[self.brush_type](res, position, size, color, stroke_scale, angle, length_first_flag)
        else:
            raise ValueError(f"Invalid brush type: {self.brush_type}")

    def _square(self, res, position, size, color, *_):
        x, y = position
        half_size = size // 2
        cv2.rectangle(res, (x - half_size, y - half_size), (x + half_size, y + half_size), color, -1)

    def _rectangle(self, res, position, size, color, stroke_scale, angle, *_):
        box = cv2.boxPoints(((position[0], position[1]), (size, stroke_scale), angle))
        cv2.fillPoly(res, [box.astype(np.int32)], color)

    def _star(self, res, position, size, color, *_):
        x, y = position
        points = []
        for i in range(5):
            angle = i * 72  # 360 / 5 points for a star
            dx = int(size * math.cos(math.radians(angle)))
            dy = int(size * math.sin(math.radians(angle)))
            points.append((x + dx, y + dy))
        points = np.array(points, np.int32)
        cv2.fillPoly(res, [points], color)

    def _circle(self, res, position, size, color, *_):
        cv2.circle(res, position, size, color, -1, cv2.LINE_AA)

    def _ellipse(self, res, position, size, color, stroke_scale, angle, *_):
        cv2.ellipse(res, position, (size, stroke_scale), angle, 0, 360, color, -1, cv2.LINE_AA)

    def _line(self, res, position, size, color, stroke_scale, angle, length_first_flag):
        x, y = position

        if length_first_flag:
            start_point = (int(x + size * math.cos(math.radians(angle))), int(y + size * math.sin(math.radians(angle))))
            end_point = (int(x - size * math.cos(math.radians(angle))), int(y - size * math.sin(math.radians(angle))))
        else:
            start_point = (
                int(x + stroke_scale * math.cos(math.radians(angle))),
                int(y + stroke_scale * math.sin(math.radians(angle))),
            )
            end_point = (
                int(x - stroke_scale * math.cos(math.radians(angle))),
                int(y - stroke_scale * math.sin(math.radians(angle))),
            )

        cv2.line(res, start_point, end_point, color, stroke_scale, cv2.LINE_AA)

    def _texture(self, res, position, size, color, *_):
        if self.texture_image is None:
            raise ValueError("Texture image not provided for texture brush.")

        x, y = position
        half_size = size // 2
        texture = cv2.resize(self.texture_image, (size, size))
        roi = res[y - half_size: y + half_size, x - half_size: x + half_size]

        if roi.shape == texture.shape:
            np.copyto(roi, texture)


if __name__ == "__main__":
    # use brushes on the canvas
    canvas = np.zeros((512, 512, 3), np.uint8)

    # split into 6 different spaces on the canva
    positions = [(128, 128), (384, 128), (128, 384), (384, 384), (256, 128), (256, 384)]

    brush1 = Brush(brush_type="circle")
    brush1.apply(canvas, positions[0], 50, (255, 0, 0))

    brush2 = Brush(brush_type="rectangle")
    brush2.apply(canvas, positions[1], 50, (0, 255, 0), 10, 45)

    brush3 = Brush(brush_type="star")
    brush3.apply(canvas, positions[2], 50, (0, 0, 255))

    brush4 = Brush(brush_type="ellipse")
    brush4.apply(canvas, positions[3], 50, (255, 255, 0), 10, 45)

    brush5 = Brush(brush_type="line")
    brush5.apply(canvas, positions[4], 50, (255, 0, 255), 10, 45, True)

    brush6 = Brush(brush_type="line")
    brush6.apply(canvas, positions[5], 50, (0, 255, 255), 10, 45, False)

    # show
    cv2.imshow("Canvas", canvas)
    cv2.waitKey(0)
