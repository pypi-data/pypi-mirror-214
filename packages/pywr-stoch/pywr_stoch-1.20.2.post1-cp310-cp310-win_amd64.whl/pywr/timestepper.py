import pandas
import numpy as np
import datetime

import pandas as pd
from pandas._libs import OutOfBoundsDatetime
from pandas._libs.tslibs.parsing import DateParseError

from pywr import _core

# Constants
SECONDS_IN_DAY = 3600 * 24


class Timestepper(object):
    def __init__(self, start="2015-01-01", end="2015-12-31", delta=1):
        self.start = start
        self.end = end
        self.delta = delta
        self._last_length = None
        self._periods = None
        self._deltas = None
        self._current = None
        self._next = None
        self.setup()
        self.reset()
        self._dirty = True

    def __iter__(
        self,
    ):
        return self

    def __len__(
        self,
    ):
        return len(self._periods)

    @property
    def dirty(self):
        return self._dirty

    def setup(self):
        periods = self.datetime_index

        # only frequencies with delta are supported
        if not hasattr(periods.freq, "delta"):
            raise ValueError("The frequency is not supported because is non-fixed")
        # Compute length of each period
        deltas = periods.freq.delta
        # Round to nearest second
        deltas = np.round(deltas.total_seconds())
        # Convert to days
        deltas = deltas / SECONDS_IN_DAY

        self._periods = periods
        self._deltas = [deltas] * len(periods)
        self.reset()
        self._dirty = False

    def reset(self, start=None):
        """Reset the timestepper

        If start is None it resets to the original self.start, otherwise
        start is used as the new starting point.
        """
        self._current = None
        current_length = len(self)

        if start is None:
            current_index = 0
        else:
            if not isinstance(start, pd.Period):
                start = pd.Period(start, freq=self.freq)
            # Determine which period the start time is within
            if pd.Period(start, freq=self.freq) <= self._periods[0]:
                raise ValueError(
                    "New starting position is smaller than the first model timestep."
                )
            for index, period in enumerate(self._periods):
                if period >= start and period != self._periods[-1]:
                    current_index = index
                    break
            else:
                raise ValueError(
                    "New starting position is outside the range of the model timesteps."
                )

        self._next = _core.Timestep(
            self._periods[current_index], current_index, self._deltas[current_index]
        )
        length_changed = self._last_length != current_length
        self._last_length = current_length
        return length_changed

    def __next__(
        self,
    ):
        return self.next()

    def next(
        self,
    ):
        self._current = current = self._next

        if current.index >= len(self._periods):
            raise StopIteration()

        # Increment to next timestep
        next_index = current.index + 1
        if next_index >= len(self._periods):
            # The final time-step is one offset beyond the end of the model.
            # Here we compute its delta and create the object.
            final_period = current.period + self.offset
            self._next = _core.Timestep(final_period, next_index, self._deltas[-1])
        else:
            self._next = _core.Timestep(
                self._periods[next_index], next_index, self._deltas[next_index]
            )

        # Return this timestep
        return current

    @property
    def start(self):
        return self.start_period

    @start.setter
    def start(self, value):
        if isinstance(value, pandas.Period):
            self._start = value
        else:
            # validate date string
            try:
                pd.Period(value, freq="D")
            except (DateParseError, OutOfBoundsDatetime):
                raise ValueError("The start date format is not valid")
            self._start = value
        self._dirty = True

    @property
    def start_period(self):
        return pandas.Period(self._start, freq=self.freq)

    @property
    def end(self):
        return self.end_period

    @end.setter
    def end(self, value):
        if isinstance(value, pandas.Period):
            self._end = value
        else:
            # validate date string
            try:
                pd.Period(value, freq="D")
            except (DateParseError, OutOfBoundsDatetime):
                raise ValueError("The end date format is not valid")
            self._end = value
        self._dirty = True

    @property
    def end_period(self):
        return pandas.Period(self._end, freq=self.freq)

    @property
    def delta(self):
        return self._delta

    @delta.setter
    def delta(self, value):
        self._delta = value
        self._dirty = True

    @property
    def freq(self):
        d = self._delta
        if isinstance(d, int):
            freq = "{}D".format(d)
        elif isinstance(d, datetime.timedelta):
            freq = "{}D".format(d.days)
        else:
            freq = d
        return freq

    @property
    def offset(self):
        return pandas.tseries.frequencies.to_offset(self.freq)

    @property
    def current(self):
        """The current timestep

        If iteration has not begun this will return None.
        """
        return self._current

    @property
    def datetime_index(self):
        """Return a `pandas.DatetimeIndex` using the start, end and delta of this object

        This is useful for creating `pandas.DataFrame` objects from Model results
        """
        return pandas.period_range(self.start, self.end, freq=self.freq)

    def __repr__(self):
        start = self.start_period.strftime("%Y-%m-%d %H:%M")
        end = self.end_period.strftime("%Y-%m-%d %H:%M")
        return '<Timestepper start="{}" end="{}" freq="{}">'.format(
            start, end, self.freq
        )
