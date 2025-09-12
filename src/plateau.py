class Plateau:
    def __init__(self, max_x: int, max_y: int):
        self.max_x = max_x
        self.max_y = max_y

    def is_within_bounds(self, x: int, y: int) -> bool:
        return 0 <= x <= self.max_x and 0 <= y <= self.max_y
