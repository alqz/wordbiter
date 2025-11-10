"""
Tests for the get_tile_views function.
"""

from word_finder import get_tile_views


def test_only_single_tiles() -> None:
    """Test with only single-letter tiles."""
    single_tiles = ["A", "E", "C"]
    horizontal_tiles = []
    vertical_tiles = []

    result = get_tile_views(single_tiles, horizontal_tiles, vertical_tiles)

    h_tiles, h_groups = result['horizontal']
    v_tiles, v_groups = result['vertical']

    assert h_tiles == ["A", "E", "C"]
    assert v_tiles == ["A", "E", "C"]
    assert h_groups == [0, 1, 2]
    assert v_groups == [0, 1, 2]
    print("✓ test_only_single_tiles passed")


def test_only_horizontal_tiles() -> None:
    """Test with only horizontal tiles."""
    single_tiles = []
    horizontal_tiles = ["TE", "FL"]
    vertical_tiles = []

    result = get_tile_views(single_tiles, horizontal_tiles, vertical_tiles)

    h_tiles, h_groups = result['horizontal']
    v_tiles, v_groups = result['vertical']

    assert h_tiles == ["TE", "FL"]
    assert v_tiles == ["T", "E", "F", "L"]
    # Horizontal view: each tile has its own group
    assert h_groups == [0, 1]
    # Vertical view: T and E share group 0, F and L share group 1
    assert v_groups == [0, 0, 1, 1]
    print("✓ test_only_horizontal_tiles passed")


def test_only_vertical_tiles() -> None:
    """Test with only vertical tiles."""
    single_tiles = []
    horizontal_tiles = []
    vertical_tiles = ["UB", "IS"]

    result = get_tile_views(single_tiles, horizontal_tiles, vertical_tiles)

    h_tiles, h_groups = result['horizontal']
    v_tiles, v_groups = result['vertical']

    assert h_tiles == ["U", "B", "I", "S"]
    assert v_tiles == ["UB", "IS"]
    # Horizontal view: U and B share group 0, I and S share group 1
    assert h_groups == [0, 0, 1, 1]
    # Vertical view: each tile has its own group
    assert v_groups == [0, 1]
    print("✓ test_only_vertical_tiles passed")


def test_mixed_tiles() -> None:
    """Test with a mix of all tile types."""
    single_tiles = ["A", "E", "C"]
    horizontal_tiles = ["TE", "FL"]
    vertical_tiles = ["UB", "IS"]

    result = get_tile_views(single_tiles, horizontal_tiles, vertical_tiles)

    h_tiles, h_groups = result['horizontal']
    v_tiles, v_groups = result['vertical']

    # Horizontal view: single tiles + horizontal tiles (intact) + vertical tiles (split)
    assert h_tiles == ["A", "E", "C", "TE", "FL", "U", "B", "I", "S"]
    # Groups: singles are 0,1,2; horizontal tiles are 3,4; vertical tiles split are 5,5,6,6
    assert h_groups == [0, 1, 2, 3, 4, 5, 5, 6, 6]

    # Vertical view: single tiles + horizontal tiles (split) + vertical tiles (intact)
    assert v_tiles == ["A", "E", "C", "T", "E", "F", "L", "UB", "IS"]
    # Groups: singles are 0,1,2; horizontal tiles split are 3,3,4,4; vertical tiles are 5,6
    assert v_groups == [0, 1, 2, 3, 3, 4, 4, 5, 6]
    print("✓ test_mixed_tiles passed")


def test_empty_tiles() -> None:
    """Test with all empty lists."""
    single_tiles = []
    horizontal_tiles = []
    vertical_tiles = []

    result = get_tile_views(single_tiles, horizontal_tiles, vertical_tiles)

    h_tiles, h_groups = result['horizontal']
    v_tiles, v_groups = result['vertical']

    assert h_tiles == []
    assert v_tiles == []
    assert h_groups == []
    assert v_groups == []
    print("✓ test_empty_tiles passed")


def test_three_letter_tiles() -> None:
    """Test with multi-letter tiles (3+ letters)."""
    single_tiles = []
    horizontal_tiles = ["ABC"]
    vertical_tiles = ["XYZ"]

    result = get_tile_views(single_tiles, horizontal_tiles, vertical_tiles)

    h_tiles, h_groups = result['horizontal']
    v_tiles, v_groups = result['vertical']

    assert h_tiles == ["ABC", "X", "Y", "Z"]
    assert v_tiles == ["A", "B", "C", "XYZ"]
    # Horizontal view: ABC is group 0, X/Y/Z (from XYZ tile) all share group 1
    assert h_groups == [0, 1, 1, 1]
    # Vertical view: A/B/C (from ABC tile) all share group 0, XYZ is group 1
    assert v_groups == [0, 0, 0, 1]
    print("✓ test_three_letter_tiles passed")


def test_real_game_scenario() -> None:
    """Test with a realistic game scenario."""
    single_tiles = ["E", "V", "N", "Y", "R", "A", "C", "H"]
    horizontal_tiles = ["UB", "TE", "FL", "IS"]
    vertical_tiles = []

    result = get_tile_views(single_tiles, horizontal_tiles, vertical_tiles)

    h_tiles, h_groups = result['horizontal']
    v_tiles, v_groups = result['vertical']

    # Horizontal view
    expected_horizontal = ["E", "V", "N", "Y", "R", "A", "C", "H", "UB", "TE", "FL", "IS"]
    assert h_tiles == expected_horizontal
    # Groups: singles are 0-7, horizontal tiles are 8-11
    assert h_groups == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    # Vertical view
    expected_vertical = ["E", "V", "N", "Y", "R", "A", "C", "H", "U", "B", "T", "E", "F", "L", "I", "S"]
    assert v_tiles == expected_vertical
    # Groups: singles are 0-7, UB split is 8,8, TE split is 9,9, FL split is 10,10, IS split is 11,11
    assert v_groups == [0, 1, 2, 3, 4, 5, 6, 7, 8, 8, 9, 9, 10, 10, 11, 11]
    print("✓ test_real_game_scenario passed")


def run_all_tests() -> None:
    """Run all tests."""
    print("=" * 50)
    print("Running get_tile_views tests")
    print("=" * 50)
    print()

    test_only_single_tiles()
    test_only_horizontal_tiles()
    test_only_vertical_tiles()
    test_mixed_tiles()
    test_empty_tiles()
    test_three_letter_tiles()
    test_real_game_scenario()

    print()
    print("=" * 50)
    print("All tests passed!")
    print("=" * 50)


if __name__ == "__main__":
    run_all_tests()
