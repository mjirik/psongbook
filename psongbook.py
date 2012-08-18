#! /usr/bin/python
# -*- coding: utf-8 -*-

# import funkcí z jiného adresáře
import sys
#sys.path.append("../src/")

import logging
logger = logging.getLogger(__name__)

#import scipy.io
#mat = scipy.io.loadmat('step0.mat')

#print mat





def annotation_to_file(annotation, filename = 'annotation.json'):
    import json
    import yaml
    with open(filename, mode='w') as f:
        json.dump(annotation,f)

    # write to yaml

    f = open('annotation.yaml', 'w')
    yaml.dump(annotation,f)
    f.close


def generate_example():
    text = u'Saxana - z filmu Saxana\n\
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


if __name__ == "__main__":
    import sys
    import Tkinter
    import argparse

    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    logger.addHandler(ch)

    logger.debug('input params')

    parser = argparse.ArgumentParser(description='Process some chord file...')
    parser.add_argument('files', metavar='N', type=str, nargs='+',
            help='input text files with song chords')
    parser.add_argument('-D', '--debug', action='store_true')
    parser.add_argument('--output', type=str, default='psongbook.tex', \
            help='output file') 
    parser.add_argument('-e', '--example', action='store_true',\
            help='generate example chord file')
    args = parser.parse_args()

    print args


    if args.example:
        generate_example()
        
    for arg in sys.argv:
        logger.debug(''+arg)

    logger.debug('Adresar '  )
    #dm = Dialogmenu()
    #print dm.retval

    #filelist = training.filesindir('/home/mjirik/data/jatra-kiv/jatra-kma/jatra_5mm/','*.*')
    #traindata(filelist)

