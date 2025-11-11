/**
 * Word Bites AI Solver - Frontend JavaScript
 * Handles form submission, API communication, and results display
 */

// DOM elements
const form = document.getElementById('tiles-form');
const solveButton = document.getElementById('solve-button');
const clearButton = document.getElementById('clear-button');
const resultsSection = document.getElementById('results-section');
const errorSection = document.getElementById('error-section');
const loadingSection = document.getElementById('loading-section');

// Form inputs
const singleTilesInput = document.getElementById('single-tiles');
const horizontalTilesInput = document.getElementById('horizontal-tiles');
const verticalTilesInput = document.getElementById('vertical-tiles');
const minWordLengthInput = document.getElementById('min-word-length');
const maxHorizontalInput = document.getElementById('max-horizontal');
const maxVerticalInput = document.getElementById('max-vertical');
const directionSelect = document.getElementById('direction');

// Results elements
const statsDiv = document.getElementById('stats');
const horizontalCountDiv = document.getElementById('horizontal-count');
const horizontalListDiv = document.getElementById('horizontal-list');
const verticalCountDiv = document.getElementById('vertical-count');
const verticalListDiv = document.getElementById('vertical-list');
const errorMessageDiv = document.getElementById('error-message');

/**
 * Parse space-separated tiles input into an array
 * @param {string} input - Space-separated tiles
 * @returns {string[]} Array of tiles
 */
function parseTiles(input) {
    return input.trim()
        .split(/\s+/)
        .filter(tile => tile.length > 0)
        .map(tile => tile.toUpperCase());
}

/**
 * Show/hide sections
 */
function showSection(section) {
    section.style.display = 'block';
}

function hideSection(section) {
    section.style.display = 'none';
}

/**
 * Display error message
 * @param {string} message - Error message to display
 */
function showError(message) {
    errorMessageDiv.textContent = message;
    showSection(errorSection);
    hideSection(resultsSection);
    hideSection(loadingSection);
}

/**
 * Display results
 * @param {Object} data - Results data from API
 */
function displayResults(data) {
    const { results, stats } = data;

    // Update stats
    statsDiv.textContent = `Found ${stats.total_count} total words (${stats.horizontal_count} horizontal, ${stats.vertical_count} vertical)`;

    // Display horizontal words
    displayWordList(results.horizontal, horizontalListDiv, horizontalCountDiv);

    // Display vertical words
    displayWordList(results.vertical, verticalListDiv, verticalCountDiv);

    // Show results section
    hideSection(loadingSection);
    hideSection(errorSection);
    showSection(resultsSection);

    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Display a list of words in a results column
 * @param {string[]} words - Array of words to display
 * @param {HTMLElement} listElement - Container element for word list
 * @param {HTMLElement} countElement - Element to show word count
 */
function displayWordList(words, listElement, countElement) {
    // Clear previous results
    listElement.innerHTML = '';

    if (words.length === 0) {
        countElement.textContent = 'No words found';
        listElement.innerHTML = '<p style="color: var(--text-secondary); font-style: italic;">No valid words found</p>';
        return;
    }

    // Update count
    countElement.textContent = `Showing all ${words.length} words (sorted by length)`;

    // Create word items
    words.forEach((word, index) => {
        const wordItem = document.createElement('div');
        wordItem.className = 'word-item';

        // Highlight longer words (7+ letters)
        if (word.length >= 7) {
            wordItem.classList.add('long-word');
        }

        wordItem.textContent = word;
        listElement.appendChild(wordItem);
    });
}

/**
 * Handle form submission
 * @param {Event} event - Form submit event
 */
async function handleSubmit(event) {
    event.preventDefault();

    // Parse input
    const singleTiles = parseTiles(singleTilesInput.value);
    const horizontalTiles = parseTiles(horizontalTilesInput.value);
    const verticalTiles = parseTiles(verticalTilesInput.value);

    // Validate input
    if (singleTiles.length === 0 && horizontalTiles.length === 0 && verticalTiles.length === 0) {
        showError('Please enter at least one tile');
        return;
    }

    // Get configuration
    const minWordLength = parseInt(minWordLengthInput.value);
    const maxHorizontal = parseInt(maxHorizontalInput.value);
    const maxVertical = parseInt(maxVerticalInput.value);
    const direction = directionSelect.value;

    // Prepare request payload (follows API contract from app.py)
    const payload = {
        single_tiles: singleTiles,
        horizontal_tiles: horizontalTiles,
        vertical_tiles: verticalTiles,
        min_length: minWordLength,
        max_horizontal_length: maxHorizontal,
        max_vertical_length: maxVertical,
        only_direction: direction === 'both' ? null : direction
    };

    // Show loading state
    hideSection(resultsSection);
    hideSection(errorSection);
    showSection(loadingSection);
    solveButton.disabled = true;

    try {
        // Call API
        const response = await fetch('/api/solve', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to solve puzzle');
        }

        if (!data.success) {
            throw new Error(data.error || 'Unknown error occurred');
        }

        // Display results
        displayResults(data);

    } catch (error) {
        console.error('Error:', error);
        showError(error.message || 'An error occurred while finding words. Please try again.');
    } finally {
        solveButton.disabled = false;
    }
}

/**
 * Handle clear button click
 */
function handleClear() {
    // Clear tile inputs
    singleTilesInput.value = '';
    horizontalTilesInput.value = '';
    verticalTilesInput.value = '';

    // Reset configuration to defaults
    minWordLengthInput.value = '3';
    maxHorizontalInput.value = '8';
    maxVerticalInput.value = '9';
    directionSelect.value = 'both';

    // Hide results and errors
    hideSection(resultsSection);
    hideSection(errorSection);
    hideSection(loadingSection);

    // Focus on first input
    singleTilesInput.focus();
}

/**
 * Initialize the application
 */
function init() {
    // Attach form submit handler
    form.addEventListener('submit', handleSubmit);

    // Attach clear button handler
    clearButton.addEventListener('click', handleClear);

    // Auto-uppercase input as user types
    const textInputs = [singleTilesInput, horizontalTilesInput, verticalTilesInput];
    textInputs.forEach(input => {
        input.addEventListener('input', (e) => {
            const cursorPosition = e.target.selectionStart;
            e.target.value = e.target.value.toUpperCase();
            e.target.setSelectionRange(cursorPosition, cursorPosition);
        });
    });

    // Check API health on load
    checkApiHealth();
}

/**
 * Check if the API is healthy
 */
async function checkApiHealth() {
    try {
        const response = await fetch('/api/health');
        const data = await response.json();

        if (!data.dictionary_loaded) {
            console.warn('Dictionary not loaded on server');
        } else {
            console.log(`API ready. Dictionary loaded with ${data.dictionary_size} words`);
        }
    } catch (error) {
        console.error('API health check failed:', error);
    }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
