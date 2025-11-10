"""
Core word-finding algorithm for Word Bites AI.
"""

from typing import Dict, List, Set, Tuple


def build_prefix_set(dictionary: Set[str]) -> Set[str]:
    """
    Build a set of all prefixes from the dictionary for efficient pruning.

    Args:
        dictionary: Set of valid dictionary words (uppercase)

    Returns:
        Set of all prefixes that exist in the dictionary
    """
    prefixes: Set[str] = set()
    for word in dictionary:
        for i in range(1, len(word) + 1):
            prefixes.add(word[:i])
    return prefixes


def get_tile_views(
    single_tiles: List[str],
    horizontal_tiles: List[str],
    vertical_tiles: List[str]
) -> Dict[str, Tuple[List[str], List[int]]]:
    """
    Generate horizontal and vertical views of tiles based on their orientations.

    Args:
        single_tiles: List of single-letter tiles (work the same in both orientations)
        horizontal_tiles: List of multi-letter tiles oriented horizontally (2+ letters each)
        vertical_tiles: List of multi-letter tiles oriented vertically (2+ letters each)

    Returns:
        Dictionary with 'horizontal' and 'vertical' keys, each containing:
        - List of tiles (strings) as they appear in that orientation
        - List of group IDs (ints) where tiles with the same group ID are mutually exclusive
    """
    horizontal_view: List[str] = []
    horizontal_groups: List[int] = []
    vertical_view: List[str] = []
    vertical_groups: List[int] = []

    group_id = 0

    # Single-letter tiles appear the same in both views
    for tile in single_tiles:
        horizontal_view.append(tile)
        horizontal_groups.append(group_id)
        vertical_view.append(tile)
        vertical_groups.append(group_id)
        group_id += 1

    # Horizontal tiles: used as multi-letter tiles in horizontal view,
    # split into individual letters in vertical view (but same group)
    for tile in horizontal_tiles:
        # In horizontal view: one multi-letter tile
        horizontal_view.append(tile)
        horizontal_groups.append(group_id)

        # In vertical view: split into individual letters, all with same group ID
        for letter in tile:
            vertical_view.append(letter)
            vertical_groups.append(group_id)

        group_id += 1

    # Vertical tiles: split into individual letters in horizontal view (same group),
    # used as multi-letter tiles in vertical view
    for tile in vertical_tiles:
        # In horizontal view: split into individual letters, all with same group ID
        for letter in tile:
            horizontal_view.append(letter)
            horizontal_groups.append(group_id)

        # In vertical view: one multi-letter tile
        vertical_view.append(tile)
        vertical_groups.append(group_id)

        group_id += 1

    return {
        'horizontal': (horizontal_view, horizontal_groups),
        'vertical': (vertical_view, vertical_groups)
    }


def find_all_words(
    tiles: List[str],
    groups: List[int],
    dictionary: Set[str],
    prefixes: Set[str],
    min_length: int = 3,
    max_length: int = 9
) -> List[str]:
    """
    Find all valid words that can be formed from the given tiles.
    Uses backtracking with prefix pruning for efficiency.

    Args:
        tiles: List of tiles, where each tile contains one or more letters
        groups: List of group IDs where tiles with the same ID are mutually exclusive
        dictionary: Set of valid dictionary words (uppercase)
        prefixes: Set of all valid prefixes from dictionary (for pruning)
        min_length: Minimum word length (default: 3)
        max_length: Maximum word length (default: 9)

    Returns:
        Sorted list of all valid words found
    """
    # Validate inputs
    if len(tiles) != len(groups):
        raise ValueError(f"tiles and groups must have same length: {len(tiles)} != {len(groups)}")
    if min_length < 1:
        raise ValueError(f"min_length must be >= 1, got {min_length}")
    if max_length < min_length:
        raise ValueError(f"max_length ({max_length}) must be >= min_length ({min_length})")

    # Uppercase all tiles once at the start
    tiles_upper = [tile.upper() for tile in tiles]

    valid_words: Set[str] = set()

    def backtrack(current_word: str, used_indices: Set[int], used_groups: Set[int]) -> None:
        """Recursively build words using available tiles."""
        # Prune: if current word is too long, stop
        if len(current_word) > max_length:
            return

        # Prune: if current word is not a prefix of any dictionary word, stop
        if current_word and current_word not in prefixes:
            return

        # Check if current word is valid
        if len(current_word) >= min_length and current_word in dictionary:
            valid_words.add(current_word)

        # Try adding each unused tile
        for i in range(len(tiles_upper)):
            tile_group = groups[i]
            # Can only use this tile if we haven't used its index or any tile from its group
            if i not in used_indices and tile_group not in used_groups:
                new_word = current_word + tiles_upper[i]
                new_used_indices = used_indices | {i}
                new_used_groups = used_groups | {tile_group}
                backtrack(new_word, new_used_indices, new_used_groups)

    # Start backtracking from empty word
    backtrack("", set(), set())

    # Sort by length (longest first), then alphabetically
    return sorted(valid_words, key=lambda w: (-len(w), w))


def solve_word_bites(
    single_tiles: List[str],
    horizontal_tiles: List[str],
    vertical_tiles: List[str],
    dictionary: Set[str],
    min_length: int = 3,
    max_horizontal_length: int = 8,
    max_vertical_length: int = 9
) -> Dict[str, List[str]]:
    """
    Top-level API to solve Word Bites puzzle.

    Args:
        single_tiles: List of single-letter tiles
        horizontal_tiles: List of multi-letter tiles oriented horizontally
        vertical_tiles: List of multi-letter tiles oriented vertically
        dictionary: Set of valid dictionary words (uppercase)
        min_length: Minimum word length (default: 3)
        max_horizontal_length: Maximum horizontal word length (default: 8)
        max_vertical_length: Maximum vertical word length (default: 9)

    Returns:
        Dictionary with 'horizontal' and 'vertical' keys, each containing a list of valid words
    """
    # Build prefix set once for efficiency (reused for both orientations)
    prefixes = build_prefix_set(dictionary)

    # Get the tile views for horizontal and vertical orientations
    views = get_tile_views(single_tiles, horizontal_tiles, vertical_tiles)

    # Unpack horizontal view
    horizontal_tiles_view, horizontal_groups = views['horizontal']

    # Unpack vertical view
    vertical_tiles_view, vertical_groups = views['vertical']

    # Find words for horizontal orientation (max 8 letters)
    horizontal_words = find_all_words(
        horizontal_tiles_view, horizontal_groups, dictionary, prefixes, min_length, max_horizontal_length
    )

    # Find words for vertical orientation (max 9 letters)
    vertical_words = find_all_words(
        vertical_tiles_view, vertical_groups, dictionary, prefixes, min_length, max_vertical_length
    )

    return {
        'horizontal': horizontal_words,
        'vertical': vertical_words
    }
