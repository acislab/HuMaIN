#!/usr/bin/python

import sys, os, subprocess, time, PIL
from PIL import Image

def die_with_usage():
	""" HELP MENU """
	print ''
	print 'usage:'
	print '   python resizeImg.py <src_image> <dst_image>'
	print 'example:'
	print '   python resizeImg.py /root/user1/EMEC609590_Cerceris_compacta.jpg /root/user1/EMEC609590.jpg'
	print ''
	sys.exit(0)

if __name__ == '__main__':
	""" MAIN """
	# help menu
	if len(sys.argv) != 3:
		die_with_usage()

	# get params
	src_filename = sys.argv[1]
	dst_filename = sys.argv[2]
    
	# sanity check
	if not os.path.isfile(src_filename):
		print '\nERROR: source image', src_filename, ' not found.\n'
		die_with_usage()
        
	#
	src_img = Image.open(src_filename)

	width = src_img.size[0]
	height = src_img.size[1]

	if (width >= height):
		if ( height < 600 ):
			width = int(round( 600 * float(width) / height ))
			dst_img = src_img.resize( (width, 600), PIL.Image.ANTIALIAS)
			dst_img.save(dst_filename)
	else:
		if ( width < 600 ):
			height = int(round( 600 * float(height) / width ))
			dst_img = src_img.resize( (600, height), PIL.Image.ANTIALIAS)
			dst_img.save(dst_filename)

