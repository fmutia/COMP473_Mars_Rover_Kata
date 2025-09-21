# src/enhanced_rover.py
from typing import List, Optional, Set, Tuple
from plateau import Plateau


class EnhancedRover:
    """Enhanced rover with collision detection and advanced features"""

    DIRECTIONS = ["N", "E", "S", "W"]

    def __init__(self, x: int, y: int, heading: str, plateau: Plateau, rover_id: str = ""):
        self.x = x
        self.y = y
        self.heading = heading
        self.plateau = plateau
        self.rover_id = rover_id
        self.move_count = 0
        self.turn_count = 0
        self.path_history: List[Tuple[int, int, str]] = [(x, y, heading)]
        self.blocked_moves = 0

    def turn_left(self):
        """Turn rover left (counter-clockwise)"""
        idx = (self.DIRECTIONS.index(self.heading) - 1) % 4
        self.heading = self.DIRECTIONS[idx]
        self.turn_count += 1
        self.path_history.append((self.x, self.y, self.heading))

    def turn_right(self):
        """Turn rover right (clockwise)"""
        idx = (self.DIRECTIONS.index(self.heading) + 1) % 4
        self.heading = self.DIRECTIONS[idx]
        self.turn_count += 1
        self.path_history.append((self.x, self.y, self.heading))

    def get_next_position(self) -> Tuple[int, int]:
        """Get the position the rover would move to (without actually moving)"""
        if self.heading == "N":
            return self.x, self.y + 1
        elif self.heading == "E":
            return self.x + 1, self.y
        elif self.heading == "S":
            return self.x, self.y - 1
        else:  # "W"
            return self.x - 1, self.y

    def can_move(self, other_rovers: Optional[List['EnhancedRover']] = None) -> bool:
        """Check if rover can move forward without collision"""
        new_x, new_y = self.get_next_position()

        # Check plateau boundaries
        if not self.plateau.is_within_bounds(new_x, new_y):
            return False

        # Check collision with other rovers
        if other_rovers:
            for other in other_rovers:
                if other != self and other.x == new_x and other.y == new_y:
                    return False

        return True

    def move(self, other_rovers: Optional[List['EnhancedRover']] = None) -> bool:
        """Move rover forward if possible. Returns True if moved, False if blocked."""
        if self.can_move(other_rovers):
            self.x, self.y = self.get_next_position()
            self.move_count += 1
            self.path_history.append((self.x, self.y, self.heading))
            return True
        else:
            self.blocked_moves += 1
            return False

    def execute_commands(self, commands: str, other_rovers: Optional[List['EnhancedRover']] = None):
        """Execute a sequence of commands with collision detection"""
        for cmd in commands:
            if cmd == "L":
                self.turn_left()
            elif cmd == "R":
                self.turn_right()
            elif cmd == "M":
                self.move(other_rovers)

    def get_position(self) -> str:
        """Get current position as string"""
        return f"{self.x} {self.y} {self.heading}"

    def get_statistics(self) -> dict:
        """Get rover movement statistics"""
        return {
            'rover_id': self.rover_id,
            'final_position': self.get_position(),
            'moves_made': self.move_count,
            'turns_made': self.turn_count,
            'blocked_moves': self.blocked_moves,
            'total_commands': self.move_count + self.turn_count,
            'path_length': len(self.path_history),
            'unique_positions': len(set((x, y) for x, y, _ in self.path_history))
        }

    def has_visited_position(self, x: int, y: int) -> bool:
        """Check if rover has visited a specific position"""
        return any(pos_x == x and pos_y == y for pos_x, pos_y, _ in self.path_history)

    def get_visited_positions(self) -> Set[Tuple[int, int]]:
        """Get all positions visited by this rover"""
        return set((x, y) for x, y, _ in self.path_history)


class MissionControl:
    """Manages multiple rovers with collision detection and mission statistics"""

    def __init__(self, plateau: Plateau):
        self.plateau = plateau
        self.rovers: List[EnhancedRover] = []
        self.mission_log: List[str] = []

    def add_rover(self, x: int, y: int, heading: str, rover_id: str = "") -> EnhancedRover:
        """Add a new rover to the mission"""
        if not rover_id:
            rover_id = f"Rover-{len(self.rovers) + 1}"

        # Check if position is already occupied
        for existing_rover in self.rovers:
            if existing_rover.x == x and existing_rover.y == y:
                raise ValueError(f"Position ({x}, {y}) is already occupied by {existing_rover.rover_id}")

        rover = EnhancedRover(x, y, heading, self.plateau, rover_id)
        self.rovers.append(rover)
        self.mission_log.append(f"Deployed {rover_id} at ({x}, {y}) facing {heading}")
        return rover

    def execute_mission(self, rover_commands: List[Tuple[EnhancedRover, str]]):
        """Execute commands for all rovers in sequence"""
        for rover, commands in rover_commands:
            self.mission_log.append(f"Executing commands for {rover.rover_id}: {commands}")
            rover.execute_commands(commands, self.rovers)

    def get_mission_statistics(self) -> dict:
        """Get comprehensive mission statistics"""
        stats = {
            'plateau_size': f"{self.plateau.max_x} x {self.plateau.max_y}",
            'total_rovers': len(self.rovers),
            'rover_stats': [rover.get_statistics() for rover in self.rovers],
            'mission_log': self.mission_log,
        }

        # Calculate aggregate statistics
        total_moves = sum(rover.move_count for rover in self.rovers)
        total_turns = sum(rover.turn_count for rover in self.rovers)
        total_blocked = sum(rover.blocked_moves for rover in self.rovers)

        all_visited = set()
        for rover in self.rovers:
            all_visited.update(rover.get_visited_positions())

        stats['aggregates'] = {
            'total_moves': total_moves,
            'total_turns': total_turns,
            'total_blocked_moves': total_blocked,
            'unique_positions_explored': len(all_visited),
            'plateau_coverage': f"{len(all_visited) / ((self.plateau.max_x + 1) * (self.plateau.max_y + 1)) * 100:.1f}%"
        }

        return stats

    def detect_collisions(self) -> List[Tuple[EnhancedRover, EnhancedRover]]:
        """Detect any rovers occupying the same position"""
        collisions = []
        for i, rover1 in enumerate(self.rovers):
            for j, rover2 in enumerate(self.rovers[i + 1:], i + 1):
                if rover1.x == rover2.x and rover1.y == rover2.y:
                    collisions.append((rover1, rover2))
        return collisions

    def print_mission_report(self):
        """Print a comprehensive mission report"""
        stats = self.get_mission_statistics()

        print(f"\n{'=' * 60}")
        print(f"🚀 MARS ROVER MISSION REPORT 🚀")
        print(f"{'=' * 60}")

        print(f"\n📍 MISSION OVERVIEW:")
        print(f"   Plateau Size: {stats['plateau_size']}")
        print(f"   Total Rovers: {stats['total_rovers']}")

        print(f"\n📊 AGGREGATE STATISTICS:")
        agg = stats['aggregates']
        print(f"   Total Moves: {agg['total_moves']}")
        print(f"   Total Turns: {agg['total_turns']}")
        print(f"   Blocked Moves: {agg['total_blocked_moves']}")
        print(f"   Positions Explored: {agg['unique_positions_explored']}")
        print(f"   Plateau Coverage: {agg['plateau_coverage']}")

        print(f"\n🤖 INDIVIDUAL ROVER REPORTS:")
        for rover_stat in stats['rover_stats']:
            print(f"   {rover_stat['rover_id']}:")
            print(f"      Final Position: {rover_stat['final_position']}")
            print(f"      Moves Made: {rover_stat['moves_made']}")
            print(f"      Turns Made: {rover_stat['turns_made']}")
            print(f"      Blocked Moves: {rover_stat['blocked_moves']}")
            print(f"      Unique Positions: {rover_stat['unique_positions']}")

        # Check for collisions
        collisions = self.detect_collisions()
        if collisions:
            print(f"\n⚠️  COLLISION ALERTS:")
            for rover1, rover2 in collisions:
                print(f"   {rover1.rover_id} and {rover2.rover_id} at ({rover1.x}, {rover1.y})")
        else:
            print(f"\n✅ NO COLLISIONS DETECTED")

        print(f"\n📋 MISSION LOG:")
        for i, log_entry in enumerate(stats['mission_log'], 1):
            print(f"   {i:2d}. {log_entry}")

        print(f"\n{'=' * 60}")


def run_enhanced_simulation(input_str: str, enable_collisions: bool = True) -> dict:
    """Run simulation with enhanced rovers and collision detection"""
    lines = input_str.strip().splitlines()
    max_x, max_y = map(int, lines[0].split())
    plateau = Plateau(max_x, max_y)

    mission_control = MissionControl(plateau)
    rover_commands = []

    # Parse rovers and commands
    for i in range(1, len(lines), 2):
        x, y, heading = lines[i].split()
        rover_id = f"Rover-{(i // 2) + 1}"
        rover = mission_control.add_rover(int(x), int(y), heading, rover_id)
        commands = lines[i + 1].strip()
        rover_commands.append((rover, commands))

    # Execute mission
    mission_control.execute_mission(rover_commands)

    # Return comprehensive results
    return mission_control.get_mission_statistics()


# Example usage and testing
if __name__ == "__main__":
    example_input = """5 5
1 2 N
LMLMLMLMM
3 3 E
MMRMMRMRRM"""

    print("🚀 Running Enhanced Mars Rover Simulation...")
    stats = run_enhanced_simulation(example_input)

    # Create mission control for report
    lines = example_input.strip().splitlines()
    max_x, max_y = map(int, lines[0].split())
    plateau = Plateau(max_x, max_y)
    mission_control = MissionControl(plateau)

    # Add rovers and execute
    rover_commands = []
    for i in range(1, len(lines), 2):
        x, y, heading = lines[i].split()
        rover_id = f"Rover-{(i // 2) + 1}"
        rover = mission_control.add_rover(int(x), int(y), heading, rover_id)
        commands = lines[i + 1].strip()
        rover_commands.append((rover, commands))

    mission_control.execute_mission(rover_commands)
    mission_control.print_mission_report()