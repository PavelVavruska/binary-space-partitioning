import math


class Vec2d:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add_vec2d_xy(self, x, y):
        self.x += x
        self.y += y

    def add_vec2d(self, vec2d):
        self.x += vec2d.x
        self.y += vec2d.y

    def get_length(self):
        x = self.x
        y = self.y

        return math.sqrt(x*x + y*y)

    def normalize(self):
        length = self.get_length()
        if length == 0:
            return Vec2d(0, 0)
        x = self.x / abs(length)
        y = self.y / abs(length)
        return Vec2d(x, y)

    def multiply_by_factor(self, factor):
        self.x *= factor
        self.y *= factor

    def dot_product_with(self, vec_1):
        return self.x * vec_1.x + self.y * vec_1.y

    @staticmethod
    def dot_product_between(vec_1, vec_2):
        return vec_1.x * vec_2.x + vec_1.y * vec_2.y