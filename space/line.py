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
from space.vectors import Vec2d


class Line:
    """
        normal vector (visible side)
             ^
             |
             |
    First--------Second
    """

    def __init__(self, first, second, normal):
        self.first = first  # type: Vec2d
        self.second = second  # type: Vec2d
        self.normal = normal  # type: Vec2d
        self.formula_m, self.formula_b = self.get_line_formula()

    def is_point_under(self, point):
        point_x = point.x
        point_y = point.y
        line_y = self.formula_m * point_x + self.formula_b
        if line_y < point_y:
            return False
        return True

    def get_line_formula(self):
        # y=mx+b
        x1 = self.first.x
        y1 = self.first.y
        x2 = self.second.x
        y2 = self.second.y
        delta_x = x1 - x2
        delta_y = y1 - y2
        if delta_x != 0:
            m = delta_y / delta_x
        else:
            m = 0
        #y = m*x + b
        b = y1 - m*x1  # calculate b from one point
        return m, b





