from plateau import Plateau
from rover import Rover

def run_simulation(input_str: str) -> str:
    lines = input_str.strip().splitlines()
    max_x, max_y = map(int, lines[0].split())
    plateau = Plateau(max_x, max_y)

    results = []
    for i in range(1, len(lines), 2):
        x, y, heading = lines[i].split()
        rover = Rover(int(x), int(y), heading, plateau)
        commands = lines[i+1].strip()
        rover.execute_commands(commands)
        results.append(rover.get_position())

    return "\n".join(results)

if __name__ == "__main__":
    example_input = """5 5
1 2 N
LMLMLMLMM
3 3 E
MMRMMRMRRM"""
    print(run_simulation(example_input))
