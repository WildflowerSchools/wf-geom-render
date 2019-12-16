import cv_utils
import numpy as np

class Geom:
    def __init__(
        self,
        coordinates=None,
        color=(0,0,0), # Using BGR for compatibility with opencv
        alpha=1.0 # Range from 0.0 to 1.0
    ):
        if coordinates is not None:
            try:
                coordinates = np.squeeze(np.array(coordinates))
            except:
                raise ValueError('Coordinates must be array-like')
        self.coordinates = coordinates
        self.color = color
        self.alpha = alpha

class Geom2D(Geom):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.coordinates.shape[-1] != 2:
            raise ValueError('For 2D geoms, size of last dimension must be 2')

class Geom3D(Geom):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.coordinates.shape[-1] != 3:
            raise ValueError('For 3D geoms, size of last dimension must be 3')

class Circle(Geom):
    def __init__(
        self,
        radius=1,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.radius = radius

class Line(Geom):
    def __init__(
        self,
        thickness=1,
        line_style='solid',
        **kwargs
    ):
        super().__init__(**kwargs)
        self.thickness = thickness
        self.line_style = line_style

class Text(Geom):
    def __init__(
        self,
        text=None,
        font=None,
        font_size=8,
        horizontal_anchor='center',
        vertical_anchor='middle',
        **kwargs
    ):
        super().__init__(**kwargs)
        self.text=text
        self.font=font
        self.font_size=font_size
        self.horizontal_anchor=horizontal_anchor
        self.vertical_anchor=vertical_anchor

class Circle2D(Geom2D, Circle):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Circle3D(Geom3D, Circle):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Line2D(Geom2D, Line):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Line3D(Geom3D, Line):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Text2D(Geom2D, Text):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Text3D(Geom3D, Text):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
