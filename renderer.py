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