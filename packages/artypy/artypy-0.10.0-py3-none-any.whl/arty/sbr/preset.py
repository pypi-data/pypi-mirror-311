import os

# TODO: Add loading and saving functions
# TODO: Handle paths appropriately

class Preset:
    def __init__(self, palette_size=10, stroke_scale=0, length_scale=1 / 3, gradient_smoothing_radius=0,
                 brush_type="circle", length_type="base", length_first_flag=True, gradient_type="sharr",
                 gradient_smoothing_type="gaussian", smoothing_iterations=1, grid_scale=3, grayscale=False,
                 has_cardboard=False, layer_scales = [1, 0.5, 0.25], error_threshold = 60, blur_factor = 1.0):
        """
        Initialize the preset object for the style-based rendering that will be used in the image painter.
        :param palette_size: the size of the palette, default is 10
        :param stroke_scale: the scale of the stroke, default is 0
        :param length_scale: the scale of the length, default is 1/3
        :param gradient_smoothing_radius: the radius of the gradient smoothing, default is 0
        :param brush_type: the type of the brush, default is "circle", other options are "square", "rectangle", "star", "ellipse", "line", "texture"
        :param length_type: the type of the length, default is "base", other option is "inverse". It defines dependency of the length on the gradient.
        :param length_first_flag: the flag for the length, default is True
        :param gradient_type: the type of the gradient, default is "sharr", other option is "sobel"
        :param gradient_smoothing_type: the type of the gradient smoothing, default is "gaussian", other options are "bilateral", "none"
        :param smoothing_iterations: the number of smoothing iterations, default is 1
        :param grid_scale: the scale of the grid, default is 3
        :param grayscale: the flag for the grayscale, default is False
        :param has_cardboard: the flag for the cardboard, default is False
        """
        self.palette_size = palette_size
        self.stroke_scale = stroke_scale
        self.gradient_smoothing_radius = gradient_smoothing_radius
        self.brush_type = brush_type
        self.length_type = length_type
        self.length_first_flag = length_first_flag
        file_names = [int(file_name.split(".")[0]) for file_name in os.listdir(f"sbr/{str(self.brush_type)}")]

        if len(file_names) == 0:
            file_names = [-1]

        self.img_save_path = os.path.join(f"sbr/{str(self.brush_type)}/{str(max(file_names) + 1)}.jpg")
        self.preset_save_path = f"../configs/presets/sbr/{str(self.brush_type)}/{str(max(file_names) + 1)}.yaml"
        self.length_scale = length_scale
        self.gradient_type = gradient_type
        self.gradient_smoothing_type = gradient_smoothing_type
        self.smoothing_iterations = smoothing_iterations
        self.grid_scale = grid_scale
        self.grayscale = grayscale
        self.has_cardboard = has_cardboard
        self.layer_scales = layer_scales
        self.error_threshold = error_threshold
        self.blur_factor = blur_factor