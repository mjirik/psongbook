#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © %YEAR%  <>
#
# Distributed under terms of the %LICENSE% license.

"""

"""

import logging

logger = logging.getLogger(__name__)
import argparse
import copy
import re

def get_chord_line_indexes(lines):
    regex = "^ *( *[A-H][#b]?[^ ]*)+ *$"
    is_chord_line_re = re.compile(regex)

    chord_line_indexes = []
    not_chord_line_indexes = []
    for i in range(len(lines)):
        if is_chord_line_re.match(lines[i]) is not None:
            chord_line_indexes.append(i)
        else:
            not_chord_line_indexes.append(i)
    return chord_line_indexes, not_chord_line_indexes

def chords_from_chord_line(chord_line):

    regex_one = "[A-H][#b]?[^ ]*"
    fiter = re.finditer(regex_one, chord_line)
    st = []
    sp = []
    chords_from_line = []
    for m in fiter:
        st.append(m.start(0))
        sp.append(m.end(0))
        chords_from_line.append(m.group(0))
    return chords_from_line, st, sp

def fill_line_to_length(line, max_length):
    """

    """
    if line is None:
        line=''

    if max_length > len(line):
        newline = line + " " * (max_length - len(line))

    else:
        newline = line
    return newline

def split_line(line, indexes):
    split = []

    rest = copy.copy(line)
    for i in indexes:
        split.append(rest[:i])
        rest = rest[i:]
    return split

def song_without_chords(lines):
    # lines = text.splitlines()
    idx_out, idx_in = get_chord_line_indexes(lines)
    newlines = []
    for i in idx_in:
        newlines.append(lines[i])

    return newlines

def main():
    logger = logging.getLogger()

    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    logger.addHandler(ch)

    # create file handler which logs even debug messages
    # fh = logging.FileHandler('log.txt')
    # fh.setLevel(logging.DEBUG)
    # formatter = logging.Formatter(
    #     '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # fh.setFormatter(formatter)
    # logger.addHandler(fh)
    # logger.debug('start')

    # input parser
    parser = argparse.ArgumentParser(
        description=__doc__
    )
    parser.add_argument(
        '-i', '--inputfile',
        default=None,
        required=True,
        help='input file'
    )
    parser.add_argument(
        '-d', '--debug', action='store_true',
        help='Debug mode')
    args = parser.parse_args()

    if args.debug:
        ch.setLevel(logging.DEBUG)


if __name__ == "__main__":
    main()