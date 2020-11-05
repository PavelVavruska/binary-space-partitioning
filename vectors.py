#  Copyright (c) 2020 Pavel Vavruska
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
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