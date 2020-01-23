#!/usr/bin/env python

import sys, os, re

############################# Validations #################################################
# Verification of the number of parameters and help
if len(sys.argv) != 2:
	print("Error: Invalid number of parameters")
	print("Use: python getDate.py <source_file>\n")
	sys.exit()

filename = sys.argv[1]

# The existence of the source file is verified
if ( not os.path.isfile(filename)):
	print("Error: File %s was not found" % (filename))
	sys.exit()

##########################################################################################

pattern1 = re.compile(r'[A-Za-z]+ [0-9]+, [0-9]+', flags = re.I)
pattern2 = re.compile(r'[0-9]+ [A-Za-z]+ [0-9]+', flags = re.I)

with open(filename,'r') as f:
	for line in f:
		result = pattern1.search(line)
		if result is not None:
			print result.group()
		else:
			result = pattern2.search(line)
			if result is not None:
				print result.group()

        