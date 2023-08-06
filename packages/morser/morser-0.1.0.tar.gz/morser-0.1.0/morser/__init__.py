import re

from .dictionary import DECODE_TABLE, ENCODE_TABLE


def _format_spaces_between_words(text: str) -> str:
    return re.sub(r'\s{1,}', ' ', text.strip())


def encode_text_to_morse_code(plain_text: str) -> str:
    """Encode a plain text to morse code."""
    if plain_text.isspace():
        raise ValueError("Parameter 'plain_text' is an empty string.")

    return ' '.join(
        ENCODE_TABLE.get(char, '#')
        for char in _format_spaces_between_words(plain_text).upper()
    )


def decode_morse_code(morse_code: str) -> str:
    """Decode morse code to plain text."""
    if morse_code.isspace():
        raise ValueError("Parameter 'morse_code' is an empty string.")

    morse_code = morse_code.strip()

    if re.search(r'\s{4,}', morse_code):
        raise ValueError('Morse code contains invalid spaces.')

    try:
        return ''.join(
            map(
                DECODE_TABLE.get,
                morse_code.replace(' ' * 3, ' <space> ').split(),
            )
        )
    except TypeError:
        raise ValueError('Morse code contains invalid characters.')
