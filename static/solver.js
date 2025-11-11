/**
 * Word Bites Solver - Core Algorithm (JavaScript Port)
 * Ported from Python implementation in src/wordbiter/word_finder.py
 */

/**
 * Build a set of all prefixes from the dictionary for efficient pruning
 * @param {Set<string>} dictionary - Set of valid dictionary words (uppercase)
 * @returns {Set<string>} Set of all prefixes that exist in the dictionary
 */
function buildPrefixSet(dictionary) {
    const prefixes = new Set();
    for (const word of dictionary) {
        for (let i = 1; i <= word.length; i++) {
            prefixes.add(word.substring(0, i));
        }
    }
    return prefixes;
}

/**
 * Generate horizontal and vertical views of tiles based on their orientations
 * @param {string[]} singleTiles - List of single-letter tiles
 * @param {string[]} horizontalTiles - List of multi-letter tiles oriented horizontally
 * @param {string[]} verticalTiles - List of multi-letter tiles oriented vertically
 * @returns {Object} Dictionary with 'horizontal' and 'vertical' keys
 */
function getTileViews(singleTiles, horizontalTiles, verticalTiles) {
    const horizontalView = [];
    const horizontalGroups = [];
    const verticalView = [];
    const verticalGroups = [];

    let groupId = 0;

    // Single-letter tiles appear the same in both views
    for (const tile of singleTiles) {
        horizontalView.push(tile);
        horizontalGroups.push(groupId);
        verticalView.push(tile);
        verticalGroups.push(groupId);
        groupId++;
    }

    // Horizontal tiles: used as multi-letter tiles in horizontal view,
    // split into individual letters in vertical view (but same group)
    for (const tile of horizontalTiles) {
        // In horizontal view: one multi-letter tile
        horizontalView.push(tile);
        horizontalGroups.push(groupId);

        // In vertical view: split into individual letters, all with same group ID
        for (const letter of tile) {
            verticalView.push(letter);
            verticalGroups.push(groupId);
        }

        groupId++;
    }

    // Vertical tiles: split into individual letters in horizontal view (same group),
    // used as multi-letter tiles in vertical view
    for (const tile of verticalTiles) {
        // In horizontal view: split into individual letters, all with same group ID
        for (const letter of tile) {
            horizontalView.push(letter);
            horizontalGroups.push(groupId);
        }

        // In vertical view: one multi-letter tile
        verticalView.push(tile);
        verticalGroups.push(groupId);

        groupId++;
    }

    return {
        horizontal: [horizontalView, horizontalGroups],
        vertical: [verticalView, verticalGroups]
    };
}

/**
 * Find all valid words that can be formed from the given tiles
 * Uses backtracking with prefix pruning for efficiency
 * @param {string[]} tiles - List of tiles, where each tile contains one or more letters
 * @param {number[]} groups - List of group IDs where tiles with the same ID are mutually exclusive
 * @param {Set<string>} dictionary - Set of valid dictionary words (uppercase)
 * @param {Set<string>} prefixes - Set of all valid prefixes from dictionary (for pruning)
 * @param {number} minLength - Minimum word length (default: 3)
 * @param {number} maxLength - Maximum word length (default: 9)
 * @returns {string[]} Sorted list of all valid words found
 */
function findAllWords(tiles, groups, dictionary, prefixes, minLength = 3, maxLength = 9) {
    // Validate inputs
    if (tiles.length !== groups.length) {
        throw new Error(`tiles and groups must have same length: ${tiles.length} != ${groups.length}`);
    }
    if (minLength < 1) {
        throw new Error(`min_length must be >= 1, got ${minLength}`);
    }
    if (maxLength < minLength) {
        throw new Error(`max_length (${maxLength}) must be >= min_length (${minLength})`);
    }

    // Uppercase all tiles once at the start
    const tilesUpper = tiles.map(tile => tile.toUpperCase());

    const validWords = new Set();

    /**
     * Recursively build words using available tiles
     * @param {string} currentWord - The word being built
     * @param {Set<number>} usedIndices - Set of tile indices already used
     * @param {Set<number>} usedGroups - Set of group IDs already used
     */
    function backtrack(currentWord, usedIndices, usedGroups) {
        // Prune: if current word is too long, stop
        if (currentWord.length > maxLength) {
            return;
        }

        // Prune: if current word is not a prefix of any dictionary word, stop
        if (currentWord && !prefixes.has(currentWord)) {
            return;
        }

        // Check if current word is valid
        if (currentWord.length >= minLength && dictionary.has(currentWord)) {
            validWords.add(currentWord);
        }

        // Try adding each unused tile
        for (let i = 0; i < tilesUpper.length; i++) {
            const tileGroup = groups[i];
            // Can only use this tile if we haven't used its index or any tile from its group
            if (!usedIndices.has(i) && !usedGroups.has(tileGroup)) {
                const newWord = currentWord + tilesUpper[i];
                const newUsedIndices = new Set(usedIndices);
                newUsedIndices.add(i);
                const newUsedGroups = new Set(usedGroups);
                newUsedGroups.add(tileGroup);
                backtrack(newWord, newUsedIndices, newUsedGroups);
            }
        }
    }

    // Start backtracking from empty word
    backtrack("", new Set(), new Set());

    // Sort by length (longest first), then alphabetically
    return Array.from(validWords).sort((a, b) => {
        if (b.length !== a.length) {
            return b.length - a.length;
        }
        return a.localeCompare(b);
    });
}

/**
 * Top-level API to solve Word Bites puzzle
 * @param {string[]} singleTiles - List of single-letter tiles
 * @param {string[]} horizontalTiles - List of multi-letter tiles oriented horizontally
 * @param {string[]} verticalTiles - List of multi-letter tiles oriented vertically
 * @param {Set<string>} dictionary - Set of valid dictionary words (uppercase)
 * @param {number} minLength - Minimum word length (default: 3)
 * @param {number} maxHorizontalLength - Maximum horizontal word length (default: 8)
 * @param {number} maxVerticalLength - Maximum vertical word length (default: 9)
 * @returns {Object} Dictionary with 'horizontal' and 'vertical' keys, each containing a list of valid words
 */
function solveWordBites(singleTiles, horizontalTiles, verticalTiles, dictionary, minLength = 3, maxHorizontalLength = 8, maxVerticalLength = 9) {
    // Build prefix set once for efficiency (reused for both orientations)
    const prefixes = buildPrefixSet(dictionary);

    // Get the tile views for horizontal and vertical orientations
    const views = getTileViews(singleTiles, horizontalTiles, verticalTiles);

    // Unpack horizontal view
    const [horizontalTilesView, horizontalGroups] = views.horizontal;

    // Unpack vertical view
    const [verticalTilesView, verticalGroups] = views.vertical;

    // Find words for horizontal orientation (max 8 letters)
    const horizontalWords = findAllWords(
        horizontalTilesView,
        horizontalGroups,
        dictionary,
        prefixes,
        minLength,
        maxHorizontalLength
    );

    // Find words for vertical orientation (max 9 letters)
    const verticalWords = findAllWords(
        verticalTilesView,
        verticalGroups,
        dictionary,
        prefixes,
        minLength,
        maxVerticalLength
    );

    return {
        horizontal: horizontalWords,
        vertical: verticalWords
    };
}
