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
import pandas as pd

#----------------------------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	""" Move from the specified directory the filenames found in the input tsv file.
	"""
	parser = argparse.ArgumentParser("Move from the specified directory the filenames found in the input tsv file.")
	parser.add_argument('-tsv', '--tsv', action="store", required=True, help="Tsv file with the .prob filenames in the first column.")
	parser.add_argument('-i', '--input', action="store", required=True, help="Directory from which the files will be deleted.")
	parser.add_argument('-o', '--output', action="store", required=True, help="Directory where the files will be copied.")
	args = parser.parse_args()

	# Arguments Validations
	if ( not os.path.isfile( args.tsv ) ):
		print('Error: The tsv file was not found.\n')
		parser.print_help()
		sys.exit(1)

	if ( not os.path.isdir( args.input ) ):
		print('Error: The input directory of probability files was not found.\n')
		parser.print_help()
		sys.exit(1)

	if not os.path.exists( args.output ):
		try:
			os.makedirs( args.output )  
		except:
			print('Error: The destination directory was not found and could not be created.\n')
			parser.print_help()
			sys.exit(2)

	df = pd.read_csv( args.tsv, sep='\t', header=None)
	for index, row in df.iterrows():
		filename = row[0][:-4] + "jpg"
		shutil.move( args.input + "/" + filename, args.output + "/" + filename )
