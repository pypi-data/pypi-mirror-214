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

from __future__ import annotations

__all__ = ['TextGrid', 'Tier', 'IntervalTier', 'PointTier',
           'IntervalElement', 'PointElement']
__version__ = "v0.1.0"

import collections.abc
import datetime
from functools import singledispatchmethod
import numbers
from typing import SupportsIndex, overload

from praattools import file_io
from praattools.interval import Interval, Time


class Element:
    name: str

    def __init__(self, name: str, *args, **kwargs):
        if not isinstance(name, str):
            raise TypeError
        self.name = name
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return "{}: '{}'".format(type(self).__name__, self.name)


class PointElement(Element, Time):
    """An element in a :py:class:`PointTier`."""

    def __init__(self, name: str, time: float | ~datetime.timedelta):
        """
        :param name: The point name/mark.
        :param time: The point's start time, in seconds or as a
            :py:class:`~datetime.timedelta`.
        """

        super().__init__(name, time)


    def __repr__(self):
        return '{} ({} s)'.format(super().__repr__(), self.time_s)

class IntervalElement(Element, Interval):
    """An element in an :py:class:`IntervalTier`."""

    def __init__(self,
                 name: str,
                 start: float | ~datetime.timedelta,
                 end: float | ~datetime.timedelta):
        """
        :param name: The interval name/mark.
        :param start: The interval's start time, in seconds or as a
            :py:class:`datetime.timedelta`.
        :param end: The interval's end time, in seconds or as a
            :py:class:`datetime.timedelta`.
        """

        super().__init__(name, start, end)

    def __repr__(self):
        return '{} ({} to {} s)'.format(super().__repr__(),
                                     self.start_s,
                                     self.end_s)


class Tier(Interval, list[Element]):
    """
    Not to be constructed separately. Base class for
    :py:class:`IntervalTier` and :py:class:`PointTier`.
    """

    name: str
    element_type: type

    def __init__(self,
                 name: str,
                 start: float | ~datetime.timedelta, 
                 end: float | ~datetime.timedelta,
                 elements: list = []):
        """
        Initialises a Tier.

        :param name: The Tier name.
        :param start: The Tier's start time, in seconds or as a
            :py:class:`~datetime.timedelta`.
        :param end: The Tier's end time, in seconds or as a
            :py:class:`~datetime.timedelta`.
        :param elements: Elements to instantiate the tier with.
        """

        # This is an abstract class. Only instantiate derived classes
        # that define an element_type.
        if not hasattr(self, 'element_type'):
            raise NotImplementedError

        self.name = name

        super().__init__(start, end) # Interval init
        super(Interval, self).__init__(elements) # list init

    def __repr__(self):
        return '{} {}'.format(super().__repr__(),
                              super(Interval, self).__repr__())

    def _check_type(self, elem):
        if not isinstance(elem, self.element_type):
            raise TypeError(type(elem))

    def append(self, elem):
        self._check_type(elem)
        super().append(elem)

    def extend(self, elems):
        [self._check_type(elem) for elem in elems]
        super().extend(elems)

    def insert(self, i, elem):
        self._check_type(elem)
        super().insert(i, elem)

    @overload
    def __setitem__(self, index: SupportsIndex, elem: Element): ...
    @overload
    def __setitem__(self,
                    index: slice,
                    elems: ~collections.abc.Iterable[Element]): ...
    def __setitem__(self, index, elem):
        if isinstance(index, SupportsIndex):
            self._check_type(elem)
        elif isinstance(index, slice):
            (self._check_type(el) for el in elem)

        super().__setitem__(index, elem)


class PointTier(Tier):
    r"""
    A PointTier, or TextTier, of :py:class:`PointElement`\ s.

    PointTiers are (currently) implemented as a :py:class:`list` of
    py:class:`PointElement`\ s. They will always support all list
    operations like :py:meth:`~list.append`, :py:meth:`~list.insert`,
    and :py:meth:`~list.pop`.
    """

    element_type: type = PointElement


class IntervalTier(Tier):
    """An IntervalTier, consisting of :py:class:`IntervalElement`\ s.

    IntervalTiers are (currently) implemented as a :py:class:`list` of
    py:class:`IntervalElement`\ s. They will always support all list
    operations like :py:meth:`~list.append`, :py:meth:`~list.insert`,
    and :py:meth:`~list.pop`.
    """

    element_type: type = IntervalElement

    def _get_full(self):
        tier = type(self)(self.start, self.end)

        last_time = tier.start
        for interval in self:
            if last_time < interval.start:
                # add an empty interval
                tier.append(IntervalElement('',
                                            last_time.total_seconds(),
                                            interval.start_s))

            # then the regular one
            tier.append(interval)
            last_time = interval.end

        if last_time < tier.end:
            # final empty one
            tier.append(IntervalElement('',
                                        last_time.total_seconds(),
                                        tier.end_s))


        return tier


class TextGrid(Interval, list[Tier]):
    """
    A TextGrid object. Supports writing and reading from long and short
    TextGrid files.

    A TextGrid is (currently) implemented as a :py:class:`list` of
    Tiers. It will always support all list operations like
    :py:meth:`~list.append`, :py:meth:`~list.insert`, and
    :py:meth:`~list.pop`.
    """

    def __init__(self,
                 start: float | ~datetime.timedelta,
                 end: float | ~datetime.timedelta,
                 tiers: ~collections.abc.Iterable[Tier] = []):
        r"""
        Initialise a TextGrid.

        :param start: The start time, in seconds or as a timedelta.
        :param end: The end time, in seconds or as a timedelta.
        :param tiers: A list or other iterable of :py:class:`Tier`\ s to
            initialise with.
        """

        # Call Interval init with start & end
        super().__init__(start, end)

        # Check that every Tier is a tier and add it
        def validate(tier: Tier) -> bool:
            if isinstance(tier, Tier):
                return True
            else:
                raise TypeError

        self.extend(tier for tier in tiers if validate(tier))

    @classmethod
    def from_file(cls, filename: str, encoding: str = 'utf-8') -> TextGrid:
        """
        Create a TextGrid from a file. Currently supports short and long
        text formats, but not (yet) binary.

        :param filename: The TextGrid filename
        :param encoding: The character encoding of the TextGrid file
        :return: The created TextGrid
        """
        with open(filename, encoding=encoding) as f:
            data = f.read()

        (header, data) = file_io.consume_string(data)
        if header != 'ooTextFile':
            raise SyntaxError
        (objtype, data) = file_io.consume_string(data)
        if objtype != 'TextGrid':
            raise SyntaxError
        (start, data) = file_io.consume_float(data)
        (end, data) = file_io.consume_float(data)

        grid = cls(start, end)

        (num_tiers, data) = file_io.consume_int(data)
        for i in range(num_tiers):
            (tier_type, data) = file_io.consume_string(data)
            (tier_name, data) = file_io.consume_string(data)
            (start, data) = file_io.consume_float(data)
            (end, data) = file_io.consume_float(data)
            (num_elements, data) = file_io.consume_int(data)
            match tier_type:
                case 'IntervalTier':
                    tier: Tier = IntervalTier(tier_name, start, end)
                    for i in range(num_elements):
                        (start, data) = file_io.consume_float(data)
                        (end, data) = file_io.consume_float(data)
                        (name, data) = file_io.consume_string(data)
                        if name:
                            elem: Element = IntervalElement(name, start, end)
                            tier.append(elem)
                case 'TextTier':
                    tier = PointTier(tier_name, start, end)
                    for i in range(num_elements):
                        (time, data) = file_io.consume_float(data)
                        (name, data) = file_io.consume_string(data)
                        elem = PointElement(name, time)
                        tier.append(elem)
                case _:
                    raise SyntaxError

            grid.append(tier)
        return grid

    def to_file(self,
                filename: str,
                format: str = 'long',
                encoding: str = 'utf-8'):
        """
        Writes a TextGrid to a file. Currently supports short and long
        text formats, but not binary.

        :param filename: The new TextGrid filename
        :param format: The format to write the TextGrid in. Must be one
            of:

            * ``'long'`` To write a longform TextGrid file.
            * ``'short'`` To write a shortform TextGrid file.
            * ``'binary'`` (Planned in a future release.)
        :param encoding: The character encoding to be used

        :raises ValueError: If encoding is not one of ``'long'``,
            ``'short'``, or ``'binary'``.
        :raises NotImplementedError: When called with
            ``encoding='binary'``.
        """

        match format:
            case 'short':
                self._to_file_short(filename, encoding)
            case 'long':
                self._to_file_long(filename, encoding)
            case 'binary':
                raise NotImplementedError
            case _:
                raise ValueError(
                    "format must be one of 'long', 'short', or 'binary'.")

    @overload
    def __getitem__(self, index: SupportsIndex) -> Tier: ...
    @overload
    def __getitem__(self, index: str) -> Tier: ...
    @overload
    def __getitem__(self, index: slice) -> list[Tier]: ...
    def __getitem__(self, index):
        """
        A TextGrid can be indexed like a list or by name. Deleting is
        also implemented like this, but (re-)assignment can only be done
        by numeric index.
        """

        if isinstance(index, str):
            for tier in self:
                if tier.name == index:
                    return tier
            # if not found:
            raise KeyError('Tier {} not found.'.format(index))

        else:
            return super().__getitem__(index)

    def __delitem__(self, index: str | SupportsIndex | slice):
        """
        Delete self[key].

        :param index: Tier deletion supports indexing by number or by
            Tier name.
        """

        if isinstance(index, int):
            super().__delitem__(index)
        elif isinstance(index, str):
            for (i, tier) in enumerate(self):
                if tier.name == index:
                    del self[i]
                    break
            # if not found:
            raise KeyError('Tier {} not found.'.format(index))
        else:
            raise TypeError('Cannot index with type {}.'.format(type(index)))

    def _to_file_short(self, filename: str, encoding: str):
        # Private method. Writes to long textgrid; use
        # TextGrid.to_file().

        with open(filename, 'w', encoding=encoding) as f:
            f.write('File type = "ooTextFile"\nObject class = "TextGrid"\n\n')
            print('{:g}\n{:g}'.format(self.start_s, self.end_s), file=f)
            print('<exists>', file=f)
            print(len(self), file=f)
            for tier in self:
                if isinstance(tier, PointTier):
                    print('"TextTier"', file=f)
                    print('"{}"'.format(tier.name), file=f)
                    print('{:g}\n{:g}'.format(tier.start_s, tier.end_s),
                          file=f)
                    print(len(tier), file=f)

                    for point in tier:
                        print('{:g}'.format(point.time_s), file=f)
                        print('"{}"'.format(point.name), file=f)
                elif isinstance(tier, IntervalTier):
                    print('"IntervalTier"', file=f)
                    print('"{}"'.format(tier.name), file=f)
                    print('{:g}\n{:g}'.format(tier.start_s, tier.end_s),
                          file=f)

                    intervals = tier._get_full()
                    print(len(intervals), file=f)
                    for interval in intervals:
                        f.write('{:g}\n{:g}\n"{}"\n'.format(
                            interval.start_s,
                            interval.end_s,
                            interval.name
                        ))

                else:
                    raise SystemError(('Something has gone wrong. Found {} '
                                      'instead of a Tier.').format(type(tier)))

    def _to_file_long(self, filename: str, encoding: str):
        # Private method. Writes to long textgrid; use
        # TextGrid.to_file().

        with open(filename, 'w', encoding=encoding) as f:
            f.write('File type = "ooTextFile"\nObject class = "TextGrid"\n\n')
            f.write(('xmin = {:g} \n'
                     'xmax = {:g} \n'
                     'tiers? <exists> \n'
                     'size = {} \n'
                     'item []: \n').format(self.start_s, self.end_s, len(self)))

            for (i, tier) in enumerate(self, 1):
                f.write('    item [{}]:\n'.format(i))

                if isinstance(tier, PointTier):
                    f.write((
                        '        class = "TextTier" \n'
                        '        name = "{}" \n'
                        '        xmin = {:g} \n'
                        '        xmax = {:g} \n'
                        '        points: size = {} \n').format(tier.name,
                                                               tier.start_s,
                                                               tier.end_s,
                                                               len(tier)))

                    for (i, point) in enumerate(tier, 1):
                        f.write(('        points [{}]:\n'
                                 '            number = {:g} \n'
                                 '            mark = "{}" \n').format(i,
                                                                 point.time_s,
                                                                 point.name))
                elif isinstance(tier, IntervalTier):
                    f.write(('        class = "IntervalTier" \n'
                             '        name = "{}" \n'
                             '        xmin = {:g} \n'
                             '        xmax = {:g} \n').format(tier.name,
                                                              tier.start_s,
                                                              tier.end_s))

                    intervals = tier._get_full()
                    
                    f.write('        intervals: size = {} \n'.format(
                        len(intervals)
                    ))
                    for (i, interval) in enumerate(intervals, 1):
                        f.write((
                            '        intervals [{}]:\n'
                            '            xmin = {:g} \n'
                            '            xmax = {:g} \n'
                            '            text = "{}" \n').format(i,
                                                            interval.start_s,
                                                            interval.end_s,
                                                            interval.name))

                else:
                    raise SystemError(('Something has gone wrong. Found {} '
                                       'instead of a Tier.').format(type(tier)))
