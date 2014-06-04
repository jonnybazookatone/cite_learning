#!/usr/bin/env python

'''
------
This script collects the important details from the excel spreadsheet and creates an SQL database
to be queried by the other scripts. Otherwise irrelevant details have to be computed everytime.
------

Pulled from Vlad's software: https://github.com/vsudilov/vss-flask/blob/master/utils/make_db.py

Header information in the Excel file:

text:u'BibCode'
text:u'CitationCount'
text:u'PubYear'
text:u'AuthorName'
text:u'AuthorRank'
text:u'Journal'
text:u'Telescope'
text:u'Affiliation'
text:u'Title'
text:u'Abstract'

Wanted output:

Citation count      
PubYear
Number of authors
Length of abstract
Length of title
'''

__author__ = "Jonathan Elliott"
__copyright__ = "Copyright 2014"
__credits__ =  "Dr. Vladimir Sudilovsky"
__version__ = "1.0"
__email__ = "jonnynelliott@googlemail.com"
__status__ = "Development"

import xlrd
import time
import numpy

from cite_lib import make_table, add_content, remove_content, check_content, sanitize

def main(db="/diska/home/jonny/sw/python/cite_learning/data/telbib-output.xlsx"):

  make_table(dbout="cilrn.db")

  print "Reading in the excel document"
  start = time.time()
  wb = xlrd.open_workbook(db)
  print "...done in %0.1f seconds" % (time.time()-start)
  ws = wb.sheet_by_index(0)
  header = ws.row(0)

  print header

  db_arr = {
           "BibCode": [],
           "CitationCount": [],
           "PubYear": [],
           "LengthOfAbstract": [],
           "LengthOfTitle": [],
           "NumberOfAuthors": [],
           "AuthorRank": [],
          }

  for i in range(ws.nrows-1):
    loadvalue = float(i)/ws.nrows*100.0
    if not round(loadvalue) % 10:
      print "Loading: %0.1f%%" % (loadvalue)
    row = ws.row(i+1)
    BibCode,CitationCount,PubYear,Author,AuthorRank,Journal,Telescope,Affiliation,Title,Abstract = [sanitize(j.value) for j in row]

    db_arr["CitationCount"].append(CitationCount)
    db_arr["PubYear"].append(PubYear)
    db_arr["LengthOfAbstract"].append(len(Abstract))
    db_arr["LengthOfTitle"].append(len(Title))
    db_arr["BibCode"].append(BibCode)
    db_arr["NumberOfAuthors"].append(0)
    db_arr["AuthorRank"].append(AuthorRank)

  # Convert to numpy arrays
  for item in db_arr:
    db_arr[item] = numpy.array(db_arr[item])

  # Calculate number of authors per bibcode
  for bibcode in list(set(db_arr["BibCode"])):
    idx = db_arr["BibCode"] == bibcode
   
    db_arr["NumberOfAuthors"][idx] = len(db_arr["BibCode"][idx])
    
    content = {}
    # Write a single entry for this BibCode
    for item in db_arr:
      content[item] = db_arr[item][idx][0]
    content_tuple = (content["BibCode"], content["CitationCount"], content["PubYear"], content["LengthOfAbstract"], content["LengthOfTitle"], content["NumberOfAuthors"])
    add_content(content_tuple, dbin="cilrn.db")

  print "Checking content....."
  print "---------------------"
  check_content(dbin="cilrn.db")
  print "---------------------"
  print "...finished checking."
     


  

if __name__=='__main__':
  main()
