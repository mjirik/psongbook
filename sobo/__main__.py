#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 mjirik <mjirik@mjirik-Latitude-E6520>
#
# Distributed under terms of the MIT license.

"""

"""

import logging
logger = logging.getLogger(__name__)
import argparse
import unicodedata
import glob
import fnmatch

import os
from . import doc2txt
from . import psongbook

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
        '-d', '--debug', action='store_true',
        help='Debug mode')
    subparsers = parser.add_subparsers(dest='mode')
    parser_d2t = subparsers.add_parser('doc2txt', help="convert doc file to txt file")
    doc2txt.get_parser(parser_d2t)
    parser_sobo = subparsers.add_parser('sobo', help="generate songbook")
    psongbook.get_parser(parser_sobo)
    parser_sobo = subparsers.add_parser('transpose', help="generate songbook")
    from . import transpose
    transpose.get_parser(parser_sobo)
    # parser.add_argument(
    #     'mode',
    #     choices=['doc2txt', 'sobo'],
    #     nargs='?',
    #     default='sobo'
    # )
    # parser.add_argument(
    #     # '-i',
    #     'inputfile',
    #     default=None,
    #     # required=True,
    #     help='input file'
    # )
    # knownargs, unknownargs = parser.parse_known_args()
    # import ipdb; ipdb.set_trace()
    args = parser.parse_args()



    if args.mode == 'doc2txt':
        doc2txt.main_args(args)
    elif args.mode == 'sobo':
        psongbook.main_args(args)
    elif args.mode == 'transpose':
        transpose.main_args(args)




def main_args():
    pass




if __name__ == "__main__":
    main()
