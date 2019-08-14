#! /usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)
import os.path
# import yaml
import pandas as pd
from . import songparser

artist_replace = {

    "Blue Effekt": "Blue Effekt"
}


def sort_filelist_by_author(rootdir, filelist):

    sngnames = []
    sngauthors = []
    for fl in filelist:
        pth = os.path.join(rootdir, fl)

        # fl = open(pth, 'r')
        # line = fl.readline()
        song = songparser.SongParser(pth)
        sngname = song.name
        sngauthor = song.artist
        sngauthor = artist_name_preprocessing(sngauthor)
        sngnames.append(sngname)
        sngauthors.append(sngauthor)

    fltable = {'file': filelist, 'name': sngnames, 'author': sngauthors}
    pdfl = pd.DataFrame(fltable)
    pdflsorted = pdfl.sort_values('author')
    fltable_sorted = pdflsorted.reset_index(drop=True).to_dict()
    #import ipdb; ipdb.set_trace() #  noqa BREAKPOINT

    # return filelist
    return fltable_sorted['file'].values()

def artist_name_preprocessing(artist):
    """
    Pokud je jméno ve slovníku, použije jej, jinak ořehodí pořadí slov, aby se řadilo dle příjmení
    :param artist:
    :return:
    """
    import re
    if artist in artist_replace:
        artist = artist_replace[artist]
    else:
        # if there is something in the braces cut this out
        rr = r"\(.*\)"
        in_braces = re.search(rr, artist)
        artist = re.sub(rr, "", artist)


        alist_reverse = artist.strip().split(" ")[::-1]
        artist = " ".join(alist_reverse)

        if in_braces is not None:
            artist = in_braces.group() + " " + artist
            #import ipdb; ipdb.set_trace()
        artist = artist.replace("(", " ")
        artist = artist.replace(")", " ")
        artist = artist.replace(";", " ")
        artist = artist.replace("  ", " ")
    return artist

