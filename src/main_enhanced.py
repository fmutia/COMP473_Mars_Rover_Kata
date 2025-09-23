# src/main_enhanced.py
import sys
import argparse
from typing import List

from hexrover.compat.plateau_compat import Plateau
from hexrover.compat.rover_compat import Rover
from visualizer import visualize_simulation, Colors
from interactive_mode import InteractiveRoverController


def run_simulation(input_str: str) -> str:
    lines: List[str] = [ln.strip() for ln in input_str.strip().splitlines() if ln.strip()]
    if not lines:
        return ""

    # plateau
    max_x, max_y = map(int, lines[0].split())
    plateau = Plateau(max_x, max_y)

    results: List[str] = []
    # process pairs: position line, commands line
    for i in range(1, len(lines), 2):
        x, y, heading = lines[i].split()
        rover = Rover(int(x), int(y), heading.upper(), plateau)

        commands = lines[i + 1].strip().upper()
        rover.execute_commands(commands)

        # append as string "x y H" (legacy format)
        results.append(str(rover))            # compat __str__ -> "x y H"

    return "\n".join(results)


def read_input_file(filename: str) -> str:
    """Read input from file"""
    try:
        with open(filename, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"{Colors.RED}Error: File '{filename}' not found.{Colors.RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"{Colors.RED}Error reading file: {e}{Colors.RESET}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Mars Rover Kata - Navigate rovers on Mars plateau",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
{Colors.BOLD}Examples:{Colors.RESET}
  {Colors.CYAN}python main_enhanced.py{Colors.RESET}                    # Run with built-in example
  {Colors.CYAN}python main_enhanced.py --file input.txt{Colors.RESET}   # Run with input file  
  {Colors.CYAN}python main_enhanced.py --visual{Colors.RESET}          # Visual simulation
  {Colors.CYAN}python main_enhanced.py --interactive{Colors.RESET}     # Interactive mode
  {Colors.CYAN}python main_enhanced.py --visual --speed 0.5{Colors.RESET} # Slower animation

{Colors.BOLD}Input format:{Colors.RESET}
  Line 1: plateau_max_x plateau_max_y
  Line 2: rover1_x rover1_y rover1_direction
  Line 3: rover1_commands
  Line 4: rover2_x rover2_y rover2_direction  
  Line 5: rover2_commands
  ... (repeat for additional rovers)
        """
    )

    parser.add_argument('--file', '-f',
                        help='Input file containing rover instructions')

    parser.add_argument('--visual', '-v', action='store_true',
                        help='Run visual simulation with animation')

    parser.add_argument('--interactive', '-i', action='store_true',
                        help='Run in interactive mode for manual control')

    parser.add_argument('--speed', '-s', type=float, default=0.8,
                        help='Animation speed in seconds (default: 0.8)')

    parser.add_argument('--output', '-o',
                        help='Output file to save results')

    args = parser.parse_args()

    # Interactive mode
    if args.interactive:
        controller = InteractiveRoverController()
        controller.run()
        return

    # Get input data
    if args.file:
        input_data = read_input_file(args.file)
    else:
        # Default example
        input_data = """5 5
1 2 N
LMLMLMLMM
3 3 E
MMRMMRMRRM"""
        print(f"{Colors.YELLOW}Using built-in example data...{Colors.RESET}")

    try:
        if args.visual:
            # Visual simulation
            print(f"{Colors.BOLD}{Colors.CYAN}🚀 Starting Visual Mars Rover Simulation 🚀{Colors.RESET}")
            visualize_simulation(input_data, delay=args.speed)
        else:
            # Standard text-based simulation
            print(f"{Colors.BOLD}{Colors.GREEN}Mars Rover Simulation Results:{Colors.RESET}")
            result = run_simulation(input_data)
            print(result)

            # Save to file if requested
            if args.output:
                with open(args.output, 'w') as f:
                    f.write(result)
                print(f"{Colors.GREEN}Results saved to '{args.output}'{Colors.RESET}")

    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Simulation interrupted by user.{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}Error during simulation: {e}{Colors.RESET}")
        sys.exit(1)


if __name__ == "__main__":
    main()