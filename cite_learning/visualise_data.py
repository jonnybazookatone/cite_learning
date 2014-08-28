#!/usr/bin/env python

"""
 X
"""

__author__ = "Jonathan Elliott"
__copyright__ = "Copyright 2014"
__credits__ =  "Dr. Vladimir Sudilovsky"
__version__ = "1.0"
__email__ = "jonnynelliott@googlemail.com"
__status__ = "Development"

import matplotlib
#matplotlib.use("TKAgg")
import matplotlib.pyplot as plt
import numpy

from cite_lib import check_content, svd_pca

def main():

  # Define arrays and variables
  feature_matrix, measured_matrix = [], []

  # Load in the full database
  print "Loading data from SQL database..."
  out1 = check_content(dbin="cilrn.db", search="PubYear,LengthOfAbstract,LengthOfTitle,NumberOfAuthors")
  out2 = check_content(dbin="cilrn.db", search="CitationCount")


  # Create an array
  for entry in out1:
    feature_matrix.append([j for j in entry])

  for entry in out2:
    measured_matrix.append([j for j in entry])

  feature_matrix = numpy.array(feature_matrix)
  measured_matrix = numpy.array(measured_matrix)

  print "...loaded feature matrix:\n"
  print "Number of data entries (rows): %d\nNumber of features (columns):  %d" % feature_matrix.shape

  print "Deconstructing into 2 dimensions with PCA..."

  M = numpy.concatenate((feature_matrix, measured_matrix), axis=1)
  z, d = svd_pca(M, k=4)
  print "Variances: %s" % d
  print "New size: %d x %d" % z.shape

  # Load figure canvas
  fig = plt.figure(0)
  ax1 = fig.add_subplot(321)
  ax2 = fig.add_subplot(322)
  ax3 = fig.add_subplot(323)
  ax4 = fig.add_subplot(324)
  ax5 = fig.add_subplot(325)

  ax1.errorbar(z[:,0], measured_matrix, fmt="o", color="blue")
  ax1.set_xlabel("PC1")
  ax1.set_ylabel("Citation count")

  ax2.errorbar(z[:,1], measured_matrix, fmt="o", color="red")
  ax2.set_xlabel("PC2")
  ax2.set_ylabel("Citation count")

  ax3.errorbar(z[:,2], measured_matrix, fmt="o", color="green")
  ax3.set_xlabel("PC3")
  ax3.set_ylabel("Citation count")

  ax4.errorbar(z[:,3], measured_matrix, fmt="o", color="black")
  ax4.set_xlabel("PC4")
  ax4.set_ylabel("Citation count")

  ax5.errorbar(z[:,0], measured_matrix, fmt="o", color="cyan")
  ax5.set_xlabel(r"$x_{1}$")
  ax5.set_ylabel(r"$x_{2}$")

  plt.show()



if __name__=='__main__':
  main()
