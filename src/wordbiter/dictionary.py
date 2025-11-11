"""
Dictionary loading utilities for Word Bites.
"""

from typing import Set

# Minimum word length to include in dictionary
MIN_WORD_LENGTH = 3


def load_dictionary(file_path: str = "/usr/share/dict/words") -> Set[str]:
    """Load dictionary words from a file."""
    try:
        with open(file_path, 'r') as f:
            # Convert to uppercase and filter by minimum length
            words: Set[str] = {
                stripped.upper()
                for line in f
                if len(stripped := line.strip()) >= MIN_WORD_LENGTH
            }
        return words
    except FileNotFoundError:
        print(f"Dictionary file not found at {file_path}")
        print("Using a small sample dictionary for testing...")
        # Small sample dictionary for testing
        sample_dict: Set[str] = {
            "CAT", "CATS", "SAT", "HAT", "HATS", "THE", "THAT", "THIS",
            "BAT", "BATS", "RAT", "RATS", "MAT", "MATS", "ATE", "EAT",
            "TEA", "SET", "SIT", "HIT", "HITS"
        }
        return sample_dict
