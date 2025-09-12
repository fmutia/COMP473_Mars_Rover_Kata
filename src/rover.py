class Rover:
    DIRECTIONS = ["N", "E", "S", "W"]

    def __init__(self, x: int, y: int, heading: str, plateau):
        self.x = x
        self.y = y
        self.heading = heading
        self.plateau = plateau

    def turn_left(self):
        idx = (self.DIRECTIONS.index(self.heading) - 1) % 4
        self.heading = self.DIRECTIONS[idx]

    def turn_right(self):
        idx = (self.DIRECTIONS.index(self.heading) + 1) % 4
        self.heading = self.DIRECTIONS[idx]

    def move(self):
        if self.heading == "N":
            new_x, new_y = self.x, self.y + 1
        elif self.heading == "E":
            new_x, new_y = self.x + 1, self.y
        elif self.heading == "S":
            new_x, new_y = self.x, self.y - 1
        else:  # "W"
            new_x, new_y = self.x - 1, self.y

        if self.plateau.is_within_bounds(new_x, new_y):
            self.x, self.y = new_x, new_y

    def execute_commands(self, commands: str):
        for cmd in commands:
            if cmd == "L":
                self.turn_left()
            elif cmd == "R":
                self.turn_right()
            elif cmd == "M":
                self.move()

    def get_position(self) -> str:
        return f"{self.x} {self.y} {self.heading}"
