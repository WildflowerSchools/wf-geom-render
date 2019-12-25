import cv_utils
import numpy as np
import copy
import matplotlib.pyplot as plt

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
            if time_index.ndim != 1:
                raise ValueError('Time index must be one-dimensional')
            time_index_sort_order = np.argsort(time_index)
            time_index = time_index[time_index_sort_order]
            if coordinates is not None:
                if coordinates.shape[0] != time_index.shape[0]:
                    raise ValueError('First dimension of coordinates array must be of same length as time index')
                coordinates = coordinates[time_index_sort_order]
        self.coordinates = coordinates
        self.coordinate_indices = coordinate_indices
        self.time_index = time_index

    def resample(
        self,
        new_time_index,
        method='interpolate'
    ):
        if method not in ['interpolate', 'fill']:
            raise ValueError('Available resampling methods are \'interpolate\' and \'fill\'')
        try:
            new_time_index = np.array(new_time_index)
        except:
            raise ValueError('New time index must be array-like')
        if new_time_index.ndim != 1:
            raise ValueError('New time index must be one-dimensional')
        new_time_index.sort()
        num_new_time_slices = new_time_index.shape[0]
        coordinates_time_slice_shape = self.coordinates.shape[1:]
        new_coordinates_shape = (num_new_time_slices,) + coordinates_time_slice_shape
        new_coordinates = np.full(new_coordinates_shape, np.nan)
        old_time_index_pointer = 0
        for new_time_index_pointer in range(num_new_time_slices):
            if new_time_index[new_time_index_pointer] < self.time_index[old_time_index_pointer]:
                continue
            if new_time_index[new_time_index_pointer] > self.time_index[-1]:
                break
            while new_time_index[new_time_index_pointer] > self.time_index[old_time_index_pointer + 1]:
                old_time_index_pointer += 1
            if method == 'interpolate':
                later_slice_weight = (
                    (new_time_index[new_time_index_pointer] - self.time_index[old_time_index_pointer])/
                    (self.time_index[old_time_index_pointer + 1] - self.time_index[old_time_index_pointer])
                )
                earlier_slice_weight = 1.0 - later_slice_weight
            else:
                earlier_slice_weight = 1.0
                later_slice_weight = 0.0
            new_coordinates[new_time_index_pointer] = (
                earlier_slice_weight*self.coordinates[old_time_index_pointer] +
                later_slice_weight*self.coordinates[old_time_index_pointer + 1]
            )
        new_geom = copy.deepcopy(self)
        new_geom.time_index = new_time_index
        new_geom.coordinates = new_coordinates
        return new_geom




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
        fill=True,
        line_color='#ffff00',
        fill_color='#ffff00',
        alpha=0.0,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.radius = radius
        self.fill = fill
        self.line_color=line_color
        self.fill_color=fill_color
        self.alpha=alpha

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

    def draw_matplotlib(self, axis):
        axis.add_artist(plt.Circle(
            xy=self.coordinates,
            radius=self.radius,
            fill=self.fill,
            edgecolor=self.line_color,
            facecolor=self.fill_color,
            alpha=self.alpha
        ))

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
