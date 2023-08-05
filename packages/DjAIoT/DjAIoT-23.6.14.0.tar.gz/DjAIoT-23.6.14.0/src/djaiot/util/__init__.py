import numpy
import pandas
import re
from typing import Iterable, Optional


# Django
default_app_config = 'infx.machine_intel.util.apps.UtilConfig'


MAX_CHAR_FLD_LEN = 255


_PARQUET_FMT = 'parquet'
_PARQUET_EXT = f'.{_PARQUET_FMT}'

_YAML_FMT = 'yml'
_YAML_EXT = f'.{_YAML_FMT}'


IterableStrType = Iterable[str]
OptionalStrType = Optional[str]


def _clean(s):
    return re.sub('_{2,}', '_', re.sub('[^\w]+', '_', s).strip('_'))


def snake_case(s):
    return _clean(s).lower()


def upper_case(s):
    return _clean(s).upper()


def coerce_bool(x):
    if pandas.notnull(x):
        return bool(x) \
            if isinstance(x, (numpy.bool_, int, float)) \
          else x


def coerce_float(x):
    try:
        return float(x)

    except:
        pass


def coerce_int(x, tol=1e-8, return_orig=False):
    if isinstance(x, (bool, numpy.bool_, str)):
        if return_orig:
            return x

    else:
        try:
            i = int(x)

            if abs(i - x) < tol:
                return i

            elif return_orig:
                return x

        except:
            if return_orig:
                return x


def format_number_up_to_n_decimal_places(x, max_n_decimal_places=3):
    return ('{:,.%uf}' % max_n_decimal_places).format(x).rstrip('0').rstrip('.')


def missing_date_strs(among_dates):
    return {str(date)
            for date in
            pandas.date_range(
                start=min(among_dates),
                end=max(among_dates),
                periods=None,
                freq='D',
                tz=None,
                normalize=False,
                name=None,
                closed=None).date} \
        .difference(
            str(date)
            for date in among_dates)


class NonOverlappingClosedIntervals:
    def __init__(self):
        self.intervals = []
        self.lower = None
        self.upper = None
        self.n = 0

    def add(self, interval):
        assert isinstance(interval, list) \
           and (len(interval) == 2)
        
        lower, upper = interval
        assert lower <= upper

        if self.intervals:
            if upper < self.lower:
                self.intervals.insert(0, interval)
                self.lower = lower
                self.n += 1

            elif lower > self.upper:
                self.intervals.append(interval)
                self.upper = upper
                self.n += 1

            else:
                i, existing_interval = \
                    next((i, existing_interval)
                         for i, existing_interval in enumerate(self.intervals)
                         if existing_interval[1] >= lower)

                if upper < existing_interval[0]:
                    assert i
                    self.intervals.insert(i, interval)
                    self.n += 1

                else:
                    if lower < existing_interval[0]:
                        existing_interval[0] = lower
                        if not i:
                            self.lower = lower

                    if upper > existing_interval[1]:
                        existing_interval[1] = upper

                        next_i = i + 1

                        while (next_i < self.n) and (self.intervals[next_i][1] <= upper):
                            self.intervals.pop(next_i)
                            self.n -= 1

                        if next_i < self.n:
                            next_existing_interval = self.intervals[next_i]
                            if next_existing_interval[0] <= upper:
                                existing_interval[1] = next_existing_interval[1]
                                self.intervals.pop(next_i)
                                self.n -= 1

                        else:
                            self.upper = upper

        else:
            self.intervals = [interval]
            self.lower = lower
            self.upper = upper
            self.n = 1

        assert self.lower == self.intervals[0][0]
        assert self.upper == self.intervals[-1][1]
        assert self.n == len(self.intervals)

    def __bool__(self):
        return self.n > 0
