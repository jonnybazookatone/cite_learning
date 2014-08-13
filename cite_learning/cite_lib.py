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

import numpy
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
  con.close()

def remove_content(dbin="cilrn.db"):
  con = lite.connect('cilrn.db')
  with con:
    con.execute("DELETE FROM CiteLearning;")
    con.commit()
  con.close()

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

  con.close()
  return out

# Excel spreadsheet parsing

def sanitize(value):
  if type(value)==unicode:
    return unicodedata.normalize('NFKD',value.replace(u'\xc3\xbc','ue')).encode('ascii', 'ignore') #Manually put "ue" in u-umlaut...Need to use a better solution eventually
  return value


###################
# Linear Regression

def gradient_descent(x, theta, y, alpha=0.3):

  # Normal gradient descent
  # m - number of entries
  # n - number of features

  m, n = x.shape
  theta -= (alpha/m) * numpy.dot((numpy.dot(theta.T, x.T).T - y).T, x).T

  return theta


def cost_function(x, theta, y):
  
  # Assumes a linear combination: f(x) = x1*theta1 + x2*theta2 + .... + xn*thetan
  # m - number of entries
  # n - number of features
  m, n = x.shape

  j = ((1./(2.*m)) * (h_x(x, theta) - y) ** 2.).sum()

  return j


def h_x(x, theta):
  
  h_x = numpy.dot(theta.T, x.T).T
  return h_x

  
def feature_scaling(x):

  x_mean = numpy.mean(x, axis=0)
  x_std = numpy.std(x, axis=0)

  x -= x_mean
  x /= x_std

  #print "Feature mean (average): %s" % x_mean.T
  #print "Feature standard deviation: %s" % x_std.T

  return x, x_mean, x_std

##############################
# Principal Component Analysis

def svd_pca(X, k=2):

  # Convert input array into matrix 
  Xorig = numpy.matrix(X)

  # Normalise and scale
  X = (Xorig - Xorig.mean(0)) / (Xorig.std(0))
  m, n = X.shape
  print "\nCreating initial matrix"
  print "Matrix X.shape: %sx%s\n" % X.shape

  # Create the covariance matrix - see notes on SVD
  #Sigma = (1/m) * (X.T * X)
  #print "Creating co-variance matrix"
  #print "Sigma S.shape: %sx%s\n" % Sigma.shape

  # Single Value Decomposition
  U, S, V = numpy.linalg.svd(X.T, full_matrices=True, compute_uv=True)

  # Deconstruction 2D -> 1D
  print "Determining U vector from SVD"
  print "Matrix U, shape: %sx%s\n" % U.shape

  z = (U[:,0:k].T * X.T).T
  zorig = z

  # Rescale and renormalise
  print "Scaling and normalising back to original format"
  print "Matrix z, shape: %sx%s\n" % z.shape
  z = numpy.multiply(z, Xorig.std(0)[:,0:k]) + Xorig.mean(0)[:,0:k]
  x_approx = numpy.multiply(zorig*U[:,0:k].T, Xorig.std(0)) + Xorig.mean(0)

  z = numpy.array(z)
  # For now, let's just return the decomposed dimensions
  return z, S #, x_approx, zorig, Xorig, U









###################
# Data sets to test

# Vlad's ESO data

def load_data_vlad():

  # Define arrays and variables
  feature_matrix, measured_matrix = [], []

  # Load in the full database
  print "Loading data from SQL database..."
  out1 = check_content(dbin="cilrn.db", search="PubYear,LengthOfAbstract,\
                       LengthOfTitle,NumberOfAuthors")
  out2 = check_content(dbin="cilrn.db", search="CitationCount")

  # Create an array
  for entry in out1:
    feature_matrix.append([j for j in entry])

  for entry in out2:
    measured_matrix.append([j for j in entry])

  feature_matrix = numpy.array(feature_matrix)
  measured_matrix = numpy.array(measured_matrix)

  return feature_matrix, measured_matrix


# Kiplinger's school data: http://www.kiplinger.com/tool/college/T014-S001-kiplinger-s-best-values-in-private-colleges/index.php

def load_data_kiplingers():
  ofile = open("schools.txt", "r")
  lines = ofile.readlines()
  ofile.close()

  M_output = []

  for i in range(len(lines)):
    j = [k for k in lines[i].strip().replace(",","").split(" ") if k]
    name = " ".join(j[1:-9])
    relevant = j[-9:-1]

    # Relevant: ['TX', '17', '6', '84', '52,741', '31,820', '12,068', '26']
    temp_arr = [name] + relevant

    temp_arr = [float(temp_arr[h]) for h in range(len(temp_arr)) if h>1]

    M_output.append(temp_arr)

  M_output = numpy.array(M_output)

  return M_output









if __name__ == "__main__":
  print __doc__
