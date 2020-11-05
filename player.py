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

from projectile import Projectile
from vectors import Vec2d

MAX_VELOCITY_ANGLE = 5
MAX_VELOCITY_STEP = 1

SIZE_R = 5


class Player(object):
    def __init__(self, x, y, angle):
        self.__x = x
        self.__y = y
        self.__angle = angle
        self.__velocity_x = 0
        self.__velocity_y = 0
        self.__velocity_angle = 0
        self.__fov = 90
        self.__aim_x = 0
        self.__aim_y = 0
        self.projectiles = []
        self.is_fire_on = False

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def fov(self):
        return self.__fov

    @property
    def aim_x(self):
        return self.__aim_x

    @property
    def aim_y(self):
        return self.__aim_y

    @property
    def angle(self):
        return self.__angle

    @property
    def velocity_x(self):
        return self.__velocity_x

    @property
    def velocity_y(self):
        return self.__velocity_y

    @property
    def velocity_angle(self):
        return self.__velocity_angle

    def set_x(self, x):
        self.__x = x

    def set_y(self, y):
        self.__y = y

    def set_aim_x(self, aim_x):
        self.__aim_x = aim_x

    def set_aim_y(self, aim_y):
        self.__aim_y = aim_y

    def set_angle(self, angle):
        self.__angle = angle

    def set_velocity_x(self, velocity_x):
        if velocity_x < -MAX_VELOCITY_STEP:
            velocity_x = -MAX_VELOCITY_STEP
        if velocity_x > MAX_VELOCITY_STEP:
            velocity_x = MAX_VELOCITY_STEP
        self.__velocity_x = velocity_x

    def set_velocity_y(self, velocity_y):
        if velocity_y < -MAX_VELOCITY_STEP:
            velocity_y = -MAX_VELOCITY_STEP
        if velocity_y > MAX_VELOCITY_STEP:
            velocity_y = MAX_VELOCITY_STEP
        self.__velocity_y = velocity_y

    def set_velocity_angle(self, velocity_angle):
        if velocity_angle < -MAX_VELOCITY_ANGLE:
            velocity_angle = -MAX_VELOCITY_ANGLE
        if velocity_angle > MAX_VELOCITY_ANGLE:
            velocity_angle = MAX_VELOCITY_ANGLE
        self.__velocity_angle = velocity_angle

    def process_view_angle(self):
        self.set_angle(self.angle + self.velocity_angle)
        self.set_velocity_angle(self.velocity_angle * 0.1)

        if self.angle >= 360:
            self.set_angle(self.angle - 360)
        if self.angle < 0:
            self.set_angle(self.angle + 360)

    def move_player(self):
        # TODO Collision detection
        self.set_x(self.x + self.velocity_x)
        self.set_y(self.y + self.velocity_y)
        self.set_velocity_x(self.velocity_x * 0.5)
        self.set_velocity_y(self.velocity_y * 0.5)
        self.set_mouse_angle()
        self.process_view_angle()

    def tick(self):
        self.move_player()
        self.move_projectiles()
        if self.is_fire_on:
            directional_vec2d = Vec2d(self.__aim_x - self.__x, self.__aim_y - self.__y).normalize()
            directional_vec2d.multiply_by_factor(3)  # speed up projectiles
            self.projectiles.append(
                Projectile(
                    Vec2d(self.__x + SIZE_R, self.__y + SIZE_R),
                    directional_vec2d
                )
            )

    def __str__(self):
        return u'Player: x {0:f}, y {1:f}, < {2:f}'.format(self.x, self.y, self.angle)

    def set_mouse_angle(self):
        x = self.__x + SIZE_R
        y = self.__y + SIZE_R
        target_x = self.__aim_x
        target_y = self.__aim_y
        if x - target_x != 0:
            degree = 0
            if x < target_x:
                degree = 180
            self.set_angle(
                180 - degree + math.degrees(
                    math.atan(
                        (y - target_y) / (x - target_x)
                    )
                )
            )

    def start_fire(self):
        self.is_fire_on = True

    def end_fire(self):
        self.is_fire_on = False

    def move_projectiles(self):
        for projectile in self.projectiles:
            projectile.move()

    def get_vectors_from_keyboard_input(self, keyboard):
        vec2d_forward = Vec2d(0, 0)
        vec2d_sideways = Vec2d(0, 0)

        player_angle = self.angle
        player_velocity_angle = self.velocity_angle

        # keyboard
        if 87 in keyboard.keys or 25 in keyboard.keys:  # 87 = w
            # go forward
            vec2d_forward.add_vec2d_xy(
                math.cos(math.radians(player_angle)),
                math.sin(math.radians(player_angle)),
            )
            # player.set_velocity_x(player.velocity_x + math.cos(math.radians(player.angle)) / 10)
            # player.set_velocity_y(player.velocity_y + math.sin(math.radians(player.angle)) / 10)
        if 83 in keyboard.keys or 39 in keyboard.keys:  # 39 = s
            # go backward
            vec2d_forward.add_vec2d_xy(
                -math.cos(math.radians(player_angle)),
                -math.sin(math.radians(player_angle)),
            )
            # player.set_velocity_x(player.velocity_x - math.cos(math.radians(player.angle)) / 10)
            # player.set_velocity_y(player.velocity_y - math.sin(math.radians(player.angle)) / 10)

        if 81 in keyboard.keys or 24 in keyboard.keys:  # 81 = Q

            self.set_velocity_angle(player_velocity_angle - 25)
            # player.set_velocity_x(player.velocity_x + math.cos(math.radians(player.angle)) / 10)
            # player.set_velocity_y(player.velocity_y + math.sin(math.radians(player.angle)) / 10)
        if 69 in keyboard.keys or 26 in keyboard.keys:  # 69 = E
            self.set_velocity_angle(player_velocity_angle + 25)
            # player.set_velocity_x(player.velocity_x - math.cos(math.radians(player.angle)) / 10)
            # player.set_velocity_y(player.velocity_y - math.sin(math.radians(player.angle)) / 10)

        if 68 in keyboard.keys or 40 in keyboard.keys:  # 40 = d

            # go right
            vec2d_sideways.add_vec2d_xy(
                math.cos(math.radians(player_angle + 90)),
                math.sin(math.radians(player_angle + 90)),
            )

        if 65 in keyboard.keys or 38 in keyboard.keys:  # 38 = a
            # go left
            vec2d_sideways.add_vec2d_xy(
                math.cos(math.radians(player_angle - 90)),
                math.sin(math.radians(player_angle - 90)),
            )
        return vec2d_forward, vec2d_sideways
