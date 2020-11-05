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
from enum import Enum


class RenderType(Enum):
    LINE = 1
    POLY = 2


def render_polygon(render_type, canvas, point_list, fill_color, outline_color):
    if render_type == RenderType.LINE:
        canvas.create_line(
            *point_list[0:4],
            fill=fill_color)
        # bottom
        canvas.create_line(
            *point_list[2:6],
            fill=fill_color)
        # left
        canvas.create_line(
            *point_list[4:8],
            fill=fill_color)
        # right
        canvas.create_line(
            *point_list[6:8],
            *point_list[0:2],
            fill=fill_color)
    if render_type == RenderType.POLY:
        canvas.create_polygon(point_list, outline=outline_color, fill=fill_color, width=1)


def calculate_x_y_line_for_x(diff_rot_2_y, diff_rot_1_y, diff_rot_2_x, diff_rot_1_x, x):
    m = 0
    if diff_rot_2_x - diff_rot_1_x != 0:
        m = (diff_rot_2_y - diff_rot_1_y) / (diff_rot_2_x - diff_rot_1_x)  # slope equation
    b = diff_rot_2_y - m * diff_rot_2_x  # compute B: y = m*x+b
    return x, m * x + b  # x, y for x