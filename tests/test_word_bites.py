"""
Test cases for Word Bites AI.
"""

from typing import Dict, List
from wordbiter.dictionary import load_dictionary
from wordbiter.word_finder import solve_word_bites


def test_word_bites() -> None:
    """Test case with specific tiles."""
    print("=" * 50)
    print("Word Bites AI - Test Case")
    print("=" * 50)

    # Load dictionary
    print("\nLoading dictionary...")
    dictionary = load_dictionary()
    print(f"Loaded {len(dictionary)} words")

    # Test tiles - separating by orientation
    single_tiles: List[str] = ["E", "V", "N", "Y", "R", "A", "C", "H"]
    horizontal_tiles: List[str] = ["UB", "TE", "FL"]
    vertical_tiles: List[str] = ["IS"]

    print(f"\nSingle tiles: {single_tiles}")
    print(f"Horizontal tiles: {horizontal_tiles}")
    print(f"Vertical tiles: {vertical_tiles}")

    # Find all valid words
    print("\nSearching for words...")
    results = solve_word_bites(single_tiles, horizontal_tiles, vertical_tiles, dictionary, min_length=3)

    # Helper function to display top 30 longest words grouped by length
    def display_words(words: List[str], title: str) -> None:
        print("\n" + "=" * 50)
        print(title)
        print("=" * 50)

        # Get top 30 longest words
        top_words = words[:30]

        if top_words:
            # Group by length for better readability
            by_length: Dict[int, List[str]] = {}
            for word in top_words:
                length = len(word)
                if length not in by_length:
                    by_length[length] = []
                by_length[length].append(word)

            print(f"Showing top {len(top_words)} longest words (out of {len(words)} total):\n")

            # Sort from longest to shortest
            for length in sorted(by_length.keys(), reverse=True):
                print(f"{length}-letter words ({len(by_length[length])}):")
                for word in by_length[length]:
                    print(f"  {word}")
                print()
        else:
            print(f"  No valid words found.")

    # Display horizontal words
    display_words(results['horizontal'], "HORIZONTAL WORDS")

    # Display vertical words
    display_words(results['vertical'], "VERTICAL WORDS")

    print()


if __name__ == "__main__":
    test_word_bites()
