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

from space.line import Line
from space.node import Node
from space.subsector import Subsector
from space.vectors import Vec2d


def get_tree():
    normal_vector_simple_north = Vec2d(0, -1)
    normal_vector_simple_south = Vec2d(0, 1)
    normal_vector_simple_west = Vec2d(-1, 0)
    normal_vector_simple_east = Vec2d(1, 0)

    point_1_a = Vec2d(10, 10)
    point_1_b = Vec2d(200, 10)
    point_1_c = Vec2d(200, 100)
    point_1_d_portal = Vec2d(150, 200)  # P !!!
    point_1_e_portal = Vec2d(100, 250)  # P !!!
    point_1_f = Vec2d(10, 200)

    point_2_a = Vec2d(300, 300)
    # P #P
    point_2_b = Vec2d(10, 300)
    point_2_c = Vec2d(50, 500)
    point_2_d = Vec2d(250, 600)
    point_2_e = Vec2d(300, 450)

    # north polygon
    line_1_a = Line(point_1_a, point_1_b, normal_vector_simple_south)  # 1st  4-5
    line_1_b = Line(point_1_b, point_1_c, normal_vector_simple_west)  # 2nd  4-8
    line_1_c = Line(point_1_c, point_1_d_portal, normal_vector_simple_north)  # 3rd  0-8
    line_1_d = Line(point_1_d_portal, point_1_e_portal, normal_vector_simple_north)  # 4th  0-11 PORTAL
    line_1_e = Line(point_1_e_portal, point_1_f, normal_vector_simple_east)  # 4th  0-11
    line_1_f = Line(point_1_f, point_1_a, normal_vector_simple_east)  # 4th  0-11

    # south polygon
    line_2_a = Line(point_2_a, point_1_d_portal, normal_vector_simple_east)  # 4th  0-11
    # line_2_b = Line(point_1_d_portal, point_1_e_portal, normal_vector_simple_east)  # 4th  0-11
    # line_1_d !!!!
    line_2_c = Line(point_1_e_portal, point_2_b, normal_vector_simple_east)  # 4th  0-11
    line_2_d = Line(point_2_b, point_2_c, normal_vector_simple_east)  # 4th  0-11
    line_2_e = Line(point_2_c, point_2_d, normal_vector_simple_east)  # 4th  0-11
    line_2_f = Line(point_2_d, point_2_e, normal_vector_simple_east)  # 4th  0-11
    line_2_g = Line(point_2_e, point_2_a, normal_vector_simple_east)  # 4th  0-11

    subsector_1 = Subsector([line_1_a, line_1_b, line_1_c, line_1_d, line_1_e, line_1_f, line_1_a])
    subsector_2 = Subsector([line_2_a, line_1_d, line_2_c, line_2_d, line_2_e, line_2_f, line_2_g])
    node = Node(line_1_d, subsector_1, subsector_2)
    return node


def travers_binary_tree(p1, z_buffer, line_list):
    """
    Not used yet.
    TODO: Hardcoded POC
    """
    y = p1.line.height
    x_start = p1.line.first.x
    x_end = p1.line.second.x
    y_start = p1.line.first.y
    y_end = p1.line.second.y
    # make sure the line is drawable
    if x_start > x_end:
        x_start, x_end = x_end, x_start
        y_start, y_end = y_end, y_start

    # travers closer first
    if p1.left:
        travers_binary_tree(p1.left, z_buffer, line_list)
    # travers farther later
    if p1.right:
        travers_binary_tree(p1.right, z_buffer, line_list)

    for x in range(x_start, x_end):
        y_cor = y_start + (y_end - y_start) / (x_end - x_start) * x
        distance_from_camera = math.sqrt(math.pow(x - cam_x, 2) + math.pow(y_cor - cam_y, 2))
        if x not in z_buffer:
            z_buffer[x] = [distance_from_camera]
        else:
            z_buffer[x].append(distance_from_camera)
        line_list.append((p1.line.first, p1.line.second))

    return z_buffer, line_list
