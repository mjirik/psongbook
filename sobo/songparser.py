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
import traceback
import inout

class SongParser:
    def __init__(self, song, filename=""):
        """

        :param song: filepath or list of lines
        :param filename:
        """
        if type(song) is list:
            lines = song
        else:
            lines = inout.load_file(song).splitlines()
            filename = song
        self.filename = filename
        #lines = self.coding(lines)
        self.lines_raw = lines
        self.parse_name_and_artist()
        lines = lines[1:]
        self.lines_no_chords = song_without_chords(lines)
        self.lines = lines
        chli, nchli = get_chord_line_indexes(self.lines)
        self.chord_line_indexes = chli
        self.no_chord_line_indexes = chli

    def coding(self, lines):
        lines_new = []

        for i in range(len(lines)):
            lineraw = lines[i]

            #print line
            # TODO dection input coding
            # TODO replacement of bad characters like \u8
            try:
                line = lineraw.decode('utf-8')
            except:
                try:
                    line = lineraw.decode('cp1250')
                    #print "cp 1250 " + fullfilepath
                except:
                    # print fullfilepath
                    traceback.print_exc()
                    logger.warning(self.filename)
            #line = line.encode("utf-8")
            lines_new.append(line)
        return lines_new



    def parse_name_and_artist(self):
        text = self.lines_raw[0]
        if len(text.strip()) == 0:
            text = self.lines_raw[1]

        name, artist = self.__parse_name_and_artist_from_line(text)
        self.name = name
        self.artist = artist

    def __parse_name_and_artist_from_line(self, text):
        name = text
        artist = ""

        try:
            # convert long dash into short dash
            text = text.replace("–".decode("utf-8"), "-")

            spl = text.split("-")
            name = spl[0].strip()
            artist = spl[1].strip()
        except:
            traceback.print_exc()
            logger.warning("Cannot parse song name and artist from first line\n" + text +"\n" + self.filename)
            #import ipdb; ipdb.set_trace()

        return name, artist



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