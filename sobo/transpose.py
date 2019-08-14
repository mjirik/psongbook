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
# import ipdb


def process_file(filename):
    text = load_file(filename)
    # ipdb.set_trace()


def load_file(ofilename):
    text = None
    with open(ofilename, 'r') as f:
        text = f.read()

    return text

def get_parser(parser=None):
    if parser is None:
        parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        '-i', '--inputfile',
        default=None,
        required=True,
        help='input file'
    )
    parser.add_argument(
        '-d', '--debug', action='store_true',
        help='Debug mode')
    return parser

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
    parser = get_parser()
    args = parser.parse_args()
    main_args(args)



def main_args(args):

    if args.debug:
        logger.setLevel(logging.DEBUG)
    process_file(args.inputfile)


if __name__ == "__main__":
    main()