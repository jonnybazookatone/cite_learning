#!/usr/bin/env python

'''Pulled from Vlad's software: https://github.com/vsudilov/vss-flask/blob/master/utils/make_db.py

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
Number of telescopes

'''

import sqlite3 as lite
import sys
import xlrd
import time
import unicodedata
import numpy

def make_table(dbout="cilrn.db"):
  try:
    con = lite.connect(dbout)

    with con:
      cur = con.cursor()
      cur.execute("CREATE TABLE CiteLearning (Id INTEGER PRIMARY KEY, BibCode TEXT, CitationCount INTEGER, PubYear INTEGER, LengthOfAbstract INTEGER, LengthOfTitle INTEGER, NumberOfAuthors INTEGER);")

  except lite.Error, e:
    if con:
      con.rollback()
      print "Error %s:" % e.args[0]
      pass

  finally:
    if con:
      con.close()

def add_content(inDictionary, dbin="cilrn.db"):
  con = lite.connect(dbin)
  with con:
    con.execute("INSERT INTO CiteLearning(BibCode,CitationCount) VALUES (?),(?);", (inDictionary["BibCode"], inDictionary["CitationCount"]))
  con.commit()

def check_content(dbin="cilrn.db"):

  con = lite.connect(dbin)
  with con:
    con.row_factory = lite.Row
    cur = con.cursor() 
    cur.execute("SELECT BibCode FROM CiteLearning")

    rows = [i[0] for i in cur.fetchall()]
    print rows

def sanitize(value):
  if type(value)==unicode:
    return unicodedata.normalize('NFKD',value.replace(u'\xc3\xbc','ue')).encode('ascii', 'ignore') #Manually put "ue" in u-umlaut...Need to use a better solution eventually
  return value

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

    if i == 20:
      break

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
      print content

    add_content(content, dbin="cilrn.db")
    print "\n\n"

  check_content(dbin="cilrn.db")
     


  

if __name__=='__main__':
  main()
