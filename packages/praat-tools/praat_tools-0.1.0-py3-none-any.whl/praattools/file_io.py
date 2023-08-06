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

import string

def skip_whitespace(data):
    data = data.lstrip()

    while data[0] not in string.digits + '-+"':
    #while data[0] != '"':
        data = data.split(maxsplit=1)[1]

    return data


def consume_numstr(data):
    data = skip_whitespace(data)
    if data[0] == '"':
        raise Exception(
            "Expected a number but found a String: '{}...'.".format(data[:10]))

    (numstr, data) = data.split(maxsplit=1)
    return (numstr, data)


def consume_int(data):
    (numstr, data) = consume_numstr(data)
    num = int(numstr)
    return (num, data)


def consume_float(data):
    (numstr, data) = consume_numstr(data)
    num = float(numstr)
    return (num, data)


def consume_string(data):
    data = skip_whitespace(data)
    if data[0] != '"':
        raise Exception(
            "Expected a String but found a number: '{}...'.".format(data[:10]))

    start_index = 1 # skip opening quote
    next_quote = data.find('"', start_index)
    while data[next_quote+1] == '"':
        start_index = next_quote+1
        next_quote = data.find('"', start_index)

    retval = data[1:next_quote]
    data = data[next_quote+1:]
    return (retval, data)
