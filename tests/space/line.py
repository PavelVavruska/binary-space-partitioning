import unittest

from space.line import Line
from space.vectors import Vec2d


class TestLine(unittest.TestCase):
    def test_is_point_under(self):
        point_1 = Vec2d(1, 1)
        point_2 = Vec2d(2, 2)
        point_3 = Vec2d(2, 3)
        point_4 = Vec2d(2, 0)

        line = Line(point_1, point_2, None)

        self.assertFalse(line.is_point_under(point_3))
        self.assertTrue(line.is_point_under(point_4))


if __name__ == '__main__':
    unittest.main()
