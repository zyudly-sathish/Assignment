#!/usr/bin/python3

import re
import os
import csv
import string
import sys
import fileinput
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

#directory where the files reside
indir = '/home/sathisha/pythonexamples/'

def main():
	#number of times to be iterated
	i = 1000
    	j = 0
    	while (j < i):
		
		ifile = open(indir + 'suppliers_data.csv', "rb")
		reader = csv.reader(ifile)
	 	
		#mapped data output file
		mfile = open(indir + 'mappedHotels.csv', "a")

		#inv_ids to be zeroed out after processing stored in this array
		inv_id_arr = []
		
		#few parameters to be initialized which acts as counters
		rownum = 0
		newrownum = j + 1
		origname = ""
		
		#following steps to read the data row by row and find the matching inv_name
		#and write to the mappedHotels.csv
		#Note : when matching the names fuzzy logic is being utilized.
		for row in reader:
			if rownum > j:
				oldrownum = rownum
				colnum = 0
				
				for col in row:
					#zerored out columns which means already processed should not processed again
					if (col != '0'):
						if (colnum == 0):
							dupinv_id = col							
							if rownum==newrownum:
								#to obtain the first hq_id from the inv_id which
								#will be used subsequently 						
								hq_id = col
								inv_id = col
					
						if (colnum == 1):
							dup_supplier = col
							if rownum==newrownum:
								#write the initial value to mappedHotels.csv
								supplier = col
								writer = csv.writer(mfile, delimiter='|', quotechar='"', quoting=csv.QUOTE_ALL)
								writer.writerow([hq_id,inv_id,supplier])
								inv_id_arr.append(inv_id)

						if (colnum == 2):
							if oldrownum == newrownum:
								origname = col
							elif (origname.lower() == col.lower()) or (fuzz.ratio(origname.lower(), col.lower()) == 100):
								#in above condition fuzzy logic being utilzed								
								writer.writerow([hq_id,dupinv_id,dup_supplier])
								inv_id_arr.append(dupinv_id)
							
						colnum+=1
			rownum = rownum + 1
		
	 	mfile.close()
		ifile.close()
	
		#This routine replace the already processed rows with zero in suppliers_data.csv
		for x in inv_id_arr:
			
			textToSearch = x
			
			textToReplace = '0'
			
			fileToSearch = indir + 'suppliers_data.csv'

			tempFile = open( fileToSearch, 'r+' )

			for line in fileinput.input( fileToSearch ):
		    		#replace the inv_id with zero
		    		tempFile.write( line.replace( textToSearch, textToReplace ) )
			tempFile.close()
		j = j + 1
		print(j)


if __name__ == "__main__":
    main()
