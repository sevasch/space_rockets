from vector import Vector

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