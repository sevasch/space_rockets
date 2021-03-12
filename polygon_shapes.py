from vector import Vector
import numpy as np
import pygame

class PolygonShape():
    def __init__(self, points: np.array):
        assert points.shape[0] == 3
        self.points = points

    def transform(self, transformation_matrix: np.array):
        assert transformation_matrix.shape == (3, 3)
        return PolygonShape(transformation_matrix.dot(self.points))

    def scale(self, factor):
        t = factor * np.eye(3)
        t [2, 2] = 1
        return self.transform(t)

    def translate(self, translation: Vector):
        t = np.eye(3)
        t[0, 2] = translation.data[0]
        t[1, 2] = translation.data[1]
        return self.transform(t)

    def rotate(self, angle):
        t = np.eye(3)
        t[:2, :2] = np.array(((np.cos(angle), -np.sin(angle)),
                              (np.sin(angle), np.cos(angle))))
        return self.transform(t)

    def to_simulator(self, simulator):
        return self.translate(-simulator.camera_center)\
            .scale(simulator.scale)\
            .translate(Vector(simulator.window_size[0], simulator.window_size[1]) / 2)\
            .get_pairs()

    def get(self):
        return self.points

    def get_pairs(self):
        return [(self.points[0, i], self.points[1, i]) for i in range(self.points.shape[1])]

    def __str__(self):
        return str(self.points)


def scale_polygon(polygon_shape, scale_factor):
    return [pt * scale_factor for pt in polygon_shape]

def translate_polygon(polygon_shape, vector: Vector):
    return [pt + vector for pt in polygon_shape]

def rotate_polygon(polygon_shape, angle):
    return [pt.rotate(angle) for pt in polygon_shape]

def make_pairs(polygon_shape):
    return [(v[0], v[1]) for v in polygon_shape]

def get_arrow(length=1, ratio=0.05):
    width = length * ratio
    return [Vector(0, width / 2 ),
            Vector(length, width / 2 ),
            Vector(length, width ),
            Vector((length + width), 0),
            Vector(length, - width ),
            Vector(length, - width / 2 ),
            Vector(0, - width / 2 )]

if '__main__' == __name__:
    x = np.ones((3, 5))
    x[:2, :] = np.random.rand(2, 5)
    print(x)
    p = PolygonShape(x)
    t = np.eye(3)
    # p.scale(0.5)
    # p.translate(Vector(-1, 2))
    print(p.rotate(np.pi).get_pairs())
