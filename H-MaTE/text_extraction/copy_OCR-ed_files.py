#!/usr/bin/env python3
##########################################################################################
# Developer: Icaro Alzuru         Project: HuMaIN (http://humain.acis.ula.ve)
##########################################################################################
# Copyright 2019    Advanced Computing and Information Systems (ACIS) Lab - UF
#                   (https://www.acis.ufl.edu/)
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##########################################################################################
import argparse, os, sys, shutil
from shutil import copyfile

#----------------------------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	""" Copy the .txt and .prob files from one directory to another, given the .jpg files found in the reference directory.
	"""
	parser = argparse.ArgumentParser("Copy the .txt and .prob files from one directory to another, given the .jpg files found in the reference directory.")
	parser.add_argument('-r', '--reference', action="store", required=True, help="Directory with the .jpg which derived files will be copied.")
	parser.add_argument('-i', '--input', action="store", required=True, help="Directory where the .txt and .prob files are located.")
	parser.add_argument('-o', '--output', action="store", required=True, help="Destination directory where the files will be copied.")
	args = parser.parse_args()

	# Arguments Validations
	if ( not os.path.isdir( args.reference ) ):
		print('Error: The directory used as reference, with the .jpg files, was not found.\n')
		parser.print_help()
		sys.exit(0)

	if ( not os.path.isdir( args.input ) ):
		print('Error: The input directory of probability and text files was not found.\n')
		parser.print_help()
		sys.exit(1)

	if not os.path.exists( args.output ):
		try:
			os.makedirs( args.output )  
		except:
			print('Error: The destination directory was not found and could not be created.\n')
			parser.print_help()
			sys.exit(2)

	# Create the list of files to process
	filename_list = list()
	for root, dirs, filenames in os.walk( args.reference ):
		filename_list = list(f for f in filenames if f.endswith('.jpg'))

	# Execution
	for filename in filename_list:
		basename = filename[:-4]
		# Text file
		try:
			src_path_filename = args.input + "/" + basename + ".txt"
			dst_path_filename = args.output + "/" + basename + ".txt"
			copyfile(src_path_filename, dst_path_filename)
			# Probabilities file
			src_path_filename = args.input + "/" + basename + ".prob"
			dst_path_filename = args.output + "/" + basename + ".prob"
			copyfile(src_path_filename, dst_path_filename)
		except:
			continue
