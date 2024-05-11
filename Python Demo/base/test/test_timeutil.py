import base.timeutil.time_tool as tt
from base.timeutil.time_tool import TimeUnit

if __name__ == '__main__':
    now_sec = tt.timestamp_now(TimeUnit.SECONDS)
    now_millis = tt.timestamp_now(TimeUnit.MILLISECONDS)
    print(f'{tt.format_timestamp('171517209004122222')}')
    print(f'{tt.format_timestamp(now_millis, pattern='_%Y%m%d_%H%M%S', with_millis=True, separator='_')}')
    print(f'{tt.suffix_by_timestamp(pattern='_%Y%m%d_%H%M%S', with_millis=True)}')
