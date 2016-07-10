#! /usr/bin/python
# -*- coding: utf-8 -*-

# import funkcí z jiného adresáře
import sys
import subprocess
import shlex
import os
import fnmatch
import traceback
#sys.path.append("../src/")

import logging
logger = logging.getLogger(__name__)

import pdb
import pandas as pd
import re
#pdb.set_trace()
#import scipy.io
#mat = scipy.io.loadmat('step0.mat')

#print mat

def genfilelist(dirpath, wildcards='*.txt', structured = True):
    """ Function generates list of files from specific dir

    filesindir(dirpath, wildcard="*.*", startpath=None)

    dirpath: required directory
    wilcard: mask for files
    startpath: start for relative path


    """


    filelist = {}
    rootdir = dirpath
    for root, subFolders, files in os.walk(rootdir):
        #pdb.set_trace()
        if structured:
            filesutf8 = []
            # encoding to utf-8

            for fileu in fnmatch.filter(files, wildcards):
                #pdb.set_trace()
                filesutf8.append(fileu.decode(sys.getfilesystemencoding()).encode('utf8')) 

            #pth = os.path.join(root,fileu)
            dirname = os.path.relpath(root,rootdir)
            filesutf8 = sort_filelist_by_author(
                    os.path.join(rootdir, dirname), 
                    filesutf8
            )
            #fl={'dirname': dirname, 'files':filesutf8}
            #filelist.append(fl)
            filelist[dirname]=filesutf8
        else:
            for file in fnmatch.filter(files, wildcards):
                filelist.append(os.path.join(root,file))
    #        
    # print filelist
    # import ipdb; ipdb.set_trace() #  noqa BREAKPOINT
    

    #filelist = []
    #print dirpath

    #for infile in glob.glob( os.path.join(dirpath, wildcard) ):
    #    if startpath != None:
    #        infile = os.path.relpath(infile, startpath)
    #    filelist.append(infile)
        #print "current file is: " + infile

    sngbky = {'dirpath'.encode('utf8'): dirpath.encode('utf-8'), 'filelist'.encode('utf-8'):filelist }
    return sngbky

def sort_filelist_by_author(rootdir, filelist):
    sngnames = []
    sngauthors = []
    for fl in filelist:
        pth = os.path.join(rootdir, fl)

        fl = open(pth, 'r')
        line = fl.readline()
        sngname, sngauthor = parse_first_line(line)
        sngnames.append(sngname)
        sngauthors.append(sngauthor)

    fltable = {'file': filelist, 'name': sngnames, 'author': sngauthors}
    pdfl = pd.DataFrame(fltable)
    pdflsorted = pdfl.sort('author')
    fltable_sorted = pdflsorted.to_dict()
    # import ipdb; ipdb.set_trace() #  noqa BREAKPOINT

    # return filelist
    return fltable_sorted['file'].values()

def parse_first_line(line):
    split = line.find('-')
    sngname = line[:split].strip()
    sngauthor = line[split + 1:].strip()

    return sngname, sngauthor


def load_file(ofilename):
    text = None
    with open(ofilename, 'r') as f:
        text = f.read()

    return text

def _parse_file(fullfilepath):
    lines = load_file(fullfilepath).splitlines()
    import songparser
    song = songparser.SongParser(lines)
    # import ipdb; ipdb.set_trace() #  noqa BREAKPOINT
    return song


def _gentexfile_for_one(fullfilepath, compact_version=False):
    """
    generate latex string for one file
    :param filepath:
    :param sngbk:
    :param part:
    :return:
    """

    docpsongbook = ""

    song = _parse_file(fullfilepath)

    headline = song.name.decode("utf8") + " - " + song.artist.decode("utf8")
    docpsongbook += ("\n\\section{" + headline + "}\n").encode("utf8")
    docpsongbook += '\n\\begin{alltt}\n'
    #pdb.set_trace()


    # fl = load_file(fullfilepath)
    if compact_version:
        lines = song.lines_no_chords
        # lines = songparser.song_without_chords(lines)
    else:
        lines = song.lines
    import songparser
    idin, idout = songparser.get_chord_line_indexes(lines)

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
                print "cp 1250 " + fullfilepath
            except:
                print fullfilepath
                traceback.print_exc()

        logger.debug(line)
        # docpsongbook += line.encode('utf-8', 'xmlcharrefreplace')
        # docpsongbook += line.encode('utf-8', 'ignore')

        # import ipdb; ipdb.set_trace() #  noqa BREAKPOINT
        if i in idin:
            docpsongbook += "\\textbf{"
        try:
            docpsongbook += line.encode('utf-8')
        except:
            import ipdb; ipdb.set_trace() #  noqa BREAKPOINT

        if i in idin:
            docpsongbook += "}"
        docpsongbook += '\n'

            # docpsongbook += line
            # try:
            #     docpsongbook += line.encode('utf-8')
            # except:
            #     print line
            #     traceback.print_exc()
    #docpsongbook += '\\input{' + filepath + '}\n'
    docpsongbook += '\\end{alltt}\n'
    if not compact_version:
        docpsongbook += '\\newpage'
    return docpsongbook

def gentexfile(sngbk, filename = 'psongbook.tex', compact_version=False):
    head = u'\\documentclass{article}\n\
\\usepackage{a4wide}\n\
\\usepackage[czech]{babel}\n\
\\usepackage[utf8]{inputenc}\n\
\\usepackage[T1]{fontenc}\n\
\\usepackage{libertine}\n\
\\usepackage{alltt}\n\
\\begin{document}\n\
\\tableofcontents\n\
'

    docpsongbook = head.encode('utf-8')
    #pdb.set_trace()
    sngbkfilelist=sngbk['filelist']

    for part in sngbkfilelist.keys():
        try:

            prt = sngbkfilelist[part]
            for filepath in prt:
                fullfilepath = os.path.join(sngbk['dirpath'].decode('utf8'),
                                            part.decode('utf8'))
                fullfilepath = os.path.join(fullfilepath,filepath)
                docpsongbook += _gentexfile_for_one(fullfilepath, compact_version=compact_version)


        except:
            traceback.print_exc()
            import ipdb; ipdb.set_trace() #  noqa BREAKPOINT

    docpsongbook += '\\end{document}\n'

    logger.debug( docpsongbook)

    f = open(filename, 'w')
    #text = 'ahoj'

    docpsongbook = replace_latex_bad_character(docpsongbook)

    # import ipdb; ipdb.set_trace() #  noqa BREAKPOINT

    f.write(docpsongbook)
    f.close()


def replace_latex_bad_character(text):
    """
    :param text: string or list of strings
    :return:
    """

    if type(text) == list:
        new_text = []
        for line in text:
            new_text.append(_replace_latex_bad_character_one_string(line))
    else:
        new_text = _replace_latex_bad_character_one_string(text)

    return new_text


def _replace_latex_bad_character_one_string(docpsongbook):
    docpsongbook = docpsongbook.replace(u'\u0008'.encode('utf-8'), '')
    docpsongbook = docpsongbook.replace("°", '')
    docpsongbook = docpsongbook.replace("´", "'")
    docpsongbook = docpsongbook.replace('\xef\xbb\xbf','')
    # hard space into normal space
    docpsongbook = docpsongbook.replace(' ',' ')
    docpsongbook = docpsongbook.replace('$','\$')
    docpsongbook = re.sub(r"(.[^\\])&", r"\1\\&", docpsongbook)
    # docpsongbook = re.sub(r"(.[^\\])\$", r"\1\$", docpsongbook)
    return docpsongbook


def genpdffile(fullfilename):
    
    proc=subprocess.Popen(shlex.split('pdflatex '+fullfilename))
    proc.communicate()
    filename, fileextension = os.path.splitext(fullfilename)
    os.unlink(filename + '.log')


def sngbk_from_file(filename = 'sngbk.yaml'):
    import yaml
    stream = open(filename, 'r')
    sngbk = yaml.load(stream)
    #print sngbk
    return sngbk



def sngbk_to_file(sngbk, filename = 'sngbk.yaml'):
    #import json
    #with open(filename, mode='w') as f:
    #    json.dump(annotation,f)

    # write to yaml

    import yaml
    f = open(filename, 'w')
    yaml.dump(sngbk,f)
    f.close


def generate_example(path=""):
    import os
    import os.path as op

    if not os.path.exists(path):
        os.makedirs(path)



    text = u'Saxana - z filmu Saxana\n\
\n\
   A D A   F#mi                   E\n\
1: Saxano, v knihách vázaných v kůži\n\
   A  D A  F#mi     E      A\n\
   Zapsáno kouzel jevíc než dost\n\
   A D A   F#mi                  E\n\
   Saxano, komu dech se z nich úží\n\
   A D A   F#mi     E      A\n\
   Saxano, měl by si říct už dost!\n\
\n\
   A7              C7\n\
   Cizími slovy ti jedna z nich poví\n\
      D7\n\
   Že muži se loví\n\
       F7      G7       E7\n\
   Buď pan admirál nebo král\n\
   A7               C7\n\
   Vem oko soví, pak dvě slzy vdovy\n\
      D7\n\
   To svař a dej psovi\n\
       F7       G7      E7\n\
   Co vyl a byl sám opodál\n\
 \n\
2: Saxano, v knihácha vázaných v kůži \n\
   Zapsáno kouzel je na tisíc \n\
   Saxano, v jedné jediné růži \n\
   Saxano, kouzel je mnohem víc\n\
\n\
   Seď chvíli tiše a pak hledej spíše\n\
   Kde ve všem se píše \n\
   Že tát bude sníh, loňský sníh\n\
   Najdeš tam psáno, jak změnit noc v ráno\n\
   Jak zakrýt ne ano \n\
   A pláč v nocích zlých, změnit v smích \n\
\n\
1: Saxano ... (Jen první část)\n\
'
    sax_fn = op.join(path,"saxana.txt")
    sb_fn = op.join(path,"sngbk.yaml")

    f = open(sax_fn, 'w')
    #text = 'ahoj'
    f.write(text.encode('utf-8')) 
    f.close()

    sngbk = {u'dirpath'.encode('utf8'): path, 'filelist': {u'.'.encode('utf8'):[sax_fn.encode('utf8')]}}
    sngbk_to_file(sngbk, filename=sb_fn)


def get_parser(parser=None):
    import argparse
    if parser is None:
        parser = argparse.ArgumentParser(description='Process some chord file...')
    parser.add_argument('sngbk', type=str, default='sngbk.yaml', \
                        nargs='?', \
                        help='file with list of all chord files')
    # parser.add_argument('files', metavar='N', type=str, nargs='+',
    #        help='input text files with song chords')
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-c', '--compact-version', action='store_true')
    parser.add_argument('-id', '--inputdir', type=str, default=None, \
                        help='input directory')
    parser.add_argument('-o', '--output', type=str, default='psongbook.tex', \
                        help="output tex file")
    parser.add_argument('-e', '--example', action='store_true', \
                        help='generate example chord file')

    return parser

def main():
    import sys
    import Tkinter

    logger.setLevel(logging.ERROR)
    ch = logging.StreamHandler()
    logger.addHandler(ch)

    logger.debug('input params')

    parser = get_parser()
    args = parser.parse_args()

    #print args
    main_args(args)

def main_args(args):

    if args.debug:
        logger.setLevel(logging.DEBUG)

    if args.example:
        generate_example()
        sys.exit()

    if args.inputdir is not None:
        sngbky = genfilelist(args.inputdir)
        sngbk_to_file(sngbky, args.sngbk)

        # args.

    sngbk = sngbk_from_file(args.sngbk)
    #print sngbk
    gentexfile(sngbk, args.output, compact_version=args.compact_version)
    genpdffile(args.output)





if __name__ == "__main__":
    main()
