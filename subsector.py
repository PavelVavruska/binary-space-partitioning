class Subsector:
    def __init__(self, polygon_list):
        self.polygon_list = polygon_list

    def get_line_iterator(self):
        for line in self.polygon_list:
            yield line