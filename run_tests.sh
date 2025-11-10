#!/bin/bash
# Test runner script that sets up PYTHONPATH correctly

export PYTHONPATH="$(cd "$(dirname "${BASH_SOURCE[0]}")/src" && pwd):$PYTHONPATH"
python3 -m pytest tests/ "$@" || {
    echo "pytest not found, running tests directly..."
    for test_file in tests/test_*.py; do
        echo "Running $test_file..."
        python3 "$test_file"
    done
}
