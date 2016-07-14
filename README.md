sobo
=========

Song book creator written in python. Input is a directory with `.txt` files. Output is one pdf file.

[Example of output songbook](https://www.dropbox.com/s/t8xbr9qhtt7wuc8/psongbook.pdf?dl=0)


Prereq
======

sudo apt-get install python-yaml

Use
===

To generate pdf songbook use:


    python sobo sobo -id ~/Dropbox/akordy/nove-poradky
    


Every song in input data is stored into `.txt` file. First line of this file contain song name and artist namefile separated with dash symbol. 

    Song name - Artist Name (Optional Band)
    
    C     G    D
    This is text of song
    C        G      D
    This is second line
        
Files are organized into subdirectories based on genre. In genre are song sorted by artist name. 
Sorting algorithm use reverse order of words. This means that last name is used on first place. 
If there is text closed into round bracket order of words is not changed and text in braces is moved on begining of sorted string.

String for sorting from our previous example is then: `Optional Band Name Artist`
        
        

[Example of input data](https://www.dropbox.com/s/xrf9jkqwrjg2f5b/nove-poradky.zip?dl=0)

        