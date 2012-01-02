import datetime

MICROSECONDS_PER_SECOND = 1000000.0
SECONDS_PER_DAY = 86400

def timedelta_to_seconds( td ):
    assert isinstance( td, datetime.timedelta )
    seconds = 0.0

    seconds += td.days * SECONDS_PER_DAY
    seconds += td.seconds
    seconds += td.microseconds / MICROSECONDS_PER_SECOND

    return seconds
