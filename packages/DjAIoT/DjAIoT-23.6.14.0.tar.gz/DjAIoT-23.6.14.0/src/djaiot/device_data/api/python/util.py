__all__ = 'parse_from_date_and_to_date',


import datetime
from typing import Tuple, Union

from arimo.util.date_time import month_end


DateOrStrType = Union[datetime.date, str]
OptionalDateOrStrType = Union[datetime.date, str, None]


def parse_from_date_and_to_date(
        from_date: DateOrStrType, to_date: OptionalDateOrStrType = None) \
        -> tuple[DateOrStrType, OptionalDateOrStrType]:
    if isinstance(from_date, str) and (len(from_date) == 7):
        if to_date:
            assert isinstance(to_date, str) \
               and (len(to_date) == 7) \
               and (to_date > from_date)

            to_date = month_end(to_date)

        else:
            to_date = month_end(from_date)

        return datetime.datetime.strptime(from_date + '-01', '%Y-%m-%d').date(), \
               to_date

    elif isinstance(from_date, str):
        assert len(from_date) == 10

        if to_date:
            assert isinstance(to_date, str) \
               and (len(to_date) == 10) \
               and (to_date > from_date)

            to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d').date()

        return datetime.datetime.strptime(from_date, '%Y-%m-%d').date(), \
               to_date

    else:
        assert isinstance(from_date, datetime.date)

        if to_date:
            assert isinstance(to_date, datetime.date) \
               and (to_date > from_date)

        return from_date, to_date