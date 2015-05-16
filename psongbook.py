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
            #fl={'dirname': dirname, 'files':filesutf8}
            #filelist.append(fl)
            filelist[dirname]=filesutf8
        else:
            for file in fnmatch.filter(files, wildcards):
                filelist.append(os.path.join(root,file))
    #        
    print filelist
    #filelist = []
    #print dirpath

    #for infile in glob.glob( os.path.join(dirpath, wildcard) ):
    #    if startpath != None:
    #        infile = os.path.relpath(infile, startpath)
    #    filelist.append(infile)
        #print "current file is: " + infile

    sngbky = {'dirpath'.encode('utf8'): dirpath.encode('utf-8'), 'filelist'.encode('utf-8'):filelist }
    return sngbky

def gentexfile(sngbk, filename = 'psongbook.tex'):
    head = u'\\documentclass{article}\n\
\\usepackage{a4wide}\n\
\\usepackage[czech]{babel}\n\
\\usepackage[utf8]{inputenc}\n\
\\usepackage{alltt}\n\
\\begin{document}\n\
'

    docpsongbook = head#.encode('utf-8')
    #pdb.set_trace()
    sngbkfilelist=sngbk['filelist']

    for part in sngbkfilelist.keys():
        prt=sngbkfilelist[part]
        for filepath in prt:
            docpsongbook += '\n\\begin{alltt}\n'
            #pdb.set_trace()
            fullfilepath = os.path.join(sngbk['dirpath'].decode('utf8'),
                    part.decode('utf8'))
            fullfilepath = os.path.join(fullfilepath,filepath)


            fl = open(os.path.join(fullfilepath), 'r')
            for line in fl:
                #print line
                # TODO dection input coding
                # TODO replacement of bad characters like \u8
                try:
                    line = line.decode('utf-8')
                except:
                    try:
                        line = line.decode('cp1250')
                        print "cp 1250 " + fullfilepath
                    except:
                        print fullfilepath
                        traceback.print_exc()


                logger.debug(line)
                # docpsongbook += line.encode('utf-8', 'xmlcharrefreplace')
                # docpsongbook += line.encode('utf-8', 'ignore')
                # docpsongbook += line.encode('utf-8')
                docpsongbook += line
                # try:
                #     docpsongbook += line.encode('utf-8')
                # except:
                #     print line
                #     traceback.print_exc()
            #docpsongbook += '\\input{' + filepath + '}\n'
            docpsongbook += '\\end{alltt}\n'


    docpsongbook += '\\end{document}\n'

    logger.debug( docpsongbook)

    f = open(filename, 'w')
    #text = 'ahoj'
    f.write(docpsongbook.encode('utf-8')) 
    f.close()
        

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


def generate_example():
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
    f = open('saxana.txt', 'w')
    #text = 'ahoj'
    f.write(text.encode('utf-8')) 
    f.close()

    sngbk = {u'dirpath'.encode('utf8'): './', 'filelist': {u'.'.encode('utf8'):['saxana.txt'.encode('utf8')]}}
    sngbk_to_file(sngbk)


if __name__ == "__main__":
    import sys
    import Tkinter
    import argparse

    logger.setLevel(logging.ERROR)
    ch = logging.StreamHandler()
    logger.addHandler(ch)

    logger.debug('input params')

    parser = argparse.ArgumentParser(description='Process some chord file...')
    parser.add_argument('sngbk', type=str, default='sngbk.yaml', \
            nargs='?',\
            help='file with list of all chord files')
    # parser.add_argument('files', metavar='N', type=str, nargs='+',
    #        help='input text files with song chords')
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-id', '--inputdir', type=str, default=None, \
            help='input directory')
    parser.add_argument('-o', '--output', type=str, default='psongbook.tex', \
            help="output tex file") 
    parser.add_argument('-e', '--example', action='store_true',\
            help='generate example chord file')
    args = parser.parse_args()

    #print args


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
    gentexfile(sngbk, args.output)
    genpdffile(args.output)




