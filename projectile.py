from vectors import Vec2d


class Projectile(object):
    def __init__(self, position_vec2d, direction_vec2d):
        self.position_vec2d = position_vec2d  # type: Vec2d
        self.direction_vec2d = direction_vec2d # type: Vec2d

    def move(self):
        self.position_vec2d.add_vec2d(self.direction_vec2d)