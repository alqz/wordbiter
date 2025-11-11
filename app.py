"""
Word Bites - Web Interface
Flask web server providing a browser-based interface for the Word Bites solver.
This module acts as a thin API layer over the core solver logic.
"""

from flask import Flask, request, jsonify, send_from_directory
import os
import sys

# Add src directory to path to import wordbiter package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from wordbiter.dictionary import load_dictionary
from wordbiter.word_finder import solve_word_bites

app = Flask(__name__, static_folder='static')

# Global dictionary cache (loaded once on startup)
dictionary = None
DEFAULT_DICTIONARY_PATH = "dictionaries/scrabble_words.txt"
DEFAULT_MIN_WORD_LENGTH = 3
DEFAULT_MAX_HORIZONTAL_LENGTH = 8
DEFAULT_MAX_VERTICAL_LENGTH = 9


def initialize_dictionary():
    """Load dictionary on startup."""
    global dictionary

    # Try multiple dictionary paths in order of preference
    dict_paths = [
        DEFAULT_DICTIONARY_PATH,
        "dictionaries/words_alpha.txt",
        "dictionaries/mit_words.txt",
        "/usr/share/dict/words"
    ]

    for path in dict_paths:
        if os.path.exists(path):
            print(f"Loading dictionary from {path}...")
            dictionary = load_dictionary(path)
            print(f"Loaded {len(dictionary)} words")
            return

    raise FileNotFoundError("No dictionary file found. Please ensure dictionaries directory exists.")


@app.route('/')
def index():
    """Serve the main HTML page."""
    return send_from_directory('static', 'index.html')


@app.route('/api/solve', methods=['POST'])
def solve():
    """
    API endpoint to solve Word Bites puzzle.

    Expected JSON payload:
    {
        "single_tiles": ["A", "E", "T"],
        "horizontal_tiles": ["AB", "CD"],
        "vertical_tiles": ["RT"],
        "min_length": 3,
        "max_horizontal_length": 8,
        "max_vertical_length": 9,
        "only_direction": null | "h" | "v"
    }

    Returns:
    {
        "success": true,
        "results": {
            "horizontal": ["WORD1", "WORD2", ...],
            "vertical": ["WORD3", "WORD4", ...]
        },
        "stats": {
            "horizontal_count": 10,
            "vertical_count": 15,
            "total_count": 25
        }
    }
    """
    try:
        # Parse request data
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "No JSON data provided"
            }), 400

        # Extract tiles (default to empty lists)
        single_tiles = [tile.upper() for tile in data.get('single_tiles', [])]
        horizontal_tiles = [tile.upper() for tile in data.get('horizontal_tiles', [])]
        vertical_tiles = [tile.upper() for tile in data.get('vertical_tiles', [])]

        # Extract configuration
        min_length = data.get('min_length', DEFAULT_MIN_WORD_LENGTH)
        max_horizontal_length = data.get('max_horizontal_length', DEFAULT_MAX_HORIZONTAL_LENGTH)
        max_vertical_length = data.get('max_vertical_length', DEFAULT_MAX_VERTICAL_LENGTH)
        only_direction = data.get('only_direction')

        # Validate inputs
        if not single_tiles and not horizontal_tiles and not vertical_tiles:
            return jsonify({
                "success": False,
                "error": "At least one tile must be provided"
            }), 400

        # Call the core solver (modular separation - web layer calls business logic)
        results = solve_word_bites(
            single_tiles,
            horizontal_tiles,
            vertical_tiles,
            dictionary,
            min_length=min_length,
            max_horizontal_length=max_horizontal_length,
            max_vertical_length=max_vertical_length
        )

        # Filter results based on direction preference
        horizontal_words = results['horizontal'] if only_direction != 'v' else []
        vertical_words = results['vertical'] if only_direction != 'h' else []

        # Prepare response
        response = {
            "success": True,
            "results": {
                "horizontal": horizontal_words,
                "vertical": vertical_words
            },
            "stats": {
                "horizontal_count": len(horizontal_words),
                "vertical_count": len(vertical_words),
                "total_count": len(horizontal_words) + len(vertical_words)
            }
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "dictionary_loaded": dictionary is not None,
        "dictionary_size": len(dictionary) if dictionary else 0
    })


if __name__ == '__main__':
    # Initialize dictionary before starting server
    initialize_dictionary()

    # Run Flask development server
    app.run(debug=True, host='0.0.0.0', port=5001)
