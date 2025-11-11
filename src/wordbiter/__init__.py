"""
Word Bites - A solver for the Word Bites puzzle game.
"""

from .word_finder import solve_word_bites, find_all_words, get_tile_views, build_prefix_set
from .dictionary import load_dictionary

__all__ = [
    'solve_word_bites',
    'find_all_words',
    'get_tile_views',
    'build_prefix_set',
    'load_dictionary',
]
