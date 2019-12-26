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
                raise ValueError('Coordinates for geom must be array-like')
            if coordinates.ndim > 3:
                raise ValueError('Coordinates for geom must be of dimension 3 or less')
            while coordinates.ndim < 3:
                coordinates = np.expand_dims(coordinates, axis=0)
        if time_index is not None:
            try:
                time_index = np.array(time_index)
            except:
                raise ValueError('Time index must be array-like')
            if time_index.ndim != 1:
                raise ValueError('Time index must be one-dimensional')
            num_time_slices = time_index.shape[0]
            time_index_sort_order = np.argsort(time_index)
            time_index = time_index[time_index_sort_order]
            if coordinates is not None:
                if coordinates.shape[0] != num_time_slices:
                    raise ValueError('First dimension of coordinates array must be of same length as time index')
                coordinates = coordinates.take(time_index_sort_order, axis=0)
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

    @classmethod
    def from_geom_list(cls, geom_list):
        num_points = 0
        num_spatial_dimensions = geom_list[0].coordinates.shape[-1]
        for geom in geom_list:
            if geom.coordinates.shape[0] != 1:
                raise ValueError('All geoms in list must be for a single time slice')
            if geom.coordinates.shape[-1] != num_spatial_dimensions:
                raise ValueError('All geoms in list must have the same number of spatial_dimensions')
            num_points += geom.coordinates.shape[1]
        new_coordinates = np.full((1, num_points, num_spatial_dimensions), np.nan)
        new_geom_list = list()
        coordinate_index = 0
        for geom in geom_list:
            coordinate_indices = list()
            for point_index in range(geom.coordinates.shape[1]):
                new_coordinates[0, coordinate_index] = geom.coordinates[0, point_index]
                coordinate_indices.append(coordinate_index)
                coordinate_index += 1
            new_geom = copy.deepcopy(geom)
            new_geom.coordinates = None,
            new_geom.coordinate_indices = coordinate_indices
            new_geom_list.append(new_geom)
        return cls(
            coordinates=new_coordinates,
            geom_list=new_geom_list
        )

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

class Point(Geom):
    def __init__(
        self,
        marker=None,
        size=None,
        line_width=None,
        line_color=None,
        fill_color=None,
        alpha=1.0,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.marker = marker
        self.size = size
        self.line_width=line_width
        self.line_color=line_color
        self.fill_color=fill_color
        self.alpha=alpha

class Line(Geom):
    def __init__(
        self,
        line_width=1,
        line_style='solid',
        color='#ffff00',
        alpha=1.0,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.line_width = line_width
        self.line_style = line_style
        self.color=color
        self.alpha=alpha

class Text(Geom):
    def __init__(
        self,
        text=None,
        font_family=None,
        font_style=None,
        font_weight=None,
        font_size=None,
        text_color='#000000',
        text_alpha=1.0,
        horizontal_alignment='center',
        vertical_alignment='bottom',
        box=False,
        box_line_color='#000000',
        box_fill=False,
        box_fill_color='#ffff00',
        box_alpha=1.0,
        box_line_width=1.0,
        box_line_style=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.text = text
        self.font_family = font_family
        self.font_style = font_style
        self.font_weight = font_weight
        self.font_size = font_size
        self.text_color = text_color
        self.text_alpha = text_alpha
        self.horizontal_alignment = horizontal_alignment
        self.vertical_alignment = vertical_alignment
        self.box = box
        self.box_line_color = box_line_color
        self.box_fill = box_fill
        self.box_fill_color = box_fill_color
        self.box_alpha = box_alpha
        self.box_line_width = box_line_width
        self.box_line_style = box_line_style

class GeomCollection2D(Geom2D, GeomCollection):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def draw_matplotlib(self, axis):
        for geom_index, geom in enumerate(self.geom_list):
            geom_copy = copy.deepcopy(geom)
            geom_copy.coordinates = self.coordinates.take(geom_copy.coordinate_indices, 1)
            geom_copy.draw_matplotlib(axis)

class GeomCollection3D(Geom3D, GeomCollection):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Circle2D(Geom2D, Circle):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def draw_matplotlib(self, axis):
        if self.coordinates.shape != (1, 1, 2):
            raise ValueError('Draw method for Circle2D requires coordinates to be of shape (1, 1, 2)')
        axis.add_artist(plt.Circle(
            xy=self.coordinates[0, 0, :],
            radius=self.radius,
            fill=self.fill,
            edgecolor=self.line_color,
            facecolor=self.fill_color,
            alpha=self.alpha
        ))

class Circle3D(Geom3D, Circle):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Point2D(Geom2D, Point):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def draw_matplotlib(self, axis):
        if self.coordinates.shape != (1, 1, 2):
            raise ValueError('Draw method for Point2D requires coordinates to be of shape (1, 1, 2)')
        s = None
        if self.size is not None:
            s=self.size**2
        axis.scatter(
            self.coordinates[0, 0, 0],
            self.coordinates[0, 0, 1],
            marker=self.marker,
            s=s,
            linewidths=self.line_width,
            edgecolors=self.line_color,
            color=self.fill_color,
            alpha=self.alpha,
        )

class Point3D(Geom3D, Point):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Line2D(Geom2D, Line):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def draw_matplotlib(self, axis):
        if self.coordinates.shape != (1, 2, 2):
            raise ValueError('Draw method for Line2D requires coordinates to be of shape (1, 2, 2)')
        axis.add_artist(plt.Line2D(
            (self.coordinates[0, 0, 0], self.coordinates[0, 1,0]),
            (self.coordinates[0, 0, 1], self.coordinates[0, 1, 1]),
            linewidth=self.line_width,
            linestyle=self.line_style,
            color=self.color,
            alpha=self.alpha,
        ))

class Line3D(Geom3D, Line):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Text2D(Geom2D, Text):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def draw_matplotlib(self, axis):
        if self.coordinates.shape != (1, 1, 2):
            raise ValueError('Draw method for Text2D requires coordinates to be of shape (1, 1, 2)')
        bbox = None
        if self.box:
            bbox = {
                'edgecolor': self.box_line_color,
                'fill': self.box_fill,
                'facecolor': self.box_fill_color,
                'alpha': self.box_alpha,
                'linewidth': self.box_line_width,
                'linestyle': self.box_line_style
            }
        axis.text(
            self.coordinates[0, 0, 0],
            self.coordinates[0, 0, 1],
            self.text,
            fontfamily=self.font_family,
            fontstyle=self.font_style,
            fontweight=self.font_weight,
            fontsize=self.font_size,
            color=self.text_color,
            alpha=self.text_alpha,
            horizontalalignment=self.horizontal_alignment,
            verticalalignment=self.vertical_alignment,
            bbox=bbox
        )

class Text3D(Geom3D, Text):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
