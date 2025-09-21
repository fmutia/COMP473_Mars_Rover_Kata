# 🚀 Mars Rover Kata - Complete Implementation

A comprehensive implementation of the Mars Rover Kata with advanced features including visual simulation, interactive control, collision detection, and mission analytics.

## 📁 Project Structure

```
COMP473_Mars_Rover_Kata/
├── .github/
│   └── workflows/
│       └── ci.yml                 # GitHub Actions CI/CD
├── docs/
│   └── ADR.md                     # Architecture Decision Records
├── src/
│   ├── __init__.py                # Package initialization
│   ├── plateau.py                 # Plateau class
│   ├── rover.py                   # Basic Rover class
│   ├── main.py                    # Original simulation
│   ├── enhanced_rover.py          # Advanced rover with collision detection
│   ├── visualizer.py              # TUI visualization system
│   ├── interactive_mode.py        # Interactive rover control
│   └── main_enhanced.py           # Enhanced CLI interface
├── tests/
│   ├── __init__.py                # Test package initialization
│   ├── test_plateau.py            # Plateau tests
│   ├── test_rover.py              # Rover tests
│   └── test_integration.py        # Integration tests
├── tools/
│   └── self_evaluation.py         # Self-evaluation generator
├── SELF_EVALUATION.md             # Team self-evaluation
└── README.md                      # This file
```

## 🚀 Quick Start

### 1. Clone and Setup
```bash
git clone <your-repo-url>
cd COMP473_Mars_Rover_Kata
pip install pytest pytest-cov flake8 black isort mypy
```

### 2. Run Basic Simulation
```bash
python src/main.py
```

### 3. Run Visual Simulation
```bash
python src/main_enhanced.py --visual
```

## 🎮 Running the Application

### Basic Mode (Original Kata)
```bash
# Run with built-in example
python src/main.py

# Output:
# 1 3 N
# 5 1 E
```

### Enhanced Command Line Interface
```bash
# Show help and available options
python src/main_enhanced.py --help

# Run with built-in example (text output)
python src/main_enhanced.py

# Run with custom input file
python src/main_enhanced.py --file input.txt

# Save results to file
python src/main_enhanced.py --output results.txt
```

### Visual Simulation Mode 🎬
```bash
# Run visual simulation with default speed
python src/main_enhanced.py --visual

# Slower animation for better visibility
python src/main_enhanced.py --visual --speed 1.2

# Faster animation
python src/main_enhanced.py --visual --speed 0.3

# Visual simulation with custom input file
python src/main_enhanced.py --file mission.txt --visual
```

**Example Visual Output:**
```
🚀 MARS ROVER MISSION CONTROL 🚀
==================================================

Rover 1 - Step 3/9: Turned LEFT
Command: 'L' | Position: (1, 2, W)

   0 1 2 3 4 5
5  · · · · · ·
4  · · · · · ·
3  · · · · · ·
2  · ← · · · ·
1  · · · · · ·
0  · · · · · ·

Legend:
  Rover 1: ← at (1, 2) facing W
  Rover 2: → at (3, 3) facing E
  · = Rover trail
```

### Interactive Control Mode 🎮
```bash
# Launch interactive rover control
python src/main_enhanced.py --interactive
```

**Interactive Commands:**
- `L` - Turn rover left
- `R` - Turn rover right
- `M` - Move rover forward
- `LMRM...` - Execute command sequences
- `status` - Show rover information
- `clear` - Clear rover trail
- `help` - Show available commands
- `quit` - Exit interactive mode

**Example Interactive Session:**
```
🚀 Mars Rover Interactive Mode 🚀
========================================

Enter plateau dimensions (max_x max_y): 5 5
✅ Plateau created: 5 x 5
Enter rover position (x y direction): 2 2 N
✅ Rover created at (2, 2) facing N

🎮 Rover Control Mode
Commands: L (turn left), R (turn right), M (move forward)
Type 'quit' to exit, 'help' for commands, 'status' for rover info

Rover Command> M
[Visual display updates]

Rover Command> status
🤖 Rover Status:
  Position: (2, 3)
  Direction: N
  Trail length: 1 steps

Rover Command> LMLM
[Executes sequence: Left, Move, Left, Move]
```

### Enhanced Simulation with Analytics 📊
```bash
# Run enhanced simulation with collision detection and statistics
python src/enhanced_rover.py

# Example output with mission report
============================================================
🚀 MARS ROVER MISSION REPORT 🚀
============================================================

📍 MISSION OVERVIEW:
   Plateau Size: 5 x 5
   Total Rovers: 2

📊 AGGREGATE STATISTICS:
   Total Moves: 8
   Total Turns: 6
   Blocked Moves: 0
   Positions Explored: 9
   Plateau Coverage: 25.0%

🤖 INDIVIDUAL ROVER REPORTS:
   Rover-1:
      Final Position: 1 3 N
      Moves Made: 4
      Turns Made: 4
      Blocked Moves: 0
      Unique Positions: 5

✅ NO COLLISIONS DETECTED
```

## 🧪 Running Tests

### Run All Tests
```bash
# Run complete test suite
pytest tests/ -v

# Run tests with coverage report
pytest tests/ -v --cov=src --cov-report=term-missing
```

### Run Specific Test Categories
```bash
# Basic functionality tests
pytest tests/test_plateau.py tests/test_rover.py -v

# Integration tests
pytest tests/test_integration.py -v

```

### Expected Test Output
```bash
=============================================================================== test session starts ===============================================================================
platform win32 -- Python 3.12.2, pytest-8.4.2, pluggy-1.6.0 -- python.exe
cachedir: .pytest_cache
rootdir: C:\Users\...\COMP473_Mars_Rover_Kata
plugins: anyio-4.2.0, cov-7.0.0
collected 33 items

tests/test_integration.py::TestIntegration::test_original_example PASSED     [  3%]
tests/test_integration.py::TestIntegration::test_single_rover PASSED         [  6%]
tests/test_plateau.py::test_plateau_bounds PASSED                            [ 21%]
tests/test_rover.py::test_rover_moves_correctly PASSED                       [ 39%]
tests/test_rover.py::test_second_rover PASSED                                [ 42%]
...
================================ 33 passed in 0.19s ================================
```

## 📝 Input Format

### Standard Input Format
```
plateau_max_x plateau_max_y
rover1_x rover1_y rover1_direction
rover1_commands
rover2_x rover2_y rover2_direction
rover2_commands
...
```

### Example Input File (`input.txt`)
```
5 5
1 2 N
LMLMLMLMM
3 3 E
MMRMMRMRRM
0 0 S
MMRMMLM
```

### Commands
- **L** - Turn 90 degrees left
- **R** - Turn 90 degrees right
- **M** - Move forward one grid point

### Directions
- **N** - North (up)
- **E** - East (right)
- **S** - South (down)
- **W** - West (left)

## 🏆 Extra Credit Features

### 1. Terminal User Interface (TUI) Visualization
- **Real-time animation** of rover movements
- **Color-coded rovers** with unique identifiers
- **Trail visualization** showing rover paths
- **Step-by-step command narration**
- **Professional mission control interface**

### 2. Interactive Rover Control
- **Manual rover control** via keyboard commands
- **Real-time visual feedback**
- **Command sequences** and status checking
- **Built-in help system**

### 3. Advanced Rover System
- **Collision detection** between multiple rovers
- **Movement statistics** and analytics
- **Mission management** and reporting
- **Performance metrics** and coverage analysis

### 4. Enhanced Command Line Interface
- **Multiple operation modes**
- **File input/output support**
- **Customizable animation speed**
- **Professional help system**

## 🔧 Troubleshooting

### Import Errors
If you encounter `ModuleNotFoundError`, try:

```bash
# Set Python path (Windows Command Prompt)
set PYTHONPATH=%PYTHONPATH%;src
python src/main_enhanced.py --visual

# Set Python path (Windows PowerShell)
$env:PYTHONPATH = "$env:PYTHONPATH;src"
python src/main_enhanced.py --visual

# Or run from src directory
cd src
python main_enhanced.py --visual
```

### Test Import Issues
```bash
# Set Python path for tests
$env:PYTHONPATH = "$env:PYTHONPATH;src"
```

### Visual Mode Not Working
- Ensure your terminal supports ANSI colors
- Try reducing animation speed: `--speed 1.0`
- Use Windows Terminal or modern terminal emulator

## 📋 Development Workflow

### Code Quality Checks
```bash
# Format code with black
black src tests --check

# Sort imports with isort
isort --check-only src tests

# Lint code with flake8
flake8 src tests --max-line-length=127

# Type check with mypy
mypy src --ignore-missing-imports
```

### Run CI Pipeline Locally
```bash
# Install development dependencies
pip install pytest pytest-cov flake8 black isort mypy

# Run the full pipeline
pytest tests/ -v --cov=src
black --check src tests
flake8 src tests --max-line-length=127
isort --check-only src tests
mypy src --ignore-missing-imports
```

## 📚 Architecture Decision Records

See `docs/ADR.md` for detailed architecture decisions including:
- Object-oriented design rationale
- Direction handling approach
- Command processing strategy

## 🎯 Assignment Requirements Checklist

- ✅ **Functional Requirements**: Complete Mars Rover Kata implementation
- ✅ **Object-Oriented Design**: Clean separation of concerns (Rover, Plateau)
- ✅ **Design Principles**: DRY, SoC, Dependency Injection applied
- ✅ **Architecture Decision Records**: Documented in `docs/ADR.md`
- ✅ **Test Suite**: Comprehensive pytest coverage (33+ tests)
- ✅ **GitHub Repository**: Public repo with frequent commits
- ✅ **CI/CD Pipeline**: GitHub Actions workflow
- ✅ **Extra Credit**: TUI visualization + interactive control + advanced features

## 🏅 Extra Credit Achievements

This implementation includes **multiple extra credit enhancements**:

1. **✅ TUI Rendering** - Animated terminal visualization
2. **✅ Interactive Mode** - Manual rover control
3. **✅ Collision Detection** - Multi-rover collision prevention
4. **✅ Mission Analytics** - Advanced statistics and reporting
5. **✅ Professional Interface** - Enhanced CLI with multiple modes

## 🤝 Team Collaboration

All team members should:
1. **Commit frequently** to the GitHub repository
2. **Use descriptive commit messages**
3. **Indicate collaborators** in commit messages when pair programming
4. **Review and test** each other's contributions
5. **Update documentation** as features are added

## 📞 Support

For questions or issues:
1. Check this README for common solutions
2. Review the Architecture Decision Records in `docs/ADR.md`
3. Run tests to verify functionality: `pytest tests/ -v`
4. Consult the instructor for guidance on additional enhancements

---

**🚀 Ready to explore Mars? Launch your rovers and start the mission!**