# Word Bites Solver

A Python-based solver for the Word Bites word puzzle game that finds all valid words that can be formed from a given set of letter tiles.

Includes both a command-line interface and a browser-based web interface for easy tile input and results visualization.

## Table of Contents

- [About Word Bites](#about-word-bites)
- [Game Rules](#game-rules)
- [How This Solver Works](#how-this-solver-works)
- [Installation](#installation)
- [Usage](#usage)
  - [Command-Line Interface](#command-line-interface)
  - [Web Interface](#web-interface)
- [Project Structure](#project-structure)
- [Examples](#examples)
- [Development](#development)

## About Word Bites

Word Bites is a word puzzle game where players must form valid words using letter tiles. Some tiles contain single letters, while others contain multiple letters that must be used together in one orientation but can be split in the other orientation.

## Game Rules

1. **Three Types of Tiles:**
   - **Single-letter tiles**: Can be used in any direction (e.g., "A", "E", "T")
   - **Horizontal tiles**: Multi-letter tiles that work as a unit horizontally but split into individual letters for vertical words (e.g., "AB" can be used as "AB" horizontally, but only "A" or "B" vertically)
   - **Vertical tiles**: Multi-letter tiles that work as a unit vertically but split into individual letters for horizontal words

2. **Word Formation:**
   - Words must be at least 3 letters long
   - Horizontal words have a maximum length of 8 letters (default)
   - Vertical words have a maximum length of 9 letters (default)
   - Each tile can only be used once per word

3. **Group Exclusion Rule:**
   - When a multi-letter tile is split (e.g., "AB" split into "A" and "B"), you cannot use both letters from that tile in the same word
   - Example: If you have a horizontal tile "AB", you can use either "A" or "B" in a vertical word, but not both

4. **Valid Words:**
   - All words must exist in the chosen dictionary
   - Words are case-insensitive

## How This Solver Works

### Algorithm Overview

The Word Bites solver uses a **backtracking algorithm with prefix pruning** for efficient word discovery:

1. **Tile View Generation:**
   - Converts input tiles into two separate views: horizontal and vertical
   - Assigns group IDs to track which letters come from the same multi-letter tile
   - Single tiles appear identically in both views
   - Multi-letter tiles appear whole in one view and split in the other

2. **Prefix Dictionary:**
   - Pre-builds a set of all valid prefixes from the dictionary
   - Enables early pruning of impossible word paths
   - Drastically reduces the search space

3. **Backtracking Search:**
   - Recursively builds words letter-by-letter
   - **Pruning strategies:**
     - Stops if the current word exceeds maximum length
     - Stops if the current word is not a valid prefix
     - Skips tiles that have already been used
     - Enforces group exclusion (can't use multiple letters from the same source tile)
   - Collects all valid words that meet minimum length requirements

4. **Result Organization:**
   - Sorts words by length (longest first) for better gameplay
   - Returns separate lists for horizontal and vertical orientations

### Time Complexity

- **Prefix building:** O(D × L) where D is dictionary size and L is average word length
- **Backtracking:** O(T!) in worst case, but heavily pruned by:
  - Prefix checking (most branches eliminated early)
  - Length constraints
  - Group exclusion rules

In practice, the solver is very fast due to aggressive pruning.

## Installation

### Prerequisites

- Python 3.8 or higher
- For CLI: Standard library only (no external dependencies required)
- For Web interface: Flask and dependencies (see requirements.txt)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd wordbiter
```

2. (Optional but recommended) Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. For CLI only: The solver is ready to use! No additional installation needed.

4. For Web interface: Install web dependencies:
```bash
pip install -r requirements.txt
```

For development with type checking, install optional dependencies:
```bash
pip install mypy pytest
```

## Usage

### Command-Line Interface

#### Interactive Mode

Run the solver interactively to input your game tiles:

```bash
python3 run.py
```

#### Command-Line Options

```bash
python3 run.py [OPTIONS]
```

**Available options:**

- `--min-word-length N`: Set minimum word length (default: 3)
- `--max-horizontal-length N`: Set maximum horizontal word length (default: 8)
- `--max-vertical-length N`: Set maximum vertical word length (default: 9)
- `--only-direction h|v`: Find words in only one direction
  - `h`: Horizontal words only
  - `v`: Vertical words only
- `--dictionary PATH`: Use a custom dictionary file (default: `/usr/share/dict/words`)

#### Quick Start Example

If you're not sure what to enter, try these sample tiles:

```
Single tiles: S C Y B N G
Horizontal tiles: AL UR KI AT
Vertical tiles: ME
```

This will find words like CALKINGS, NATURALS, BRACINGLY, MEGABUCKS, and many others!

### Example Session

```
==================================================
Word Bites Solver
==================================================

Loading dictionary...
Loaded 235,886 words

--------------------------------------------------
Enter single-letter tiles (space-separated, or leave blank):
Single tiles: A E T

Enter horizontal multi-letter tiles (space-separated, or leave blank):
Horizontal tiles: AB CD

Enter vertical multi-letter tiles (space-separated, or leave blank):
Vertical tiles: RT

Configuration:
  Min word length: 3
  Max horizontal length: 8
  Max vertical length: 9
  Direction: both

Searching for words...

==================================================
HORIZONTAL WORDS (Top 30 Longest)
==================================================
Showing top 30 longest words (out of 142 total):

  CREATED
  REACTED
  CATERED
  ...

==================================================
VERTICAL WORDS (Top 30 Longest)
==================================================
Showing top 30 longest words (out of 89 total):

  EART
  RATE
  TEAR
  ...
```

#### Using Custom Dictionaries

The project includes several dictionary files in the `dictionaries/` directory:

```bash
# Use Scrabble dictionary
python3 run.py --dictionary dictionaries/scrabble_words.txt

# Use MIT words
python3 run.py --dictionary dictionaries/mit_words.txt

# Use alpha words
python3 run.py --dictionary dictionaries/words_alpha.txt
```

### Web Interface

#### Starting the Web Server

1. Make sure you have installed Flask dependencies:
```bash
pip install -r requirements.txt
```

2. Start the web server:
```bash
python3 app.py
```

3. Open your browser and navigate to:
```
http://localhost:5001
```

#### Using the Web Interface

The web interface provides a user-friendly form for entering tiles and viewing results:

1. **Enter Tiles**: Fill in the input fields for single-letter, horizontal, and vertical tiles
   - Tiles are automatically converted to uppercase
   - Separate multiple tiles with spaces (e.g., "A E T R")

2. **Configure Options**: Adjust settings as needed
   - Min word length (default: 3)
   - Max horizontal/vertical word length
   - Direction filter (both, horizontal only, or vertical only)

3. **Find Words**: Click the "Find Words" button to solve the puzzle

4. **View Results**: Results are displayed in two columns
   - Words are sorted by length (longest first)
   - Words with 7+ letters are highlighted
   - Each column is independently scrollable

**Try this example** if you're not sure what to enter:
- Single tiles: `S C Y B N G`
- Horizontal tiles: `AL UR KI AT`
- Vertical tiles: `ME`

#### API Endpoints

The web server provides the following API endpoints:

- `GET /` - Serves the web interface
- `POST /api/solve` - Solves a Word Bites puzzle
  - Request body: JSON with tiles and configuration
  - Response: JSON with horizontal and vertical word lists
- `GET /api/health` - Health check endpoint
  - Returns server status and dictionary info

#### Architecture

The web interface maintains **modular separation** between components:

- **Frontend** ([static/](static/))
  - [index.html](static/index.html) - User interface
  - [style.css](static/style.css) - Styling
  - [script.js](static/script.js) - Client-side logic

- **Backend API Layer** ([app.py](app.py))
  - Flask web server
  - REST API endpoints
  - Thin wrapper over core solver logic

- **Core Solver** ([src/wordbiter/](src/wordbiter/))
  - [word_finder.py](src/wordbiter/word_finder.py) - Algorithm implementation
  - [dictionary.py](src/wordbiter/dictionary.py) - Dictionary management
  - No dependencies on web layer

This separation ensures the core solver remains reusable and testable independently of the web interface.

## Project Structure

```
wordbiter/
├── src/
│   └── wordbiter/           # Main package (core solver)
│       ├── __init__.py      # Package initialization
│       ├── main.py          # CLI interface
│       ├── word_finder.py   # Core solving algorithm
│       └── dictionary.py    # Dictionary loading utilities
├── static/                  # Web frontend
│   ├── index.html           # Web interface HTML
│   ├── style.css            # Styling
│   └── script.js            # Client-side JavaScript
├── tests/                   # Test suite
│   ├── test_find_all_words.py
│   ├── test_group_exclusion.py
│   ├── test_tile_views.py
│   └── test_word_bites.py
├── dictionaries/            # Word lists
│   ├── scrabble_words.txt
│   ├── words_alpha.txt
│   └── mit_words.txt
├── app.py                   # Flask web server
├── run.py                   # CLI entry point
├── run_tests.sh             # Test runner
├── setup.py                 # Package setup
├── requirements.txt         # Web dependencies
├── README.md                # This file
└── LICENSE                  # License information
```

## Examples

### Example 1: Quick Start Game

**Input:**
- Single tiles: `S C Y B N G`
- Horizontal tiles: `AL UR KI AT`
- Vertical tiles: `ME`

**Sample Results:**
- Long horizontal words: `CALKINGS`, `NATURALS`, `NATURAL`, `BALKING`, `URGENCY`
- Long vertical words: `BRACINGLY`, `GRAYBACKS`, `MEALYBUGS`, `MEGABUCKS`, `TUMESCING`

This is a great example to try if you're new to the solver!

### Example 2: Basic Game

**Input:**
- Single tiles: `A E T`
- Horizontal tiles: `RD`
- Vertical tiles: (none)

**Key Results:**
- Horizontal: `TRADE`, `TREAD`, `RATED`, `DATER`
- Vertical: `ART`, `EAR`, `TEA`, `RAT`

### Example 3: Complex Game

**Input:**
- Single tiles: `S I N`
- Horizontal tiles: `TA ER`
- Vertical tiles: `CO MP`

**Search Strategy:**
- Horizontal view: `[S, I, N, TA, E, R, C, O, M, P]`
- Vertical view: `[S, I, N, T, A, CO, E, R, MP]`

### Example 4: Vertical Words Only

```bash
python3 run.py --only-direction v
```

Searches only for vertical words, useful when you've already solved the horizontal direction.

## Development

### Running Tests

Run the test suite using the provided script:

```bash
./run_tests.sh
```

### Running Type Checks

If you have mypy installed:

```bash
mypy src/wordbiter/
```

### Code Organization

- **`word_finder.py`**: Core algorithm
  - `get_tile_views()`: Converts tiles to horizontal/vertical views
  - `find_all_words()`: Backtracking search with pruning
  - `solve_word_bites()`: Top-level API

- **`dictionary.py`**: Dictionary management
  - `load_dictionary()`: Loads and normalizes word lists

- **`main.py`**: Command-line interface
  - Argument parsing
  - User input handling
  - Result formatting

## Algorithm Details

### Tile View Transformation

Multi-letter tiles are handled by creating two separate views:

```python
Input:
  single: [A, E]
  horizontal: [RT]
  vertical: [CO]

Horizontal View:
  tiles: [A, E, RT, C, O]
  groups: [0, 1, 2, 3, 3]

Vertical View:
  tiles: [A, E, R, T, CO]
  groups: [0, 1, 2, 2, 3]
```

Group IDs track mutual exclusion - tiles with the same group ID cannot both be used in a single word.

### Search Optimization

The backtracking algorithm achieves high performance through:

1. **Prefix pruning**: Immediately abandons paths that don't form valid prefixes
2. **Length bounds**: Stops exploring when length limits are reached
3. **Group tracking**: Efficiently enforces the mutual exclusion rule
4. **Set operations**: Uses sets for O(1) dictionary and prefix lookups

## License

See [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please ensure:

- All tests pass (`./run_tests.sh`)
- Type annotations are correct (`mypy src/wordbiter/`)
- Code follows existing style conventions

## Troubleshooting

### "ModuleNotFoundError: No module named 'wordbiter'"

Use the provided runner scripts:
- `python3 run.py` for the main program
- `./run_tests.sh` for tests

### "Dictionary file not found"

The program defaults to `/usr/share/dict/words`. Use `--dictionary` to specify an alternative:

```bash
python3 run.py --dictionary dictionaries/scrabble_words.txt
```

### Performance Issues

If the solver is slow:
- Reduce `--max-horizontal-length` and `--max-vertical-length`
- Use a smaller dictionary
- Use `--only-direction` to search only one orientation
