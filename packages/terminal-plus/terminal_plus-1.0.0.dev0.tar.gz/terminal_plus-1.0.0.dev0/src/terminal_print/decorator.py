from .color import FontColor
import os

def font_color(color = FontColor.default):
    def inner(func):
        def wapper(*args, **kwargs):
            print(color, end='')
            ret = func(*args, **kwargs)
            print(FontColor.default, end='')
            return ret
        return wapper
    return inner

def head_foot_line(line = '-', color = FontColor.green):
    def inner(func):
        def wapper(*args, **kwargs):
            print(color, end='')
            t_columns = os.get_terminal_size().columns
            print(line * t_columns)
            ret = func(*args, **kwargs)
            print(line * t_columns)
            print(FontColor.default, end='')
            return ret
        return wapper
    return inner


