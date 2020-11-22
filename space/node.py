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
from space.subsector import Subsector
from space.vectors import Vec2d


class Node:

    def __init__(self, line, left, right):
        self.line = line
        self.left = left
        self.right = right

    def travers(self, player):
        is_under = self.line.is_point_under(Vec2d(player.x, player.y))
        future_node = self.left if is_under else self.right

        if isinstance(future_node, Subsector):
            return future_node, self.line
        elif isinstance(future_node, Node):
            return future_node.travers(player)

    def get_neighbours(self, player):
        is_under = self.line.is_point_under(Vec2d(player.x, player.y))
        return self.left if not is_under else self.right
