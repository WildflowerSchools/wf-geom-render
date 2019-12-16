import cv_utils

class Geom:
    def __init__(
        self,
        color=(0,0,0), #Using BGR for compatibility with opencv
        alpha=1.0 # Range from 0.0 to 1.0
    ):
    self.color = color
    self.alpha = alpha

class Circle(Geom):
    def __init__(
    self,
    radius=1,
    color,
    alpha
    ):
    self.radius = radius
    super().__init__(color, alpha)

class Line(Geom):
    def __init__(
    self,
    thickness=1,
    line_type='solid',
    color,
    alpha
    ):
    self.thickness = thickness
    self.line_type = line_type
    super().__init__(color, alpha)