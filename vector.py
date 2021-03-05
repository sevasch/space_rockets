import numpy as np

class Vector():
    def __init__(self, x=0, y=0):
        self.data = np.array((x, y), dtype=float)

    @classmethod
    def from_polar(cls, length, angle):
        vec_x = -length * np.sin(angle)
        vec_y = length * np.cos(angle)
        return cls(vec_x, vec_y)

    def rotate(self, angle):
        R = np.array(((np.cos(angle), -np.sin(angle)),
                      (np.sin(angle), np.cos(angle))))
        new_vec = R.dot(self.data)
        return Vector(new_vec[0], new_vec[1])

    def dot(self, other):
        return self.data[0] * other.data[0] + self.data[1] * other.data[1]

    def get_angle(self):
        return np.arctan2(self.data[1], self.data[0])

    def norm(self):
        return np.sqrt(self.data[0]**2 + self.data[1]**2)

    def unit_length(self):
        return self / max(self.norm(), 1e-3)

    def get(self):
        return (self.data[0], self.data[1])

    def __getitem__(self, key):
        return self.data[key]

    def __str__(self):
        return str(self.data)

    def __neg__(self):
        return Vector(-self.data[0], -self.data[1])

    def __add__(self, other):
        data_new = self.data + other.data
        return Vector(data_new[0], data_new[1])

    def __sub__(self, other):
        data_new = self.data - other.data
        return Vector(data_new[0], data_new[1])

    def __mul__(self, other: float):
        return Vector(self.data[0] * other, self.data[1] * other)

    def __truediv__(self, other: float):
        return Vector(self.data[0] / other, self.data[1] / other)


if __name__ == '__main__':
    v1 = Vector(1, 2)
    v2 = Vector(1, 1)
    print(v1.dot(v2))