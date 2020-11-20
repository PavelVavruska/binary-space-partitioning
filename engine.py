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
import time
import tkinter

from space import bsp
from player import Player
from renderer import render_polygon, RenderType, calculate_x_y_line_for_x
from space.vectors import Vec2d

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 650
ENGINE_PIXEL_SIZE = 5
PIXEL_SIZE = 10
NUMBER_OF_HORIZONTAL_BIG_PIXELS = WINDOW_WIDTH / ENGINE_PIXEL_SIZE

MICROSECONDS_IN_SECOND = 1_000_000
NANOSECONDS_IN_SECOND = 1_000_000_000

COLOR_WHITE = '#FFFFFF'
COLOR_BLACK = '#000000'
COLOR_CYAN = '#0000FF'
COLOR_GREEN = '#00FF00'
COLOR_RED = '#FF0000'

# tkinter init

tk = tkinter.Tk()
frame = tkinter.Frame(tk, width=100, height=100)
msgL1 = tkinter.StringVar()
msgL1.set('Keyboard')
msgL2 = tkinter.StringVar()
msgL2.set('Player')
msgL3 = tkinter.StringVar()
msgL3.set('Frametimes')
msgL4 = tkinter.StringVar()
msgL4.set('Player - additional')
label = tkinter.Label(frame, textvariable=msgL1)
label.pack()
label = tkinter.Label(frame, textvariable=msgL2)
label.pack()
label = tkinter.Label(frame, textvariable=msgL3)
label.pack()
label = tkinter.Label(frame, textvariable=msgL4)
label.pack()
frame.pack()

# tStart = 0
# tEnd = int(round(time.time() * 1_000_000))  # μs
xCor = WINDOW_WIDTH // 2
yCor = WINDOW_HEIGHT // 2
canvas_abs = tkinter.Canvas(tk, width=WINDOW_WIDTH / 3, height=WINDOW_HEIGHT, bg=COLOR_BLACK)

canvas_trans = tkinter.Canvas(tk, width=WINDOW_WIDTH / 3, height=WINDOW_HEIGHT, bg="#222222")

canvas_3d = tkinter.Canvas(tk, width=WINDOW_WIDTH / 3, height=WINDOW_HEIGHT, bg=COLOR_BLACK)
canvas_3d_2 = tkinter.Canvas(tk, width=WINDOW_WIDTH / 3, height=WINDOW_HEIGHT, bg="#222222")

canvas_abs.pack(side=tkinter.LEFT)
canvas_trans.pack(side=tkinter.LEFT)
canvas_3d.pack(side=tkinter.LEFT)
canvas_3d_2.pack(side=tkinter.LEFT)


# init entities

def process_mouse_motion(event):
    player.set_aim_x(event.x)
    player.set_aim_y(event.y)


def process_mouse_click(event):
    if event.type == tkinter.EventType.ButtonPress:
        player.start_fire()
    elif event.type == tkinter.EventType.ButtonRelease:
        player.end_fire()


class Keyboard():
    __keys = set()

    @property
    def keys(self):
        return self.__keys

    @classmethod
    def key_press_handler(cls, event):
        cls.__keys.add(event.keycode)

    @classmethod
    def key_release_handler(cls, event):
        if event.keycode:
            cls.__keys.remove(event.keycode)


keyboard = Keyboard()

frame.bind_all('<KeyPress>', keyboard.key_press_handler)
frame.bind_all('<KeyRelease>', keyboard.key_release_handler)
tk.bind('<Motion>', process_mouse_motion)
tk.bind("<Button-1>", process_mouse_click)
tk.bind("<ButtonRelease>", process_mouse_click)

player = Player(30.0, 30.0, 90)

isAlive = True
time_render_end = time.time()

tree = bsp.get_tree()


def render_sector(subsector, portal_line, portal=None):
    for line in subsector.get_line_iterator():  # type: line.Line
        diff_1_x = line.first.x - player.x
        diff_2_x = line.second.x - player.x
        diff_1_y = line.first.y - player.y
        diff_2_y = line.second.y - player.y
        if line == portal_line:
            fill_color = "#FF0000"
        else:
            fill_color = "#FFFFFF"
        canvas_abs.create_line(line.first.x, line.first.y, line.second.x,
                               line.second.y, fill=fill_color)

    # minimap absolute map
    canvas_abs.create_oval(player_pixel_x,
                           player_pixel_y,
                           player_pixel_x + 10,
                           player_pixel_y + 10, fill="#999999")

    canvas_abs.create_line(player_pixel_x + 5,
                           player_pixel_y + 5,
                           player_pixel_x + 5 + player_aiming_vec2d.x * 10,
                           player_pixel_y + 5 + player_aiming_vec2d.y * 10, fill="#FFFFFF")

    canvas_abs.create_line(player_pixel_x + 5,
                           player_pixel_y + 5,
                           player_pixel_x + 5 + vec2d_forward.x * 50,
                           player_pixel_y + 5 + vec2d_forward.y * 50, fill="#00FF00")

    canvas_abs.create_line(player_pixel_x + 5,
                           player_pixel_y + 5,
                           player_pixel_x + 5 + vec2d_sideways.x * 50,
                           player_pixel_y + 5 + vec2d_sideways.y * 50, fill="#FF0000")

    canvas_abs.create_line(player_pixel_x + 5,
                           player_pixel_y + 5,
                           player_pixel_x + 5 + vec2d_combined.x * 50,
                           player_pixel_y + 5 + vec2d_combined.y * 50, fill="#FF00FF")

    # draw frustrum
    canvas_abs.create_line(player_pixel_x + 5,
                           player_pixel_y + 5,
                           player_pixel_x + 5 + player_aiming_vec2d.x * 10,
                           player_pixel_y + 5 + player_aiming_vec2d.y * 10, fill="#FFFFFF")

    for projectile in player.projectiles:  # type: projectile
        if projectile.position_vec2d.x < 0 or projectile.position_vec2d.x > 640 or \
                projectile.position_vec2d.y < 0 or projectile.position_vec2d.y > 480:
            player.projectiles.remove(projectile)
            continue
        pos_x = projectile.position_vec2d.x
        pos_y = projectile.position_vec2d.y
        pos_dir_x = pos_x + projectile.direction_vec2d.x
        pos_dir_y = pos_y + projectile.direction_vec2d.y
        canvas_abs.create_line(pos_x,
                               pos_y,
                               pos_dir_x,
                               pos_dir_y, fill="#AAAAFF")

    # transformed map

    # render_graphics TRANS

    # minimap absolute map trans
    player_pixel_trans_x = WINDOW_WIDTH / 6
    player_pixel_trans_y = WINDOW_HEIGHT / 2

    canvas_trans.create_oval(player_pixel_trans_x,
                             player_pixel_trans_y,
                             player_pixel_trans_x + 10,
                             player_pixel_trans_y + 10, fill="#999999")

    canvas_trans.create_line(player_pixel_trans_x + 5,
                             player_pixel_trans_y + 5,
                             player_pixel_trans_x + 15,
                             player_pixel_trans_y + 5, fill="#FFFFFF")
    canvas_trans.create_line(player_pixel_trans_x,
                             0,
                             player_pixel_trans_x,
                             WINDOW_HEIGHT, fill="#FF0000")

    player_angle = player.angle
    portal_last_points_buffer = []

    for i, line in enumerate(subsector.get_line_iterator()):  # type: line.Line

        # transform vertexes relative to the player
        diff_1_x = line.first.x - player.x
        diff_2_x = line.second.x - player.x
        diff_1_y = line.first.y - player.y
        diff_2_y = line.second.y - player.y

        # rotate around the player
        diff_rot_1_x = diff_1_x * math.cos(math.radians(player_angle)) + diff_1_y * math.sin(math.radians(player_angle))
        diff_rot_1_y = - diff_1_x * math.sin(math.radians(player_angle)) + diff_1_y * math.cos(
            math.radians(player_angle))

        diff_rot_2_x = diff_2_x * math.cos(math.radians(player_angle)) + diff_2_y * math.sin(
            math.radians(player_angle))
        diff_rot_2_y = - diff_2_x * math.sin(math.radians(player_angle)) + diff_2_y * math.cos(
            math.radians(player_angle))

        # line clipping behind camera
        if not portal:
            if (diff_rot_1_x <= 0.1 and diff_rot_2_x <= 0.1):  # trivial reject
                continue
            elif (diff_rot_1_x <= 0.1):  # 1 x is behind player, calculate
                diff_rot_1_x, diff_rot_1_y = calculate_x_y_line_for_x(diff_rot_2_y, diff_rot_1_y, diff_rot_2_x,
                                                                      diff_rot_1_x, 2)

            elif (diff_rot_2_x <= 0.1):  # 2 x is behind player, calculate
                diff_rot_2_x, diff_rot_2_y = calculate_x_y_line_for_x(diff_rot_2_y, diff_rot_1_y, diff_rot_2_x,
                                                                      diff_rot_1_x, 2)

        diff_rot_center_1_x = diff_rot_1_x + WINDOW_WIDTH / 6
        diff_rot_center_1_y = diff_rot_1_y + WINDOW_HEIGHT / 2
        diff_rot_center_2_x = diff_rot_2_x + WINDOW_WIDTH / 6
        diff_rot_center_2_y = diff_rot_2_y + WINDOW_HEIGHT / 2

        canvas_trans.create_line(diff_rot_center_1_x, diff_rot_center_1_y, diff_rot_center_2_x, diff_rot_center_2_y,
                                 fill=fill_color)

        # find angle to point 1
        p1_angle_rad = math.atan2(diff_rot_1_y, diff_rot_1_x)
        # find angle to point 2
        p2_angle_rad = math.atan2(diff_rot_2_y, diff_rot_2_x)

        # calculate distance from player angle and triangle hypotenuse

        line_point_distance_1 = math.sqrt(diff_rot_1_x * diff_rot_1_x + diff_rot_1_y * diff_rot_1_y)
        line_point_distance_2 = math.sqrt(diff_rot_2_x * diff_rot_2_x + diff_rot_2_y * diff_rot_2_y)
        # if line_point_distance_1 > 0:
        line_point_distance_1 = math.cos(p1_angle_rad) * line_point_distance_1
        # if line_point_distance_2 > 0:
        line_point_distance_2 = math.cos(p2_angle_rad) * line_point_distance_2

        if line_point_distance_1 > 0:
            diff_rot_3d_1_x = diff_rot_1_y * 128 / line_point_distance_1 + WINDOW_WIDTH / 6
            line_point_distance_1 = 100 / (line_point_distance_1 / 50)
            diff_rot_3d_1_y = diff_rot_1_y
        else:
            diff_rot_3d_1_x = 10
            diff_rot_3d_1_y = 10

        if line_point_distance_2 > 0:
            diff_rot_3d_2_x = diff_rot_2_y * 128 / line_point_distance_2 + WINDOW_WIDTH / 6
            line_point_distance_2 = 100 / (line_point_distance_2 / 50)
            diff_rot_3d_2_y = diff_rot_2_y
        else:
            diff_rot_3d_2_x = 10
            diff_rot_3d_2_y = 10

        looking_dot = Vec2d.dot_product_between(line.normal, player_aiming_vec2d)

        outline_color = "#FFFF00"

        # handling of narrow portal and its edges
        # interpolation of lines
        is_one_point_visible = False
        if portal:
            if portal[0] < diff_rot_3d_1_x < portal[1]:
                is_one_point_visible = True
                if diff_rot_3d_2_x < portal[0]:
                    diff_rot_3d_2_x, diff_rot_3d_2_y = calculate_x_y_line_for_x(diff_rot_2_y, diff_rot_1_y,
                                                                                diff_rot_2_x,
                                                                                diff_rot_1_x, portal[0])
                elif diff_rot_3d_2_x > portal[1]:
                    diff_rot_3d_2_x, diff_rot_3d_2_y = calculate_x_y_line_for_x(diff_rot_2_y, diff_rot_1_y,
                                                                                diff_rot_2_x,
                                                                                diff_rot_1_x, portal[1])
                    # change y towards portal1
            elif portal[0] < diff_rot_3d_2_x < portal[1]:
                is_one_point_visible = True
                if diff_rot_3d_1_x < portal[0]:
                    diff_rot_3d_1_x, diff_rot_3d_1_y = calculate_x_y_line_for_x(diff_rot_2_y, diff_rot_1_y,
                                                                                diff_rot_2_x,
                                                                                diff_rot_1_x, portal[0])
                    # change y towards portal0
                elif diff_rot_3d_1_x > portal[1]:
                    diff_rot_3d_1_x, diff_rot_3d_1_y = calculate_x_y_line_for_x(diff_rot_2_y, diff_rot_1_y,
                                                                                diff_rot_2_x,
                                                                                diff_rot_1_x, portal[1])
                    # change y towards portal1
            elif diff_rot_3d_1_x < portal[0] < portal[1] < diff_rot_3d_2_x:
                is_one_point_visible = True
                # both points are outof portal
                diff_rot_3d_1_x, diff_rot_3d_1_y = calculate_x_y_line_for_x(diff_rot_2_y, diff_rot_1_y,
                                                                            diff_rot_2_x,
                                                                            diff_rot_1_x, portal[0])
                diff_rot_3d_2_x, diff_rot_3d_2_y = calculate_x_y_line_for_x(diff_rot_2_y, diff_rot_1_y,
                                                                            diff_rot_2_x,
                                                                            diff_rot_1_x, portal[1])
            elif diff_rot_3d_2_x < portal[0] < portal[1] < diff_rot_3d_1_x:
                is_one_point_visible = True
                # both points are out of portal
                diff_rot_3d_2_x, diff_rot_3d_2_y = calculate_x_y_line_for_x(diff_rot_2_y, diff_rot_1_y,
                                                                            diff_rot_2_x,
                                                                            diff_rot_1_x, portal[0])
                diff_rot_3d_1_x, diff_rot_3d_1_y = calculate_x_y_line_for_x(diff_rot_2_y, diff_rot_1_y,
                                                                            diff_rot_2_x,
                                                                            diff_rot_1_x, portal[1])

        points = [
            diff_rot_3d_1_x,
            300 + line_point_distance_1,
            diff_rot_3d_1_x,
            300 - line_point_distance_1,
            diff_rot_3d_2_x,
            300 - line_point_distance_2,
            diff_rot_3d_2_x,
            300 + line_point_distance_2,
        ]

        portal_rendered = False
        if not portal:
            if line == portal_line:
                portal_rendered = True
                render_sector(tree.get_neighbours(player), portal_line,
                              portal=sorted([diff_rot_3d_1_x, diff_rot_3d_2_x]))

        if (not portal or is_one_point_visible) and not portal_rendered:
            fill_color = "#FFFFFF"
            render_polygon(render_type=RenderType.POLY,
                           canvas=canvas_3d,
                           point_list=points,
                           fill_color=fill_color,
                           outline_color=outline_color)

            render_polygon(render_type=RenderType.LINE,
                           canvas=canvas_3d_2,
                           point_list=points,
                           fill_color=fill_color,
                           outline_color=outline_color)


while isAlive:

    if 9 in keyboard.keys:  # ESC = 9
        isAlive = False

    vec2d_forward, vec2d_sideways = player.get_vectors_from_keyboard_input(keyboard)  # hangle keyboard input for player
    vec2d_combined = Vec2d(vec2d_forward.x, vec2d_forward.y)
    vec2d_combined.add_vec2d_xy(vec2d_sideways.x, vec2d_sideways.y)

    time_render_start = time_render_end
    time_render_end = time.time()
    time_render_delta = time_render_end - time_render_start
    if time_render_delta < 0.01:
        time.sleep(0.01 - time_render_delta)

    # render_graphics ABS
    # wipe screen
    canvas_abs.delete("all")
    # wipe screen
    canvas_trans.delete("all")
    canvas_3d.delete("all")
    canvas_3d_2.delete("all")

    player_pixel_x = player.x  # * PIXEL_SIZE
    player_pixel_y = player.y  # * PIXEL_SIZE

    # BSP

    player_aiming_vec2d = Vec2d(math.cos(math.radians(player.angle)), math.sin(math.radians(player.angle)))

    half_fov = player.fov / 2
    start_fov = int(player.angle - half_fov)
    end_fov = int(player.angle + half_fov)
    current_subsector, current_portal_line = tree.travers(player)
    render_sector(current_subsector, current_portal_line)

    msgL1.set("Keys: {0:s}".format(str(keyboard.keys)))
    msgL3.set("vec2d_forward.x: {0:f}, vec2d_forward.y: {1:f}, vec2d_sideways.x: {2:f}, vec2d_sideways.x: {3:f}".format(
        vec2d_forward.x, vec2d_forward.y, vec2d_sideways.x, vec2d_sideways.y))
    msgL4.set(
        "PA: {0:.2f}, PSX: {1:.2f}, PSY: {2:.2f}".format(player.velocity_angle, player.velocity_x, player.velocity_y))
    player.set_velocity_x(player.velocity_x + vec2d_combined.x)
    player.set_velocity_y(player.velocity_y + vec2d_combined.y)
    player.tick()
    frame.update()
    frame.update_idletasks()

# end the game
frame.quit()
