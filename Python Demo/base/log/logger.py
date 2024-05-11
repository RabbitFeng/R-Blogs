# 1. 单条日志富文本
# TODO: 2. 单条日志富文本混合
from enum import IntEnum


class ShowType(IntEnum):
    """
    显示方式
    """
    DEFAULT = 0,
    '''默认'''
    HIGH_LIGHT = 1,
    '''高亮'''
    UNDER_LINE = 4,
    '''下划线'''
    FLASHING = 5,
    '''闪烁'''
    HIGH_LIGHT_REVERSE = 7
    '''反显'''


class LogColor(IntEnum):
    NONE = 0,
    '''空'''
    BLACK = 30,
    '''黑色'''
    RED = 31,
    '''红色'''
    GREEN = 32,
    '''绿色'''
    YELLOW = 33,
    '''黄色'''
    BLUE = 34,
    '''蓝色'''
    MAGENTA = 35,
    '''品红色'''
    CYAN = 36,
    '''青色'''
    WHITE = 37,
    '''白色'''


def _text_color_str(color: LogColor) -> str:
    return f';{color.value}' if color != LogColor.NONE else ''


def _background_color_str(color: LogColor) -> str:
    return f';{color.value + 10}' if color != LogColor.NONE else ''


class LoggerBuilder:
    def __init__(self):
        self.__log = ''
        self.__show_type: ShowType = ShowType.DEFAULT
        self.__text_color: LogColor = LogColor.NONE
        self.__background_color: LogColor = LogColor.NONE

    def clear(self):
        self.__log = ''
        self.__show_type: ShowType = ShowType.DEFAULT
        self.__text_color: LogColor = LogColor.NONE
        self.__background_color: LogColor = LogColor.NONE
        return self

    def set_log(self, log: str):
        self.__log = log
        return self

    def set_show_type(self, show_type: ShowType):
        self.__show_type = show_type
        return self

    def set_text_color(self, color: LogColor):
        self.__text_color = color
        return self

    def set_background_color(self, color: LogColor):
        self.__background_color = color
        return self

    def build(self) -> str:
        text_color = _text_color_str(self.__text_color)
        background_color = _background_color_str(self.__background_color)
        return f'\033[{self.__show_type.value}{text_color}{background_color}m{self.__log}\033[0m'


# Shell
__builder = LoggerBuilder()


def log(line: str, show_type=ShowType.DEFAULT, text_color=LogColor.NONE, background_color=LogColor.NONE):
    print(__builder.clear()
          .set_log(line)
          .set_show_type(show_type)
          .set_text_color(text_color)
          .set_background_color(background_color)
          .build())


def log_error(line: str):
    log(line, show_type=ShowType.HIGH_LIGHT, text_color=LogColor.RED, background_color=LogColor.NONE)
