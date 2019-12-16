import cv_utils
import numpy as np

class Geom:
    def __init__(
        self,
        color=(0,0,0), # Using BGR for compatibility with opencv
        alpha=1.0 # Range from 0.0 to 1.0
    ):
        self.color = color
        self.alpha = alpha

class Circle(Geom):
    def __init__(
    self,
    radius=1,
    *args,
    **kwargs
    ):
        self.radius = radius
        super().__init__(*args, **kwargs)

class Circle2D(Circle):
    def __init__(
    self,
    coordinates,
    *args,
    **kwargs
    ):
        try:
            coordinates = np.array(coordinates)
        except:
            raise ValueError('Coordinates must be array-like')
        if coordinates.shape != (2,):
            raise ValueError('Coordinates must be of shape (2,)')
        self.coordinates = coordinates
        super().__init__(*args, **kwargs)

class Circle3D(Circle):
    def __init__(
    self,
    coordinates,
    *args,
    **kwargs
    ):
        try:
            coordinates = np.array(coordinates)
        except:
            raise ValueError('Coordinates must be array-like')
        if coordinates.shape != (2,):
            raise ValueError('Coordinates must be of shape (3,)')
        self.coordinates = coordinates
        super().__init__(*args, **kwargs)

class Line(Geom):
    def __init__(
    self,
    thickness=1,
    line_type='solid',
    *args,
    **kwargs
    ):
        self.thickness = thickness
        self.line_type = line_type
        super().__init__(*args, **kwargs)

class Line2D(Geom):
    def __init__(
    self,
    coordinates,
    *args,
    **kwargs):
        try:
            coordinates = np.array(coordinates)
        except:
            raise ValueError('Coordinates must be array-like')
        if coordinates.shape != (2,2):
            raise ValueError('Coordinates must be of shape (2,2)')
        super().__init__(*args, **kwargs)

class Line3D(Geom):
    def __init__(
    self,
    coordinates,
    *args,
    **kwargs):
        try:
            coordinates = np.array(coordinates)
        except:
            raise ValueError('Coordinates must be array-like')
        if coordinates.shape != (2,3):
            raise ValueError('Coordinates must be of shape (2,3)')
        super().__init__(*args, **kwargs)

class Text(Geom):
    def __init__(
    self,
    text,
    font=None,
    font_size=8,
    horizontal_anchor='center',
    vertical_anchor='middle',
    *args,
    **kwargs
    ):
        self.text=text
        self.font=font
        self.font_size=font_size
        self.horizontal_anchor=horizontal_anchor
        self.vertical_anchor=vertical_anchor
        super().__init__(*args, **kwargs)

class Text2D(Geom):
    def __init__(
    self,
    coordinates,
    *args,
    **kwargs
    ):
        try:
            coordinates = np.array(coordinates)
        except:
            raise ValueError('Coordinates must be array-like')
        if coordinates.shape != (2,2):
            raise ValueError('Coordinates must be of shape (2,)')
        self.coordinates = coordinates
        super().__init__(*args, **kwargs)

class Text3D(Geom):
    def __init__(
    self,
    coordinates,
    *args,
    **kwargs
    ):
        try:
            coordinates = np.array(coordinates)
        except:
            raise ValueError('Coordinates must be array-like')
        if coordinates.shape != (2,2):
            raise ValueError('Coordinates must be of shape (3,)')
        self.coordinates = coordinates
        super().__init__(*args, **kwargs)
