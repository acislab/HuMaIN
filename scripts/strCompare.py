#!/usr/bin/python

import sys, os, subprocess
import time
from pyxdameraulevenshtein import normalized_damerau_levenshtein_distance


def die_with_usage():
    """ HELP MENU """
    print ''
    print 'Usage:'
    print '   python strCompare.py <gold_folder> <result_folder> <output_file>'
    print 'It assumes extension .txt for the files of folders <gold_folder> and <result_folder>'    
    print 'Example:'
    print '   python strCompare.py /root/label-data/ent/gold/ocr /root/Data/entResult cmp_ent.txt'
    print ''
    sys.exit(0)


if __name__ == '__main__':
    """ MAIN """
    # help menu
    if len(sys.argv) != 4:
        die_with_usage()

    # get params
    gold_folder = sys.argv[1]
    result_folder = sys.argv[2]
    filename = sys.argv[3]
    
    # sanity check
    if not os.path.isdir(gold_folder):
        print '\nERROR: source folder', gold_folder, 'does not exist.\n'
        die_with_usage()
        
    if not os.path.isdir(result_folder):
        print '\nERROR: source folder', result_folder, 'does not exist.\n'
        die_with_usage()
        
    f = open(filename,'w') 
        
    for root, dirs, files in os.walk(gold_folder):
        for file in files:
            if file.endswith(".txt"):
                baseFilename = file[:-4]
                gold_filename = gold_folder + "/" + file 
                result_filename = result_folder + "/" + baseFilename +"/" + file
                
                with open(gold_filename, 'r') as gfile:
                    gold_content = gfile.read()
                    #print gold_filename + "\n" + gold_content
                
                    try:
                        with open(result_filename, 'r') as rfile:
                            result_content = rfile.read()
                            #print result_filename + "\n" + result_content
        
                            a = normalized_damerau_levenshtein_distance(gold_content, result_content)
                            f.write( baseFilename + " " + str(a) + "\n")
                    except IOError:
                        f.write( baseFilename + " 2.0\n")
  
    f.close()

