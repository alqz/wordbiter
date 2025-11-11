"""Setup script for Word Bites."""

from setuptools import setup, find_packages

setup(
    name="wordbiter",
    version="1.0.0",
    description="Word Bites - Find all valid words from game tiles",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "wordbiter=wordbiter.main:main",
        ],
    },
)
