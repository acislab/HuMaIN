#!/usr/bin/env python
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
import argparse, os, sys
from pyzbar import pyzbar
import cv2, math, multiprocessing
import numpy as np
import pandas as pd

CORES_N = multiprocessing.cpu_count()
SRC_DIR = ""
DST_DIR = ""

def delBarRuler ( filename ):
	src_filename = SRC_DIR + "/" + filename
	# Load the image
	img_original = cv2.imread( src_filename, cv2.IMREAD_UNCHANGED )
	image = img_original.copy()
	#########################################################################################################################
	# Find and remove rulers (Manual Procedure)

	# Filter some noise or garbage
	img = cv2.blur(img_original,(7,7))

	# Convert the image to B/W (8 bits)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	# Edge detection
	edges = cv2.Canny(gray, 75, 150) # More garbage but includes more edges (good and bad)

	#Create default parametrization LSD
	lsd = cv2.createLineSegmentDetector(0)
	#Detect lines in the image
	lines = lsd.detect( edges )[0]

	# Detect the angle of the lines and group the lines using the angle
	line_dict = dict()
	for l in lines:
		x0, y0, x1, y1 = l.flatten()
		# Angle estimation rounded to one decimal position
		angle = round((math.atan2( y0-y1, x1-x0 ))/15, 1)
		# Consider only lines of more than 20 pixels
		length = math.sqrt( (x0-x1)**2 + (y0-y1)**2 )
		if length > 30: 
			if angle in line_dict:
				line_array = line_dict[ angle ]
				line_array.append( [x0, y0, x1, y1, length] )
				line_dict[ angle ] = line_array
			else:
				line_array = [ [x0, y0, x1, y1, length] ]
				line_dict[ angle ] = line_array


	for angle, line_array in line_dict.items():
		# print("Angulo:" + str(angle))
		n_l = len(line_array)
		# Considers only groups of 10 lines or more
		if n_l > 10:
			# Create a dataframe with the lines of the same angle
			df_lines = pd.DataFrame(line_array, columns=['x0', 'y0', 'x1', 'y1', 'length'] )
			# Order the lines by the first y coordinate value (in ascending order)
			df_lines.sort_values( ['y0'], ascending=[1], inplace=True)
			# Try to detect clusters of at least 10 lines (Cluster: lines with a distance < 10 pixels to the next line)
			df_cluster = pd.DataFrame(columns=['x0', 'y0', 'x1', 'y1'])
			df_cluster.loc[0] = [  df_lines['x0'].iloc[0], df_lines['y0'].iloc[0], df_lines['x1'].iloc[0], df_lines['y1'].iloc[0]  ]
			i_row = 1
			i_cluster = 1			
			while i_row < n_l:
				# If the vertical distance to the previous line is less than 10 pixels
				if ( (df_lines['y0'].iloc[ i_row ] - df_lines['y0'].iloc[ i_row - 1 ]) < 10 ):
					# Add the line to the cluster
					df_cluster.loc[ i_cluster ] = [  df_lines['x0'].iloc[i_row], df_lines['y0'].iloc[i_row], df_lines['x1'].iloc[i_row], df_lines['y1'].iloc[i_row]  ]
					i_cluster = i_cluster + 1
				else:
					# The construction of the cluster has finished
					if df_cluster.shape[0] >= 10: # If the cluster has at least 10 lines
						df_cluster.sort_values( ['x0'], ascending=[1], inplace=True)
						#######################################################################################
						# From the cluster, we create a kernel: vertical and horizontal alignment
						df_kernel = pd.DataFrame(columns=['x0', 'y0', 'x1', 'y1'])
						df_kernel.loc[0] = [  df_cluster['x0'].iloc[0], df_cluster['y0'].iloc[0], df_cluster['x1'].iloc[0], df_cluster['y1'].iloc[0]  ]
						j = 1
						i_kernel = 1
						while j < df_cluster.shape[0]:
							if ( (df_cluster['x0'].iloc[ j ] - df_cluster['x0'].iloc[ j - 1 ]) < 25 ):
								# Add the line to the kernel
								df_kernel.loc[ i_kernel ] = [  df_cluster['x0'].iloc[j], df_cluster['y0'].iloc[j], df_cluster['x1'].iloc[j], df_cluster['y1'].iloc[j]  ]
								i_kernel = i_kernel + 1
							else:
								# The construction of the kernel has finished
								if df_kernel.shape[0] >= 10: # If the kernel has at least 10 lines
									#==============================================================================
									# Convex Hull painting
									points = []
									for idx, row in df_kernel.iterrows():
										points.append( ( row['x0'], row['y0'] ) )
										points.append( ( row['x1'], row['y1'] ) )
									x1 = np.int32( np.array( points ) )
									x2 = cv2.UMat( x1 )
									filler = cv2.convexHull( x2 )
									x3 = cv2.UMat.get( filler )
									cv2.fillPoly(image, [x3], (255, 255, 255))
									# cv2.line(image, (int(row['x0']), int(row['y0'])), (int(row['x1']), int(row['y1'])), (0, 255, 0), 2)
									#==============================================================================

								# Initialize the kernel
								df_kernel.drop( df_kernel.index, inplace=True )
								df_kernel.loc[0] = [  df_cluster['x0'].iloc[j], df_cluster['y0'].iloc[j], df_cluster['x1'].iloc[j], df_cluster['y1'].iloc[j]  ]
								i_kernel = 1

							j = j + 1
						#######################################################################################

					# Initialize the cluster
					df_cluster.drop( df_cluster.index, inplace=True )
					df_cluster.loc[0] = [  df_lines['x0'].iloc[i_row], df_lines['y0'].iloc[i_row], df_lines['x1'].iloc[i_row], df_lines['y1'].iloc[i_row]  ]
					i_cluster = 1

				i_row = i_row + 1

			# Print the cluster in case it is big enough
			if df_cluster.shape[0] >= 10: # If the cluster has at least 10 lines
				df_cluster.sort_values( ['x0'], ascending=[1], inplace=True)
				#######################################################################################
				# From the cluster, we create a kernel: vertical and horizontal alignment
				df_kernel = pd.DataFrame(columns=['x0', 'y0', 'x1', 'y1'])
				df_kernel.loc[0] = [  df_cluster['x0'].iloc[0], df_cluster['y0'].iloc[0], df_cluster['x1'].iloc[0], df_cluster['y1'].iloc[0]  ]
				j = 1
				i_kernel = 1
				while j < df_cluster.shape[0]:
					if ( (df_cluster['x0'].iloc[ j ] - df_cluster['x0'].iloc[ j - 1 ]) < 25 ):
						# Add the line to the kernel
						df_kernel.loc[ i_kernel ] = [  df_cluster['x0'].iloc[j], df_cluster['y0'].iloc[j], df_cluster['x1'].iloc[j], df_cluster['y1'].iloc[j]  ]
						i_kernel = i_kernel + 1
					else:
						# The construction of the kernel has finished
						if df_kernel.shape[0] >= 10: # If the kernel has at least 10 lines
							#==============================================================================
							# Convex Hull painting
							points = []
							for idx, row in df_kernel.iterrows():
								points.append( ( row['x0'], row['y0'] ) )
								points.append( ( row['x1'], row['y1'] ) )
							x1 = np.int32( np.array( points ) )
							x2 = cv2.UMat( x1 )
							filler = cv2.convexHull( x2 )
							x3 = cv2.UMat.get( filler )
							cv2.fillPoly(image, [x3], (255, 255, 255))
							# cv2.line(image, (int(row['x0']), int(row['y0'])), (int(row['x1']), int(row['y1'])), (255, 255, 255), 2)
							#==============================================================================

						# Initialize the kernel
						df_kernel.drop( df_kernel.index, inplace=True )
						df_kernel.loc[0] = [  df_cluster['x0'].iloc[j], df_cluster['y0'].iloc[j], df_cluster['x1'].iloc[j], df_cluster['y1'].iloc[j]  ]
						i_kernel = 1

					j = j + 1
				#######################################################################################

	#########################################################################################################################
	# Find the barcodes in the image and decode them
	barcodes = pyzbar.decode( img_original )
	# Loop over the detected barcodes
	for barcode in barcodes:
		# extract the bounding box location and paint a white rectangle on it
		(x, y, w, h) = barcode.rect
		cv2.rectangle(image, (x-1, y-1), (x+w+1, y+h+1), (255, 255, 255), -1)

	#########################################################################################################################
	# Save the final image
	dst_filename = DST_DIR + "/" + filename
	cv2.imwrite( dst_filename, image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

#----------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	""" MAIN """
	parser = argparse.ArgumentParser("Detect and deletes the barcodes in the images of a directory. It replaces them with a white box.")
	parser.add_argument('-i', '--input', action="store", required=True, help="Directory where the jpg images are located.")
	parser.add_argument('-o', '--output', action="store", required=True, help="Directory where the new version of the images will be save. Only those where a bar code was found.")
	args = parser.parse_args()
	# Arguments Validations
	if ( not os.path.isdir( args.input ) ):
		print('Error: The directory of the jpg files was not found.\n')
		parser.print_help()
		sys.exit(1)

	if not os.path.exists( args.output ):
		try:
			os.makedirs( args.output )  
		except:
			print('Error: The destination directory was not found and could not be created.\n')
			parser.print_help()
			sys.exit(2)	

	SRC_DIR = args.input
	DST_DIR = args.output

	# Create the list of files to process
	filename_list = list()
	for root, dirs, filenames in os.walk( args.input ):
		filename_list = list(f for f in filenames if f.endswith('.jpg'))

	# Pool handler
	p = multiprocessing.Pool( CORES_N )
	p.map( delBarRuler, filename_list )

