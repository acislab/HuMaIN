#!/usr/bin/python

import sys, os
from PIL import Image


def die_with_usage():
    """ HELP MENU """
    print ''
    print 'Usage:'
    print '   python crop.py <filename> <x> <y> <width> <height> <output_file>'
    print ''   
    print 'Example:'
    print '   python /home/user1/blueSky1.jpg 340 12 100 150 cloud.jpg'
    print ''
    sys.exit(0)


def int_input(s):
    try:
        n = int(s)
        return n
    except ValueError:
        print "Error: ", s, "is not a valid integer.\n"
        die_with_usage()


if __name__ == '__main__':
    """ MAIN """
    # help menu
    if len(sys.argv) != 7:
        die_with_usage()
    
    # get params
    filename = sys.argv[1]
    x = int_input(sys.argv[2])
    y = int_input(sys.argv[3])
    width = int_input(sys.argv[4])
    height = int_input(sys.argv[5])
    outfname = sys.argv[6]
    
    # sanity check
    if not os.path.isfile(filename):
        print '\nERROR: source file', filename, 'does not exist.\n'
        die_with_usage()
    
    image = Image.open(filename)
    box = (x, y, x + width, y + height)
    new_image = image.crop( box )
    new_image.save( outfname )
