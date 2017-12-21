from datetime import datetime

# import psycopg2
import pytz



def date_as_timestamp(date_time):
    return timehelper.to_posix(date_time)


class timehelper(object):
    # @staticmethod
    # def localize_and_format(tz, fmt, dt):
    #
    #     # disallow naive datetimes
    #     if dt.tzinfo is None:
    #         raise ValueError("Passed datetime object has no tzinfo")
    #
    #     # workaround for psycopg2 tzinfo
    #     if isinstance(dt.tzinfo, psycopg2.tz.FixedOffsetTimezone):
    #         dt.tzinfo._utcoffset = dt.tzinfo._offset
    #
    #     return pytz.timezone(tz).normalize(dt).strftime(fmt)

    @staticmethod
    def now():
        return datetime.utcnow().replace(tzinfo=pytz.UTC)

    @staticmethod
    def to_posix(dt):
        return (dt - datetime(1970, 1, 1, tzinfo=pytz.UTC)).total_seconds()

    @staticmethod
    def from_posix(p):
        return datetime.fromtimestamp(p, pytz.UTC)
