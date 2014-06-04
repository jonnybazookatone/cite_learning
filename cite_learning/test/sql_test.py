#!/usr/bin/python
"""Default python script layout."""

import sys
import sqlite3 as lite

__author__ = "Jonny Elliott"
__copyright__ = "Copyright 2013"
__credits__ =  ""
__license__ = "GPL"
__version__ = "0.0"
__maintainer__ = "Jonny Elliott"
__email__ = "jonnyelliott@mpe.mpg.de"
__status__ = "Prototype"

def make_table():

  try:
    con = lite.connect('test.db')

    with con:
      cur = con.cursor()
      cur.execute("CREATE TABLE Copied (Id INTEGER PRIMARY KEY, Path TEXT);")
      # Layout: ID number, 
      path = ("\'Test path\'",)
      cur.execute("INSERT INTO Copied(Path) VALUES (?);", path)

  except lite.Error, e:  
    if con:
      con.rollback()  
      print "Error %s:" % e.args[0]
      sys.exit(1)

  finally:  
    if con:
      con.close() 

def add_content(intuple, dbin="cilrn.db"):
  con = lite.connect(dbin)
  with con:
    con.execute("INSERT INTO CiteLearning(BibCode,CitationCount,PubYear,LengthOfAbstract,LengthOfTitle,NumberOfAuthors) VALUES (?,?,?,?,?,?);", (intuple))
  con.commit()

def remove_content(dbin="cilrn.db"):
  con = lite.connect('cilrn.db')
  with con:
    con.execute("DELETE FROM CiteLearning;")
    con.commit()

def check_content(dbin="cilrn.db"):

  con = lite.connect(dbin)
  with con:
    con.row_factory = lite.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM CiteLearning")

    for i in cur.fetchall():
      print i

if __name__ == "__main__":


  indb = "/diska/home/jonny/sw/python/cite_learning/cite_learning/cilrn.db"
  make_check = False
  use_check = True
  delete_content = False

  if make_check:
    #  make_table()
    indi = {"BibCode": "BibCode", "CitationCount": 10, "PubYear": 2015.0, "LengthOfAbstract": 100, "LengthOfTitle": 100, "NumberOfAuthors": 10}
    intuple = (indi["BibCode"], indi["CitationCount"], indi["PubYear"], indi["LengthOfAbstract"], indi["LengthOfTitle"], indi["NumberOfAuthors"])
    print "Making content (4 rows)"
    for i in range(1,5):
      add_content(intuple, indb)
    print "Checking content"
    check_content(indb)
    print "Deleting content"
    remove_content(indb)
    print "Checking content"
    check_content(indb)

  if use_check:
    check_content(indb)

  if delete_content:
    print "First content:"
    check_content(indb)
    remove_content(indb)
    print "New content:"
    check_content(indb)

# Tue Apr 29 15:49:32 CEST 2014
