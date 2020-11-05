from vectors import Vec2d


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
