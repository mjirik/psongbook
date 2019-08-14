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
# import glob
import fnmatch

import os

def doc_to_text_catdoc(filename):
    (fi, fo, fe) = os.popen3('catdoc -w "%s"' % filename)
    fi.close()
    retval = fo.read()
    erroroutput = fe.read()
    fo.close()
    fe.close()
    if not erroroutput:
        return retval
    else:
        raise OSError("Executing the command caused an error: %s" % erroroutput)

def text_processing(txt, replace_tab=True):
    txt = txt.replace('\t', ' - ')
    return txt

def save_to_file(txt, ofilename):
    with open(ofilename, 'w') as f:
        f.write(txt)

def file_processing(filename):
    txt = doc_to_text_catdoc(filename)
    txt = text_processing(txt)
    ofilename = get_output_filename(filename.decode('utf8'))
    save_to_file(txt, ofilename)

def directory_processing(path):
    # glob is not working recursively
    # flist = glob.glob(os.path.join(filename, "*.doc"))
    filelist = [os.path.join(dirpath, f)
        for dirpath, dirnames, files in os.walk(path)
        for f in fnmatch.filter(files, '*.doc')]

    for filename in filelist:
        file_processing(filename)

def get_output_filename(filename):
    pth, fn = os.path.split(filename)
    ofilename = unicodedata.normalize('NFKD', fn).encode('ascii', 'ignore')
    ofilename = ofilename.replace(' ', '_')
    ofilename = ofilename.replace('.doc', '.txt')
    ofilename = os.path.join(pth, ofilename)
    return ofilename

def get_parser(parser=None):
    if parser is None:
        parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        # '-i',
        'inputfile',
        default=None,
        # required=True,
        help='input file'
    )
    parser.add_argument(
        '-d', '--debug', action='store_true',
        help='Debug mode')
    return parser

def main():
    logger = logging.getLogger()

    logger.setLevel(logging.DEBUG)
    # this was used as ch.setLevel(logging.DEBUG)
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

    
    if os.path.isfile(args.inputfile):
        file_processing(args.inputfile)
    else:
        directory_processing(args.inputfile)
    # import ipdb; ipdb.set_trace() #  noqa BREAKPOINT
    


if __name__ == "__main__":
    main()
