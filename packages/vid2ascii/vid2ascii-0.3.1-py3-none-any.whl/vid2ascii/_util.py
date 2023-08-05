import warnings
import shutil

def ConvertWarning(message):
    warnings.warn(message, category=UserWarning, stacklevel=2)


class ConvertError(Exception):
    pass


def get_bounds(width, height):
    aspect_ratio = width / height
    columns, rows = shutil.get_terminal_size()
    term_aspect_ratio = columns / rows

    if aspect_ratio < term_aspect_ratio:
        char_height = rows - 1
        char_width = int(char_height * aspect_ratio)
    else:
        char_width = columns - 1
        char_height = int(char_width / aspect_ratio)

    width_shift, height_shift = 0, 0
    if aspect_ratio > 1:
        height_shift = 1
        width_shift = round(aspect_ratio)
    else:
        height_shift = round(1 / aspect_ratio)
        width_shift = 1

    while char_width * char_height > 900: # can cause lag in frames
        char_width -= width_shift
        char_height -= height_shift

    char_width *= 2 # characters are twice as tall as they are wide
    return char_width, char_height
    

def get_color(red: float, green: float, blue: float) -> tuple:
    return f'\033[38;2;{int(red)};{int(green)};{int(blue)}m'
