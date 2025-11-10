"""
Unit tests to verify that group exclusion logic prevents using multiple letters
from the same source tile in a single word.
"""

from typing import List, Set
from word_finder import solve_word_bites


def test_horizontal_tile_letters_mutually_exclusive_in_vertical_words() -> None:
    """
    Test that when a horizontal tile like 'AB' is split into A and B for vertical words,
    both A and B cannot be used in the same vertical word.
    """
    # Create a dictionary with words that test the exclusion
    dictionary: Set[str] = {
        "BAT",    # Would need B + A + T (but B and A are from same tile "AB")
        "TAB",    # Would need T + A + B (but A and B are from same tile "AB")
        "BAD",    # Would need B + A + D (but B and A are from same tile "AB")
        "ABE",    # Would need A + B + E (but A and B are from same tile "AB")
        "BET",    # Valid: B (from AB) + E + T
        "ATE",    # Valid: A (from AB) + T + E
        "TED",    # Valid: T + E + D
        "BED",    # Valid: B (from AB) + E + D
    }

    single_tiles: List[str] = ["T", "E", "D"]
    horizontal_tiles: List[str] = ["AB"]
    vertical_tiles: List[str] = []

    results = solve_word_bites(single_tiles, horizontal_tiles, vertical_tiles, dictionary, min_length=3)

    vertical_words = results['vertical']

    # These words should NOT be in vertical results (require both A and B from AB tile)
    assert "BAT" not in vertical_words, "BAT should not be possible (needs both B and A from AB tile)"
    assert "TAB" not in vertical_words, "TAB should not be possible (needs both A and B from AB tile)"
    assert "BAD" not in vertical_words, "BAD should not be possible (needs both B and A from AB tile)"
    assert "ABE" not in vertical_words, "ABE should not be possible (needs both A and B from AB tile)"

    # These words SHOULD be possible (use only one letter from AB tile)
    assert "BET" in vertical_words, "BET should be possible (B from AB, E, T)"
    assert "ATE" in vertical_words, "ATE should be possible (A from AB, T, E)"
    assert "TED" in vertical_words, "TED should be possible (T, E, D)"
    assert "BED" in vertical_words, "BED should be possible (B from AB, E, D)"

    print("✓ test_horizontal_tile_letters_mutually_exclusive_in_vertical_words passed")


def test_vertical_tile_letters_mutually_exclusive_in_horizontal_words() -> None:
    """
    Test that when a vertical tile like 'XY' is split into X and Y for horizontal words,
    both X and Y cannot be used in the same horizontal word.
    """
    dictionary: Set[str] = {
        "XYZ",    # Would need X + Y + Z (but X and Y are from same tile "XY")
        "YAX",    # Would need Y + A + X (but Y and X are from same tile "XY")
        "WAX",    # Valid: W + A + X (from XY)
        "YAW",    # Valid: Y (from XY) + A + W
        "WAY",    # Valid: W + A + Y (from XY)
        "ZAX",    # Valid: Z + A + X (from XY)
    }

    single_tiles: List[str] = ["A", "W", "Z"]
    horizontal_tiles: List[str] = []
    vertical_tiles: List[str] = ["XY"]

    results = solve_word_bites(single_tiles, horizontal_tiles, vertical_tiles, dictionary, min_length=3)

    horizontal_words = results['horizontal']

    # These words should NOT be in horizontal results (require both X and Y from XY tile)
    assert "XYZ" not in horizontal_words, "XYZ should not be possible (needs both X and Y from XY tile)"
    assert "YAX" not in horizontal_words, "YAX should not be possible (needs both Y and X from XY tile)"

    # These words SHOULD be possible
    assert "WAX" in horizontal_words, "WAX should be possible (W, A, X from XY)"
    assert "YAW" in horizontal_words, "YAW should be possible (Y from XY, A, W)"
    assert "WAY" in horizontal_words, "WAY should be possible (W, A, Y from XY)"
    assert "ZAX" in horizontal_words, "ZAX should be possible (Z, A, X from XY)"

    print("✓ test_vertical_tile_letters_mutually_exclusive_in_horizontal_words passed")


def test_multiple_horizontal_tiles_exclusion() -> None:
    """
    Test that exclusion works correctly when there are multiple horizontal tiles.
    """
    dictionary: Set[str] = {
        "CAFE",   # C + A + F + E (valid if we have all as singles)
        "ACE",    # A + C + E (valid)
        "CAF",    # C + A + F (valid)
        "FEE",    # F + E + E (would need both E's from FE, not possible)
        "FEN",    # F + E + N (would need both F and E from FE if that's the source)
        "FAT",    # F (from FE) + A + T
        "EAT",    # E (from FE) + A + T
        "CAT",    # C + A + T
    }

    single_tiles: List[str] = ["A", "T", "N"]
    horizontal_tiles: List[str] = ["CA", "FE"]  # CA and FE are horizontal tiles
    vertical_tiles: List[str] = []

    results = solve_word_bites(single_tiles, horizontal_tiles, vertical_tiles, dictionary, min_length=3)

    vertical_words = results['vertical']

    # Cannot use both C and A from CA tile
    # Cannot use both F and E from FE tile
    assert "FEE" not in vertical_words, "FEE not possible (needs both F and E from FE)"

    # Can use one letter from each multi-letter tile
    assert "FAT" in vertical_words, "FAT should be possible (F from FE, A from CA, T)"
    assert "EAT" in vertical_words, "EAT should be possible (E from FE, A from CA, T)"
    assert "CAT" in vertical_words, "CAT should be possible (C from CA, A single, T)"

    print("✓ test_multiple_horizontal_tiles_exclusion passed")


def test_three_letter_tile_exclusion() -> None:
    """
    Test that all three letters from a 3-letter tile are mutually exclusive.
    """
    dictionary: Set[str] = {
        "DOG",    # Would need D + O + G (all from DOG tile, not possible)
        "GOD",    # Would need G + O + D (all from DOG tile, not possible)
        "DOT",    # D (from DOG) + O (from DOG) + T (not possible, D and O from same tile)
        "GOT",    # G (from DOG) + O (from DOG) + T (not possible, G and O from same tile)
        "DEN",    # D (from DOG) + E + N (valid)
        "ONE",    # O (from DOG) + N + E (valid)
        "GEN",    # G (from DOG) + E + N (valid)
        "TEN",    # T + E + N (valid, doesn't use DOG)
    }

    single_tiles: List[str] = ["E", "N", "T"]
    horizontal_tiles: List[str] = ["DOG"]
    vertical_tiles: List[str] = []

    results = solve_word_bites(single_tiles, horizontal_tiles, vertical_tiles, dictionary, min_length=3)

    vertical_words = results['vertical']

    # Cannot use any two letters from DOG together
    assert "DOG" not in vertical_words, "DOG not possible (all from same tile)"
    assert "GOD" not in vertical_words, "GOD not possible (all from same tile)"
    assert "DOT" not in vertical_words, "DOT not possible (D and O from same tile)"
    assert "GOT" not in vertical_words, "GOT not possible (G and O from same tile)"

    # Can use single letter from DOG
    assert "DEN" in vertical_words, "DEN should be possible (D from DOG, E, N)"
    assert "ONE" in vertical_words, "ONE should be possible (O from DOG, N, E)"
    assert "GEN" in vertical_words, "GEN should be possible (G from DOG, E, N)"
    assert "TEN" in vertical_words, "TEN should be possible (T, E, N)"

    print("✓ test_three_letter_tile_exclusion passed")


def test_horizontal_tiles_work_intact_in_horizontal_words() -> None:
    """
    Test that horizontal tiles can be used as complete units in horizontal words.
    """
    dictionary: Set[str] = {
        "CARTE",  # CA + R + TE
        "CATER",  # CA + TE + R
        "TECAR",  # TE + CA + R
    }

    single_tiles: List[str] = ["R"]
    horizontal_tiles: List[str] = ["CA", "TE"]
    vertical_tiles: List[str] = []

    results = solve_word_bites(single_tiles, horizontal_tiles, vertical_tiles, dictionary, min_length=3)

    horizontal_words = results['horizontal']

    # In horizontal view, CA and TE are used as complete tiles
    # Available tiles: R (group 0), CA (group 1), TE (group 2)
    assert "CARTE" in horizontal_words, "CARTE should work with CA + R + TE"
    assert "CATER" in horizontal_words, "CATER should work with CA + TE + R"
    assert "TECAR" in horizontal_words, "TECAR should work with TE + CA + R"

    print("✓ test_horizontal_tiles_work_intact_in_horizontal_words passed")


def test_vertical_tiles_work_intact_in_vertical_words() -> None:
    """
    Test that vertical tiles can be used as complete units in vertical words.
    """
    dictionary: Set[str] = {
        "MUST",   # M + U + ST
        "MIST",   # M + IS + T (but T is not available as single - can't form this)
        "RUST",   # R + U + ST
        "RISUM",  # R + IS + U + M
        "STRUM",  # ST + R + U + M
    }

    single_tiles: List[str] = ["M", "U", "R"]
    horizontal_tiles: List[str] = []
    vertical_tiles: List[str] = ["IS", "ST"]

    results = solve_word_bites(single_tiles, horizontal_tiles, vertical_tiles, dictionary, min_length=3)

    vertical_words = results['vertical']

    # In vertical view, IS and ST are used as complete tiles
    # Available: M (group 0), U (group 1), R (group 2), IS (group 3), ST (group 4)
    assert "MUST" in vertical_words, "MUST should work with M + U + ST tile"
    assert "RUST" in vertical_words, "RUST should work with R + U + ST tile"
    assert "RISUM" in vertical_words, "RISUM should work with R + IS + U + M"
    assert "STRUM" in vertical_words, "STRUM should work with ST + R + U + M"

    # This should NOT work because we don't have a single T
    assert "MIST" not in vertical_words, "MIST should not work (no single T available)"

    print("✓ test_vertical_tiles_work_intact_in_vertical_words passed")


def test_mixed_orientation_independence() -> None:
    """
    Test that horizontal and vertical word searches are independent.
    A tile that's horizontal doesn't affect horizontal word formation.
    """
    dictionary: Set[str] = {
        "TEACH",  # TE + A + C + H
        "REACH",  # R + E + A + C + H
        "REACT",  # R + E + A + C + T
    }

    single_tiles: List[str] = ["R", "A", "C", "H"]
    horizontal_tiles: List[str] = ["TE"]
    vertical_tiles: List[str] = []

    results = solve_word_bites(single_tiles, horizontal_tiles, vertical_tiles, dictionary, min_length=3)

    horizontal_words = results['horizontal']

    # In horizontal view, TE is used as a complete tile
    assert "TEACH" in horizontal_words, "TEACH should work with TE + A + C + H"

    # Note: REACH and REACT need individual E, which isn't available in horizontal view
    # because TE is kept as a unit in horizontal view

    print("✓ test_mixed_orientation_independence passed")


def run_all_tests() -> None:
    """Run all group exclusion tests."""
    print("=" * 50)
    print("Running Group Exclusion Tests")
    print("=" * 50)
    print()

    test_horizontal_tile_letters_mutually_exclusive_in_vertical_words()
    test_vertical_tile_letters_mutually_exclusive_in_horizontal_words()
    test_multiple_horizontal_tiles_exclusion()
    test_three_letter_tile_exclusion()
    test_horizontal_tiles_work_intact_in_horizontal_words()
    test_vertical_tiles_work_intact_in_vertical_words()
    test_mixed_orientation_independence()

    print()
    print("=" * 50)
    print("All group exclusion tests passed!")
    print("=" * 50)


if __name__ == "__main__":
    run_all_tests()
