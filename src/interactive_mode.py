# src/interactive_mode.py
import sys
# OLD
# from plateau import Plateau
# from rover import Rover

# NEW
from hexrover.compat.plateau_compat import Plateau
from hexrover.compat.rover_compat import Rover

from visualizer import MarsRoverVisualizer, Colors


class InteractiveRoverController:
    def __init__(self):
        self.plateau = None
        self.visualizer = None
        self.current_rover = None

    def setup_plateau(self):
        """Set up the plateau dimensions"""
        print(f"{Colors.BOLD}{Colors.CYAN}🚀 Mars Rover Interactive Mode 🚀{Colors.RESET}")
        print(f"{Colors.YELLOW}{'=' * 40}{Colors.RESET}")
        print()

        while True:
            try:
                dimensions = input(f"{Colors.WHITE}Enter plateau dimensions (max_x max_y): {Colors.RESET}").strip()
                max_x, max_y = map(int, dimensions.split())
                if max_x < 0 or max_y < 0:
                    raise ValueError("Dimensions must be non-negative")
                break
            except ValueError as e:
                print(f"{Colors.RED}Invalid input. Please enter two non-negative integers.{Colors.RESET}")

        self.plateau = Plateau(max_x, max_y)
        self.visualizer = MarsRoverVisualizer(self.plateau, delay=0.3)
        print(f"{Colors.GREEN}✅ Plateau created: {max_x} x {max_y}{Colors.RESET}")

    def create_rover(self):
        """Create a new rover at specified position"""
        while True:
            try:
                position = input(f"{Colors.WHITE}Enter rover position (x y direction): {Colors.RESET}").strip()
                x, y, heading = position.split()
                x, y = int(x), int(y)

                if not self.plateau.is_within_bounds(x, y):
                    raise ValueError(f"Position ({x}, {y}) is outside plateau bounds")

                if heading not in ['N', 'E', 'S', 'W']:
                    raise ValueError("Direction must be N, E, S, or W")

                break
            except ValueError as e:
                print(f"{Colors.RED}Invalid input: {e}{Colors.RESET}")

        rover = Rover(x, y, heading, self.plateau)
        rover_id = self.visualizer.add_rover(rover)
        self.current_rover = rover

        print(f"{Colors.GREEN}✅ Rover created at ({x}, {y}) facing {heading}{Colors.RESET}")
        self.visualizer.draw_plateau(f"Rover deployed at ({x}, {y}) facing {heading}")

        return rover_id

    def control_rover(self):
        """Interactive rover control"""
        if not self.current_rover:
            print(f"{Colors.RED}No rover available. Create a rover first.{Colors.RESET}")
            return

        print(f"\n{Colors.BOLD}{Colors.YELLOW}🎮 Rover Control Mode{Colors.RESET}")
        print(f"{Colors.WHITE}Commands: L (turn left), R (turn right), M (move forward)")
        print(f"Type 'quit' to exit, 'help' for commands, 'status' for rover info{Colors.RESET}")
        print()

        while True:
            try:
                command = input(f"{Colors.CYAN}Rover Command> {Colors.RESET}").strip().upper()

                if command == 'QUIT':
                    break
                elif command == 'HELP':
                    self.show_help()
                elif command == 'STATUS':
                    self.show_rover_status()
                elif command == 'CLEAR':
                    self.visualizer.rover_trails[0] = []  # Clear trail
                    self.visualizer.draw_plateau("Trail cleared")
                elif len(command) == 1 and command in 'LRM':
                    self.execute_single_command(command)
                elif all(c in 'LRM' for c in command) and len(command) > 1:
                    self.execute_command_sequence(command)
                else:
                    print(f"{Colors.RED}Invalid command. Type 'help' for available commands.{Colors.RESET}")

            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}Use 'quit' to exit properly.{Colors.RESET}")
            except Exception as e:
                print(f"{Colors.RED}Error: {e}{Colors.RESET}")

    def execute_single_command(self, command):
        """Execute a single rover command"""
        old_pos = (self.current_rover.x, self.current_rover.y)

        if command == 'L':
            self.current_rover.turn_left()
            action = "Turned LEFT"
        elif command == 'R':
            self.current_rover.turn_right()
            action = "Turned RIGHT"
        elif command == 'M':
            self.current_rover.move()
            action = "Moved FORWARD"
            # Add to trail if rover moved
            if (self.current_rover.x, self.current_rover.y) != old_pos:
                if len(self.visualizer.rover_trails) > 0:
                    self.visualizer.rover_trails[0].append(old_pos)

        info = f"{action} | Position: ({self.current_rover.x}, {self.current_rover.y}, {self.current_rover.heading})"
        self.visualizer.draw_plateau("Manual Control", info)

    def execute_command_sequence(self, commands):
        """Execute a sequence of commands"""
        print(f"{Colors.YELLOW}Executing sequence: {commands}{Colors.RESET}")
        for command in commands:
            self.execute_single_command(command)

    def show_help(self):
        """Show help information"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}Available Commands:{Colors.RESET}")
        print(f"{Colors.WHITE}  L         - Turn rover left (90 degrees)")
        print(f"  R         - Turn rover right (90 degrees)")
        print(f"  M         - Move rover forward one step")
        print(f"  LRM...    - Execute sequence of commands")
        print(f"  status    - Show current rover status")
        print(f"  clear     - Clear rover trail")
        print(f"  help      - Show this help")
        print(f"  quit      - Exit interactive mode{Colors.RESET}")
        print()

    def show_rover_status(self):
        """Show current rover status"""
        if self.current_rover:
            print(f"\n{Colors.BOLD}{Colors.GREEN}🤖 Rover Status:{Colors.RESET}")
            print(f"{Colors.WHITE}  Position: ({self.current_rover.x}, {self.current_rover.y})")
            print(f"  Direction: {self.current_rover.heading}")
            print(
                f"  Trail length: {len(self.visualizer.rover_trails[0]) if self.visualizer.rover_trails else 0} steps{Colors.RESET}")
            print()

    def run(self):
        """Main interactive loop"""
        try:
            self.setup_plateau()
            self.create_rover()
            self.control_rover()

            print(f"\n{Colors.GREEN}Thank you for using Mars Rover Interactive Mode!{Colors.RESET}")

        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Exiting...{Colors.RESET}")
        except Exception as e:
            print(f"\n{Colors.RED}Unexpected error: {e}{Colors.RESET}")


if __name__ == "__main__":
    controller = InteractiveRoverController()
    controller.run()