#! /usr/bin/python
# -*- coding: utf-8 -*-

# import funkcí z jiného adresáře
import sys
import subprocess
import shlex
import os
#sys.path.append("../src/")

import logging
logger = logging.getLogger(__name__)

import pdb
#pdb.set_trace()
#import scipy.io
#mat = scipy.io.loadmat('step0.mat')

#print mat


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

    for part in sngbk.keys():
        prt=sngbk[part]
        for filepath in prt:
            docpsongbook += '\n\\begin{alltt}\n'

            fl = open(filepath, 'r')
            for line in fl:
                #print line
                line = line.decode('utf-8')
                logger.debug(line)
                docpsongbook += line#.encode('utf-8')
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

    sngbk = {u'pohadky':['saxana.txt']}
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
    parser.add_argument('-o', '--output', type=str, default='psongbook.tex', \
            help='output file') 
    parser.add_argument('-e', '--example', action='store_true',\
            help='generate example chord file')
    args = parser.parse_args()

    #print args


    if args.debug:
        logger.setLevel(logging.DEBUG)

    if args.example:
        generate_example()
        sys.exit()
        
    sngbk = sngbk_from_file(args.sngbk)
    #print sngbk
    gentexfile(sngbk, args.output)
    genpdffile(args.output)



