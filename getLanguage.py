#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys, os

# References:
# https://en.wikipedia.org/wiki/Most_common_words_in_English
# http://www.clarin.com/sociedad/palabras-mas-usadas-espanol-comunes-frecuentes-diccionario-Real_Academia_Espanola_0_1399660188.html

# The 10 most common word of every language that do not exist in other languages.
eng_l = ["the","to","of","and","in","that","have","it","for","not","on","with","he","as","you","do","at","this","but","his","by","from","they","we","say","her","she","or","an","will","my","one","all","would","there","their","what","so","up"]
spa_l = ["de","la","que","el","en","los","se","del","las","un","por","con","no","una","su","para","es","al","lo","como","más","pero","sus","le","ha","me","si","sin","sobre","este","ya","entre","cuando","todo","esta","ser","son","dos","también"]

##########################################################################################
def checkLanguage(filename):
	eng_n = 0
	spa_n = 0
	with open(filename,'r') as f:
		for line in f:
			for word in line.split():
				word = word.lower()
				if word in eng_l:
					eng_n = eng_n + 1
				elif word in spa_l:
					spa_n = spa_n + 1
	
	#print "Eng: " + str(eng_n) + "\n"
	#print "Spa: " + str(spa_n) + "\n"
	if spa_n > eng_n:
		return 0
	else:
		return 1


##########################################################################################
if __name__ == "__main__":
	############################# Validations ############################################
	# Verification of the number of parameters and help
	if len(sys.argv) != 2:
		print("Error: Invalid number of parameters")
		print("Use: python getLanguage.py <source_file>\n")
		sys.exit()

	filename = sys.argv[1]

	# The existence of the source file is verified
	if ( not os.path.isfile(filename)):
		print("Error: File %s was not found" % (filename))
		sys.exit()
		
	######################### Calling the function #######################################
	checkLanguage(filename)