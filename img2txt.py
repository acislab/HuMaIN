#!/usr/bin/python

###########################################################################################
# This script executes the Binarization, Segmentation, and Character recognition process
# of ocropy. It generates a text file with the recognized text.
# Execution format:
# python img2txt.py <source_file> <dest_folder>
#
# Developed by Icaro Alzuru.
# October 2015.
# ACIS Lab, University of Florida
###########################################################################################

import sys, os, subprocess

dirOcropy = "/root/ocropy"

############################# Validations #################################################
# Verification of the number of parameters and help
if len(sys.argv) != 3:
	print("Error: Invalid number of parameters")
	print("Use: python img2txt.py <source_file> <dest_folder>\n")
	sys.exit()

filename = sys.argv[1]
dstFolder = sys.argv[2]

# The existence of the source file is verified
if ( not os.path.isfile(filename)):
	print("Error: File %s was not found" % (filename))
	sys.exit()

# The existence of the destination folder is verified or created
if ( not os.path.isdir( dstFolder )):
	subprocess.call(["mkdir -p " + dstFolder], shell=True)
	if ( not os.path.isdir( dstFolder )):
		print("Error: Destination folder %s could not be created" % (dstFolder))
		sys.exit()

# The existence of the ocropy folder is verified
if ( not os.path.isdir(dirOcropy)):
	print("Error: Ocropy folder %s was not found" % (dirOcropy))
	sys.exit()
##########################################################################################

### Binarization
c = dirOcropy + "/ocropus-nlbin -n " + filename + " -o " + dstFolder
r = subprocess.call([c], shell=True)
if r != 0:
	print("Error: Binarization process failed")
	sys.exit()
	
### Segmentation
c = dirOcropy + "/ocropus-gpageseg -n " + dstFolder + "/0001.bin.png"
r = subprocess.call([c], shell=True)
if r != 0:
	print("Error: Segmentation process failed")
	sys.exit()

### Character Recognition
c = dirOcropy + "/ocropus-rpred -m en-default.pyrnn.gz " + dstFolder + "/0001/*.png"
r = subprocess.call([c], shell=True)
if r != 0:
	print("Error: Character recognition process failed")
	sys.exit()

### All text
name1 = filename.split("/")[-1]
name = name1.split(".")[0]
c = "cat " + dstFolder + "/0001/??????.txt > " + dstFolder + "/" + name + ".txt" 
r = subprocess.call([c], shell=True)


