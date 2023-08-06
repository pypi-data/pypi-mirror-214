from functools import wraps

import typer

import morser

app = typer.Typer(name='Morser', no_args_is_help=True)


def on_stdout(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(func(*args, **kwargs))

    return wrapper


app.command(name='encode', no_args_is_help=True)(
    on_stdout(morser.encode_text_to_morse_code)
)
app.command(
    name='decode',
    no_args_is_help=True,
    help=(
        'Decode morse code to plain text. '
        'If morse code starts with a \'-\', use: decode -- "your string".'
    ),
)(on_stdout(morser.decode_morse_code))
