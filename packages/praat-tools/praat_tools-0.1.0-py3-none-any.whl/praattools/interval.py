# praat-tools --- Read and write Praat objects
# Copyright (C) 2023 Athena Luka
#
# This file is part of praat-tools.
#
# praat-tools is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# praat-tools is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with praat-tools. If not, see
# <https://www.gnu.org/licenses/>.

from datetime import timedelta
import numbers

class Time:
    _time: timedelta

    def __init__(self, time):
        if isinstance(time, timedelta):
            self._time = time
        elif isinstance(time, numbers.Real):
            self._time = timedelta(seconds=time)
        else:
            raise TypeError('Time must be a number in seconds or a timedelta.')

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value: timedelta):
        if not isinstance(value, timedelta):
            raise TypeError('Expected {}, found {}'.format(timedelta,
                                                           type(value)))

        self._time = value

    @property
    def time_s(self) -> float:
        return self.time.total_seconds()

    @time_s.setter
    def time_s(self, value: float):
        self._time = timedelta(seconds=value)

    @property
    def time_ms(self) -> float:
        return self.time / timedelta(milliseconds=1)

    @time_ms.setter
    def time_ms(self, value: float):
        self._time = timedelta(milliseconds=value)

    def __repr__(self):
        return '{}: {} s'.format(type(self).__name__, self.time_s)


class Interval:
    _start: Time
    _end: Time

    def __init__(self, start, end):
        self._start = Time(start)
        self._end = Time(end)

        if self.start > self.end:
            raise ValueError('End time cannot be smaller than start time.')

    def __repr__(self):
        return '{}: {} to {} s'.format(type(self).__name__, self.start_s, self.end_s)

    @property
    def start(self) -> timedelta:
        """Start time."""

        return self._start.time

    @start.setter
    def start(self, value: timedelta):
        if value > self.end:
            raise ValueError('Start time cannot exceed end time.')

        self._start.time = value

    @property
    def end(self) -> timedelta:
        """End time."""
        return self._end.time

    @end.setter
    def end(self, value: timedelta):
        if value < self.start:
            raise ValueError('End time cannot be smaller than start time.')

        self._end.time = value

    @property
    def start_s(self) -> float:
        """Start time in seconds."""

        return self._start.time_s

    @start_s.setter
    def start_s(self, value: float):
        self.start = timedelta(seconds=value)

    @property
    def end_s(self) -> float:
        """End time in seconds."""

        return self._end.time_s

    @end_s.setter
    def end_s(self, value: float):
        self.end = timedelta(seconds=value)

    @property
    def start_ms(self) -> float:
        """Start time in milliseconds."""

        return self._start.time_ms

    @start_ms.setter
    def start_ms(self, value: float):
        self.start = timedelta(milliseconds=value)

    @property
    def end_ms(self) -> float:
        """End time in milliseconds."""

        return self._end.time_ms

    @end_ms.setter
    def end_ms(self, value: float):
        self.end = timedelta(milliseconds=value)
