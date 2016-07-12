#! /usr/bin/python
# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger(__name__)
import traceback

def load_file(ofilename):
    text = None
    with open(ofilename, 'r') as f:
        textraw = f.read()

    try:
        text = textraw.decode('utf-8')
    except:
        try:
            text= textraw.decode('cp1250')
            # logger.warning("cp1250 used for file " + ofilename)
            #print "cp 1250 " + fullfilepath
        except:
            # print fullfilepath
            traceback.print_exc()
            logger.warning("Coding problem with file " +  ofilename)
    return text
