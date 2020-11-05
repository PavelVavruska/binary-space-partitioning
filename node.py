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

