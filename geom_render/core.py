import cv_utils

class Geom:
    def __init__(
        self,
        color=(0,0,0), #Using BGR for compatibility with opencv
        alpha=1.0 # Range from 0.0 to 1.0
    ):
    self.color = color
    self.alpha = alpha
