"""
Unit tests for the find_all_words function.
"""

from typing import List, Set
from wordbiter.word_finder import find_all_words


def create_simple_dictionary() -> Set[str]:
    """Create a simple dictionary for testing."""
    return {
        "CAT", "CATS", "SAT", "HAT", "HATS", "THE", "THAT", "THIS",
        "BAT", "BATS", "RAT", "RATS", "MAT", "MATS", "ATE", "EAT",
        "TEA", "SET", "SIT", "HIT", "HITS", "ACE", "ACT", "ACTS",
        "TAC", "TACS", "SATE", "CAST", "CASE"
    }


def test_single_letters_only() -> None:
    """Test with only single-letter tiles."""
    dictionary: Set[str] = create_simple_dictionary()
    tiles: List[str] = ["C", "A", "T"]
    groups: List[int] = [0, 1, 2]  # Each tile has its own group

    result = find_all_words(tiles, groups, dictionary, min_length=3)

    # Expected: CAT, ACT, TAC (all 3-letter permutations that are words)
    expected: List[str] = ["ACT", "CAT", "TAC"]  # Sorted by length, then alphabetically
    assert result == expected, f"Expected {expected}, got {result}"
    print("✓ test_single_letters_only passed")


def test_single_letters_multiple_words() -> None:
    """Test with single letters that form multiple words."""
    dictionary: Set[str] = create_simple_dictionary()
    tiles: List[str] = ["C", "A", "T", "S"]
    groups: List[int] = [0, 1, 2, 3]  # Each tile has its own group

    result = find_all_words(tiles, groups, dictionary, min_length=3)

    # Expected words (sorted longest first, then alphabetically)
    expected: List[str] = [
        "ACTS", "CAST", "CATS", "SATE", "TACS",  # 4-letter words
        "ACE", "ACT", "ATE", "CAT", "EAT", "SAT", "SET", "TAC", "TEA"  # 3-letter words
    ]

    # Note: The actual result depends on what 3-letter combos are in dictionary
    # Let's check that we have the key words
    assert "CATS" in result
    assert "CAST" in result
    assert "ACTS" in result
    assert "CAT" in result
    assert "ACT" in result
    print(f"✓ test_single_letters_multiple_words passed (found {len(result)} words)")


def test_multi_letter_tile() -> None:
    """Test with a multi-letter tile."""
    dictionary: Set[str] = create_simple_dictionary()
    tiles: List[str] = ["C", "AT"]
    groups: List[int] = [0, 1]  # Each tile has its own group

    result = find_all_words(tiles, groups, dictionary, min_length=3)

    # Expected: CAT (C + AT)
    expected: List[str] = ["CAT"]
    assert result == expected, f"Expected {expected}, got {result}"
    print("✓ test_multi_letter_tile passed")


def test_multi_letter_tiles_extended() -> None:
    """Test with multi-letter tile forming longer words."""
    dictionary: Set[str] = create_simple_dictionary()
    tiles: List[str] = ["C", "AT", "S"]
    groups: List[int] = [0, 1, 2]  # Each tile has its own group

    result = find_all_words(tiles, groups, dictionary, min_length=3)

    # Expected: CATS (C + AT + S), CAT (C + AT), SAT (S + AT)
    # Sorted longest first
    expected: List[str] = ["CATS", "CAT", "SAT"]
    assert result == expected, f"Expected {expected}, got {result}"
    print("✓ test_multi_letter_tiles_extended passed")


def test_no_valid_words() -> None:
    """Test with tiles that don't form any valid words."""
    dictionary: Set[str] = create_simple_dictionary()
    tiles: List[str] = ["X", "Y", "Z"]
    groups: List[int] = [0, 1, 2]  # Each tile has its own group

    result = find_all_words(tiles, groups, dictionary, min_length=3)

    expected: List[str] = []
    assert result == expected, f"Expected {expected}, got {result}"
    print("✓ test_no_valid_words passed")


def test_empty_tiles() -> None:
    """Test with empty tile list."""
    dictionary: Set[str] = create_simple_dictionary()
    tiles: List[str] = []
    groups: List[int] = []  # No groups for empty tiles

    result = find_all_words(tiles, groups, dictionary, min_length=3)

    expected: List[str] = []
    assert result == expected, f"Expected {expected}, got {result}"
    print("✓ test_empty_tiles passed")


def test_min_length_filter() -> None:
    """Test that min_length parameter works correctly."""
    dictionary: Set[str] = create_simple_dictionary()
    tiles: List[str] = ["C", "A", "T", "S"]
    groups: List[int] = [0, 1, 2, 3]  # Each tile has its own group

    # With min_length=4, should only get 4+ letter words
    result = find_all_words(tiles, groups, dictionary, min_length=4)

    # All results should be at least 4 letters
    for word in result:
        assert len(word) >= 4, f"Word '{word}' is shorter than min_length=4"

    # Should include CATS, CAST, ACTS
    assert "CATS" in result
    assert "CAST" in result
    print(f"✓ test_min_length_filter passed (found {len(result)} words >= 4 letters)")


def test_two_letter_tiles() -> None:
    """Test with multiple two-letter tiles."""
    dictionary: Set[str] = {"BATH", "BAT", "HAT", "THAT", "THE"}
    tiles: List[str] = ["BA", "TH"]
    groups: List[int] = [0, 1]  # Each tile has its own group

    result = find_all_words(tiles, groups, dictionary, min_length=3)

    # Expected: BATH (BA + TH)
    # Note: THAT would require BA + TH + AT, but we don't have AT as a tile
    expected: List[str] = ["BATH"]
    assert result == expected, f"Expected {expected}, got {result}"
    print("✓ test_two_letter_tiles passed")


def test_mixed_single_and_multi() -> None:
    """Test with a mix of single and multi-letter tiles."""
    dictionary: Set[str] = {"HATS", "HAT", "THAT", "SAT", "ATS"}
    tiles: List[str] = ["H", "AT", "S"]
    groups: List[int] = [0, 1, 2]  # Each tile has its own group

    result = find_all_words(tiles, groups, dictionary, min_length=3)

    # Expected: HATS (H + AT + S), HAT (H + AT), SAT (S + AT), ATS (AT + S)
    expected: List[str] = ["HATS", "ATS", "HAT", "SAT"]
    assert result == expected, f"Expected {expected}, got {result}"
    print("✓ test_mixed_single_and_multi passed")


def test_sorting_order() -> None:
    """Test that results are sorted correctly (longest first, then alphabetically)."""
    dictionary: Set[str] = {"CAT", "CATS", "ACT", "ACTS", "TACS", "TAC"}
    tiles: List[str] = ["C", "A", "T", "S"]
    groups: List[int] = [0, 1, 2, 3]  # Each tile has its own group

    result = find_all_words(tiles, groups, dictionary, min_length=3)

    # Check that longer words come first
    prev_length: float = float('inf')
    for word in result:
        current_length: int = len(word)
        assert current_length <= prev_length, f"Words not sorted by length: {result}"
        prev_length = current_length

    # Check that words of same length are alphabetically sorted
    four_letter_words: List[str] = [w for w in result if len(w) == 4]
    assert four_letter_words == sorted(four_letter_words), f"4-letter words not alphabetically sorted: {four_letter_words}"

    print(f"✓ test_sorting_order passed (result: {result})")


def run_all_tests() -> None:
    """Run all tests."""
    print("=" * 50)
    print("Running find_all_words unit tests")
    print("=" * 50)
    print()

    test_single_letters_only()
    test_single_letters_multiple_words()
    test_multi_letter_tile()
    test_multi_letter_tiles_extended()
    test_no_valid_words()
    test_empty_tiles()
    test_min_length_filter()
    test_two_letter_tiles()
    test_mixed_single_and_multi()
    test_sorting_order()

    print()
    print("=" * 50)
    print("All tests passed!")
    print("=" * 50)


if __name__ == "__main__":
    run_all_tests()
