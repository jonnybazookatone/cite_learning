#!/usr/bin/env python

"""
Library to be used with CiteLearning pipeline.
"""

__author__ = "Jonathan Elliott"
__copyright__ = "Copyright 2014"
__credits__ =  "Dr. Vladimir Sudilovsky"
__version__ = "1.0"
__email__ = "jonnynelliott@googlemail.com"
__status__ = "Development"

import sqlite3 as lite
import unicodedata

# SQL scripting

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

def check_content(dbin="cilrn.db", search="*"):

  con = lite.connect(dbin)
  with con:
    con.row_factory = lite.Row
    cur = con.cursor()
    cur.execute("SELECT %s FROM CiteLearning" % search)

    out = cur.fetchall()
    silent = True
    if not silent:
      for i in out:
        print i

  return out

# Excel spreadsheet parsing

def sanitize(value):
  if type(value)==unicode:
    return unicodedata.normalize('NFKD',value.replace(u'\xc3\xbc','ue')).encode('ascii', 'ignore') #Manually put "ue" in u-umlaut...Need to use a better solution eventually
  return value


if __name__ == "__main__":
  print __doc__
