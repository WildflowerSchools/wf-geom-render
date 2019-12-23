import cv_utils
import numpy as np

class Geom:
    def __init__(
        self,
        coordinates=None,
        coordinate_indices=None,
        time_index=None
    ):
        if coordinates is not None:
            try:
                coordinates = np.array(coordinates)
            except:
                raise ValueError('Coordinates must be array-like')
        if time_index is not None:
            try:
                time_index = np.array(time_index)
            except:
                raise ValueError('Time index must be array-like')
            time_index_sort_order = np.argsort(time_index)
            time_index = time_index[time_index_sort_order]
            if coordinates is not None:
                if coordinates.shape[0] != time_index.shape[0]:
                    raise ValueError('First dimension of coordinates array must be of same length as time index')
                coordinates = coordinates[time_index_sort_order]
        self.coordinates = coordinates
        self.coordinate_indices = coordinate_indices
        self.time_index = time_index


class Geom2D(Geom):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.coordinates is not None and self.coordinates.shape[-1] != 2:
            raise ValueError('For 2D geoms, size of last dimension must be 2')

class Geom3D(Geom):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.coordinates is not None and self.coordinates.shape[-1] != 3:
            raise ValueError('For 3D geoms, size of last dimension must be 3')

class GeomCollection(Geom):
    def __init__(
        self,
        geom_list=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.geom_list = geom_list

class Circle(Geom):
    def __init__(
        self,
        radius=1,
        line_color='#ffff00',
        line_alpha=1.0,
        fill_color='#ffff00',
        fill_alpha=0.0,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.radius = radius
        self.line_color=line_color
        self.line_alpha=line_alpha
        self.fill_color=fill_color
        self.fill_alpha=fill_alpha

class Line(Geom):
    def __init__(
        self,
        thickness=1,
        line_style='solid',
        color='#ffff00',
        alpha=1.0,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.thickness = thickness
        self.line_style = line_style
        self.color=color
        self.alpha=alpha

class Text(Geom):
    def __init__(
        self,
        text=None,
        font=None,
        font_size=8,
        horizontal_anchor='center',
        vertical_anchor='middle',
        text_color='#ffff00',
        text_alpha=1.0,
        background_color='#ffff00',
        background_alpha=0.0,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.text=text
        self.font=font
        self.font_size=font_size
        self.horizontal_anchor=horizontal_anchor
        self.vertical_anchor=vertical_anchor
        self.text_color=text_color
        self.text_alpha=text_alpha
        self.background_color=background_color
        self.background_alpha=background_alpha

class GeomCollection2D(Geom2D, GeomCollection):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class GeomCollection3D(Geom3D, GeomCollection):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
