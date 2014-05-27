#!/usr/bin/env python

'''Pulled from Vlad's software: https://github.com/vsudilov/vss-flask/blob/master/utils/make_db.py'''

import xlrd
import time
import unicodedata

def sanitize(value):
  if type(value)==unicode:
    return unicodedata.normalize('NFKD',value.replace(u'\xc3\xbc','ue')).encode('ascii', 'ignore') #Manually put "ue" in u-umlaut...Need to use a better solution eventually
  return value

def main(db="/diska/home/jonny/sw/python/cite_learning/data/telbib-output.xlsx"):
  print "Reading in the excel document"
  start = time.time()
  wb = xlrd.open_workbook(db)
  print "...done in %0.1f seconds" % (time.time()-start)
  ws = wb.sheet_by_index(0)
  header = ws.row(0)

  print header

if __name__=='__main__':
  main()
