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
from subsector import Subsector


class Node:

    def __init__(self, line, left, right):

        self.left = left
        self.right = right
        self.line = line

    def travers(self, player):
        """
        TODO: Hardcoded POC
        """
        """player_vec = Vec2d(player.x, player.y).normalize()
        player_aim = Vec2d(player.aim_x, player.aim_y).normalize()
        normal_plane = self.line.normal.normalize()
        normal_vec = Vec2d((self.line.second.x + self.line.first.x)/2, (self.line.second.y + self.line.first.y)/2).normalize()
        dot_1 = player_vec.dot_product_with(normal_vec)
        dot_2 = player_aim.dot_product_with(normal_plane)
        print()
        print(str(dot_1) + "player_vec.dot_product_with(normal_vec)")
        print(str(dot_2) + "player_aim.dot_product_with(normal_plane)")
        print(str(dot_1*dot_2) + " **** ")"""

        if player.y < self.line.first.y:
            if isinstance(self.left, Subsector):
                return self.left, self.line
            elif isinstance(self.left, Node):
                self.left.travers(player)
        else:
            if isinstance(self.right, Subsector):
                return self.right, self.line
            elif isinstance(self.right, Node):
                self.left.travers(player)

    def get_neighbours(self, player):
        """
        TODO: Hardcoded POC
        """
        if player.y > self.line.first.y:
            return self.left
        else:
            return self.right

