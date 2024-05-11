import time
from enum import Enum


class TimeUnit(Enum):
    """
    时间单位
    """
    MILLISECONDS = 0,
    SECONDS = 1,
    MINUTES = 2,
    HOURS = 3,
    DAYS = 4,
    YEARS = 5


# TODO: 参数健壮性

def timestamp_now(unit: TimeUnit = TimeUnit.MILLISECONDS) -> int:
    f"""
    获取时间戳，默认ms
    :param unit: 时间单位 {TimeUnit.SECONDS or TimeUnit.SECONDS}
    :return: int 时间戳
    """
    match unit:
        case TimeUnit.SECONDS:
            return round(time.time())
        case TimeUnit.MILLISECONDS | _:
            return round(time.time() * 1000)


def format_timestamp(timestamp: str | int,
                     pattern: str = '%Y-%m-%d %H:%M:%S',
                     unit: TimeUnit = TimeUnit.MILLISECONDS,
                     with_millis: bool = False,
                     separator: str = '.') -> str:
    f"""
    格式化时间戳 %Y-%m-%d %H:%M:%S.sss
    :param separator: 
    :param timestamp: 时间戳
    :param pattern: 格式化
    :param unit: 时间单位 {TimeUnit.SECONDS or TimeUnit.SECONDS}
    :param with_millis: 包含毫秒 仅当unit = TimeUnit.MILLISECONDS生效
    :return:
    """
    match unit:
        case TimeUnit.SECONDS:
            return time.strftime(f'{pattern}', time.localtime(int(timestamp)))
        case TimeUnit.MILLISECONDS | _:
            return time.strftime(f'{pattern}{f'{separator}{str(timestamp)[-3:]}' if with_millis else ''}',
                                 time.localtime(int(timestamp) / 1000))


def suffix_by_timestamp(pattern: str = '_%Y%m%d_%H%M%S',
                        with_millis: bool = True
                        ) -> str:
    """
    获取时间戳后缀 20240508_162718_035
    :param pattern:
    :param with_millis:
    :return: 时间戳后缀
    """
    return format_timestamp(timestamp_now(unit=TimeUnit.MILLISECONDS), pattern, TimeUnit.MILLISECONDS, with_millis,
                            separator='_')
