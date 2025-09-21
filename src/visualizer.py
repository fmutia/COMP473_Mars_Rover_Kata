# src/visualizer.py
import time
import os
import sys
from typing import List, Tuple
from plateau import Plateau
from rover import Rover


class Colors:
    """ANSI color codes for terminal output"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'


class MarsRoverVisualizer:
    def __init__(self, plateau: Plateau, delay: float = 0.5):
        self.plateau = plateau
        self.rovers = []
        self.delay = delay
        self.rover_colors = [Colors.RED, Colors.BLUE, Colors.GREEN, Colors.MAGENTA, Colors.CYAN]
        self.rover_trails = []  # Store trails for each rover

    def add_rover(self, rover: Rover) -> int:
        """Add a rover to the visualization and return its ID"""
        rover_id = len(self.rovers)
        self.rovers.append(rover)
        self.rover_trails.append([])  # Initialize empty trail for this rover
        return rover_id

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def get_direction_symbol(self, heading: str) -> str:
        """Get the symbol for rover direction"""
        symbols = {
            'N': '↑',
            'E': '→',
            'S': '↓',
            'W': '←'
        }
        return symbols.get(heading, '?')

    def draw_plateau(self, step_info: str = "", command_info: str = ""):
        """Draw the current state of the plateau with rovers"""
        self.clear_screen()

        # Title
        print(f"{Colors.BOLD}{Colors.YELLOW}🚀 MARS ROVER MISSION CONTROL 🚀{Colors.RESET}")
        print(f"{Colors.CYAN}{'=' * 50}{Colors.RESET}")
        print()

        # Info panel
        if step_info:
            print(f"{Colors.WHITE}{step_info}{Colors.RESET}")
        if command_info:
            print(f"{Colors.YELLOW}{command_info}{Colors.RESET}")
        print()

        # Create a grid representation
        grid = {}

        # Add rover trails
        for rover_id, trail in enumerate(self.rover_trails):
            color = self.rover_colors[rover_id % len(self.rover_colors)]
            for x, y in trail:
                if (x, y) not in grid:
                    grid[(x, y)] = f"{color}·{Colors.RESET}"

        # Add current rover positions (overwrite trails)
        for rover_id, rover in enumerate(self.rovers):
            color = self.rover_colors[rover_id % len(self.rover_colors)]
            symbol = self.get_direction_symbol(rover.heading)
            grid[(rover.x, rover.y)] = f"{Colors.BOLD}{color}{symbol}{Colors.RESET}"

        # Draw the plateau (inverted Y to match coordinate system)
        print(f"  {Colors.WHITE}", end="")
        for x in range(self.plateau.max_x + 1):
            print(f"{x:2}", end="")
        print(f"{Colors.RESET}")

        for y in range(self.plateau.max_y, -1, -1):
            print(f"{Colors.WHITE}{y:2}{Colors.RESET}", end="")
            for x in range(self.plateau.max_x + 1):
                cell_content = grid.get((x, y), f"{Colors.BG_BLACK} {Colors.RESET}")
                print(f"{cell_content} ", end="")
            print()

        # Legend
        print(f"\n{Colors.BOLD}Legend:{Colors.RESET}")
        for i, rover in enumerate(self.rovers):
            color = self.rover_colors[i % len(self.rover_colors)]
            symbol = self.get_direction_symbol(rover.heading)
            print(
                f"  {Colors.BOLD}{color}Rover {i + 1}{Colors.RESET}: {color}{symbol}{Colors.RESET} at ({rover.x}, {rover.y}) facing {rover.heading}")
        print(f"  {Colors.WHITE}·{Colors.RESET} = Rover trail")
        print()

    def animate_rover_commands(self, rover_id: int, commands: str):
        """Animate a rover executing commands step by step"""
        rover = self.rovers[rover_id]

        print(f"{Colors.BOLD}{Colors.GREEN}Executing commands for Rover {rover_id + 1}: {commands}{Colors.RESET}")
        time.sleep(1)

        for i, command in enumerate(commands):
            # Record current position before move
            old_pos = (rover.x, rover.y)

            # Execute command
            if command == 'L':
                rover.turn_left()
                action = "Turned LEFT"
            elif command == 'R':
                rover.turn_right()
                action = "Turned RIGHT"
            elif command == 'M':
                rover.move()
                action = "Moved FORWARD"
                # Add old position to trail if rover actually moved
                if (rover.x, rover.y) != old_pos:
                    self.rover_trails[rover_id].append(old_pos)
            else:
                continue

            step_info = f"Rover {rover_id + 1} - Step {i + 1}/{len(commands)}: {action}"
            command_info = f"Command: '{command}' | Position: ({rover.x}, {rover.y}, {rover.heading})"

            self.draw_plateau(step_info, command_info)
            time.sleep(self.delay)

    def show_final_state(self):
        """Show the final state of all rovers"""
        self.draw_plateau("🎯 MISSION COMPLETE! Final positions:", "All rovers have completed their missions.")

        print(f"{Colors.BOLD}{Colors.GREEN}Final Rover Positions:{Colors.RESET}")
        for i, rover in enumerate(self.rovers):
            print(f"  Rover {i + 1}: {rover.get_position()}")
        print()


def visualize_simulation(input_str: str, delay: float = 0.8):
    """Main function to run the visual simulation"""
    lines = input_str.strip().splitlines()
    max_x, max_y = map(int, lines[0].split())
    plateau = Plateau(max_x, max_y)

    # Create visualizer
    visualizer = MarsRoverVisualizer(plateau, delay)

    # Parse and add rovers
    rover_commands = []
    for i in range(1, len(lines), 2):
        x, y, heading = lines[i].split()
        rover = Rover(int(x), int(y), heading, plateau)
        rover_id = visualizer.add_rover(rover)
        commands = lines[i + 1].strip()
        rover_commands.append((rover_id, commands))

    # Show initial state
    visualizer.draw_plateau("🌍 INITIAL SETUP", "All rovers deployed and ready for mission!")
    time.sleep(2)

    # Execute commands for each rover
    for rover_id, commands in rover_commands:
        visualizer.animate_rover_commands(rover_id, commands)
        time.sleep(1)

    # Show final state
    visualizer.show_final_state()


if __name__ == "__main__":
    example_input = """5 5
1 2 N
LMLMLMLMM
3 3 E
MMRMMRMRRM"""

    print(f"{Colors.BOLD}{Colors.CYAN}Starting Mars Rover Visual Simulation...{Colors.RESET}")
    time.sleep(1)

    try:
        visualize_simulation(example_input, delay=0.8)
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}Simulation interrupted by user.{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}Error during simulation: {e}{Colors.RESET}")

    input(f"\n{Colors.WHITE}Press Enter to exit...{Colors.RESET}")