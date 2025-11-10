"""
Word Bites AI - Milestone 1
Given a set of tiles (each containing one or more letters), find all valid words.
"""

import argparse
from typing import List
from dictionary import load_dictionary
from word_finder import solve_word_bites


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
    args = parser.parse_args()

    print("=" * 50)
    print("Word Bites AI - Milestone 1")
    print("=" * 50)

    # Load dictionary
    print("\nLoading dictionary...")
    dictionary = load_dictionary()
    print(f"Loaded {len(dictionary)} words")

    # Get tiles from user
    print("\n" + "-" * 50)
    print("Enter single-letter tiles (comma-separated, or leave blank):")
    single_input = input("Single tiles: ").strip()
    single_tiles: List[str] = [tile.strip().upper() for tile in single_input.split(',') if tile.strip()]

    print("\nEnter horizontal multi-letter tiles (comma-separated, or leave blank):")
    horizontal_input = input("Horizontal tiles: ").strip()
    horizontal_tiles: List[str] = [tile.strip().upper() for tile in horizontal_input.split(',') if tile.strip()]

    print("\nEnter vertical multi-letter tiles (comma-separated, or leave blank):")
    vertical_input = input("Vertical tiles: ").strip()
    vertical_tiles: List[str] = [tile.strip().upper() for tile in vertical_input.split(',') if tile.strip()]

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
        min_length=3,
        max_horizontal_length=args.max_horizontal_length,
        max_vertical_length=args.max_vertical_length
    )

    # Display horizontal words (top 30 longest)
    if args.only_direction != "v":  # Show if not vertical-only
        print("\n" + "=" * 50)
        print("HORIZONTAL WORDS (Top 30 Longest)")
        print("=" * 50)
        horizontal_words = results['horizontal']
        top_horizontal = horizontal_words[:30]
        print(f"Showing top {len(top_horizontal)} longest words (out of {len(horizontal_words)} total):\n")
        if top_horizontal:
            for word in top_horizontal:
                print(f"  {word}")
        else:
            print("  No valid words found.")

    # Display vertical words (top 30 longest)
    if args.only_direction != "h":  # Show if not horizontal-only
        print("\n" + "=" * 50)
        print("VERTICAL WORDS (Top 30 Longest)")
        print("=" * 50)
        vertical_words = results['vertical']
        top_vertical = vertical_words[:30]
        print(f"Showing top {len(top_vertical)} longest words (out of {len(vertical_words)} total):\n")
        if top_vertical:
            for word in top_vertical:
                print(f"  {word}")
        else:
            print("  No valid words found.")

    print()


if __name__ == "__main__":
    main()
