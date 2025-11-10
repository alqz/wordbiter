# Word Bites AI Solver

A Python-based solver for the Word Bites word puzzle game that finds all valid words that can be formed from a given set of letter tiles.

## Table of Contents

- [About Word Bites](#about-word-bites)
- [Game Rules](#game-rules)
- [How This Solver Works](#how-this-solver-works)
- [Installation](#installation)
- [Usage](#usage)
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
- Standard library only (no external dependencies required)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd wordbiter
```

2. (Optional) Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. The solver is ready to use! No additional installation needed.

For development with type checking, install optional dependencies:
```bash
pip install mypy pytest
```

## Usage

### Interactive Mode

Run the solver interactively to input your game tiles:

```bash
python3 run.py
```

### Command-Line Options

```bash
python3 run.py [OPTIONS]
```

**Available options:**

- `--max-horizontal-length N`: Set maximum horizontal word length (default: 8)
- `--max-vertical-length N`: Set maximum vertical word length (default: 9)
- `--only-direction h|v`: Find words in only one direction
  - `h`: Horizontal words only
  - `v`: Vertical words only
- `--dictionary PATH`: Use a custom dictionary file (default: `/usr/share/dict/words`)

### Example Session

```
==================================================
Word Bites AI - Milestone 1
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

### Using Custom Dictionaries

The project includes several dictionary files in the `dictionaries/` directory:

```bash
# Use Scrabble dictionary
python3 run.py --dictionary dictionaries/scrabble_words.txt

# Use MIT words
python3 run.py --dictionary dictionaries/mit_words.txt

# Use alpha words
python3 run.py --dictionary dictionaries/words_alpha.txt
```

## Project Structure

```
wordbiter/
├── src/
│   └── wordbiter/           # Main package
│       ├── __init__.py      # Package initialization
│       ├── main.py          # CLI interface
│       ├── word_finder.py   # Core solving algorithm
│       └── dictionary.py    # Dictionary loading utilities
├── tests/                   # Test suite
│   ├── test_find_all_words.py
│   ├── test_group_exclusion.py
│   ├── test_tile_views.py
│   └── test_word_bites.py
├── dictionaries/            # Word lists
│   ├── scrabble_words.txt
│   ├── words_alpha.txt
│   └── mit_words.txt
├── run.py                   # Entry point script
├── run_tests.sh             # Test runner
├── setup.py                 # Package setup
├── README.md                # This file
└── LICENSE                  # License information
```

## Examples

### Example 1: Basic Game

**Input:**
- Single tiles: `A, E, T`
- Horizontal tiles: `RD`
- Vertical tiles: (none)

**Key Results:**
- Horizontal: `TRADE`, `TREAD`, `RATED`, `DATER`
- Vertical: `ART`, `EAR`, `TEA`, `RAT`

### Example 2: Complex Game

**Input:**
- Single tiles: `S, I, N`
- Horizontal tiles: `TA, ER`
- Vertical tiles: `CO, MP`

**Search Strategy:**
- Horizontal view: `[S, I, N, TA, E, R, C, O, M, P]`
- Vertical view: `[S, I, N, T, A, CO, E, R, MP]`

### Example 3: Vertical Words Only

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
