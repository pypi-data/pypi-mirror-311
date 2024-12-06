"""Contains Poseidon Bay search tools"""

def search_for_vowels(phrase: str) -> set:
    """Takes in a phrase and returns a set of vowels."""
    vowels = set('aeiuo')
    return vowels.intersection(set(phrase))


def search_for_char(phrase: str, chars: str='aeiou') -> set:
    """Returns chars in phrase"""
    return set(chars).intersection(set(phrase))
