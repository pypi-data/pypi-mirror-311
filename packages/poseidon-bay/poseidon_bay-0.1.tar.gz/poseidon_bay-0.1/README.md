# Poseidon Bay

Contains Poseidon Bay search tools.

## Installation

```bash
pip install poseidon_bay

## Usage
from poseidon_bay import search_for_vowels, search_for_char

phrase = "Hello, World!"
print(search_for_vowels(phrase))  # Output: {'o', 'e'}
print(search_for_char(phrase, 'lo'))  # Output: {'l', 'o'}
