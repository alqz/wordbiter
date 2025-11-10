"""
Word Bites AI - Milestone 1
Given a set of tiles (each containing one or more letters), find all valid words.
"""

import argparse
from typing import List
from .dictionary import load_dictionary
from .word_finder import solve_word_bites

# Constants
SEPARATOR_WIDTH = 50
DEFAULT_DISPLAY_LIMIT = 30
DEFAULT_MIN_WORD_LENGTH = 3


def display_words(words: List[str], title: str, max_display: int = DEFAULT_DISPLAY_LIMIT) -> None:
    """
    Display a list of words with a title and count.

    Args:
        words: List of words to display (should be pre-sorted)
        title: Title to display above the words
        max_display: Maximum number of words to display (default: DEFAULT_DISPLAY_LIMIT)
    """
    print("\n" + "=" * SEPARATOR_WIDTH)
    print(title)
    print("=" * SEPARATOR_WIDTH)
    top_words = words[:max_display]
    print(f"Showing top {len(top_words)} longest words (out of {len(words)} total):\n")
    if top_words:
        for word in top_words:
            print(f"  {word}")
    else:
        print("  No valid words found.")


def main() -> None:
    """Main function for manual input of game state."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Word Bites AI - Find words from tiles")
    parser.add_argument(
        "--max-horizontal-length",
        type=int,
        default=8,
        help="Maximum horizontal word length (default: 8)"
    )
    parser.add_argument(
        "--max-vertical-length",
        type=int,
        default=9,
        help="Maximum vertical word length (default: 9)"
    )
    parser.add_argument(
        "--only-direction",
        type=str,
        choices=["h", "v"],
        default=None,
        help="Only find words in one direction: 'h' for horizontal only, 'v' for vertical only (default: both directions)"
    )
    parser.add_argument(
        "--dictionary",
        type=str,
        default="/usr/share/dict/words",
        help="Path to list of words"
    )
    args = parser.parse_args()

    print("=" * SEPARATOR_WIDTH)
    print("Word Bites AI - Milestone 1")
    print("=" * SEPARATOR_WIDTH)

    # Load dictionary
    print("\nLoading dictionary...")
    dictionary = load_dictionary(args.dictionary)
    print(f"Loaded {len(dictionary)} words")

    # Get tiles from user
    print("\n" + "-" * SEPARATOR_WIDTH)
    print("Enter single-letter tiles (space-separated, or leave blank):")
    single_input = input("Single tiles: ").strip()
    single_tiles: List[str] = [tile.upper() for tile in single_input.split()]

    print("\nEnter horizontal multi-letter tiles (space-separated, or leave blank):")
    horizontal_input = input("Horizontal tiles: ").strip()
    horizontal_tiles: List[str] = [tile.upper() for tile in horizontal_input.split()]

    print("\nEnter vertical multi-letter tiles (space-separated, or leave blank):")
    vertical_input = input("Vertical tiles: ").strip()
    vertical_tiles: List[str] = [tile.upper() for tile in vertical_input.split()]

    # Display configuration
    print("\nConfiguration:")
    print(f"  Max horizontal length: {args.max_horizontal_length}")
    print(f"  Max vertical length: {args.max_vertical_length}")
    if args.only_direction:
        direction_name = "horizontal" if args.only_direction == "h" else "vertical"
        print(f"  Direction: {direction_name} only")
    else:
        print(f"  Direction: both")

    # Find all valid words
    print("\nSearching for words...")
    results = solve_word_bites(
        single_tiles,
        horizontal_tiles,
        vertical_tiles,
        dictionary,
        min_length=DEFAULT_MIN_WORD_LENGTH,
        max_horizontal_length=args.max_horizontal_length,
        max_vertical_length=args.max_vertical_length
    )

    # Display results
    if args.only_direction != "v":  # Show horizontal if not vertical-only
        display_words(results['horizontal'], f"HORIZONTAL WORDS (Top {DEFAULT_DISPLAY_LIMIT} Longest)")

    if args.only_direction != "h":  # Show vertical if not horizontal-only
        display_words(results['vertical'], f"VERTICAL WORDS (Top {DEFAULT_DISPLAY_LIMIT} Longest)")

    print()


if __name__ == "__main__":
    main()
