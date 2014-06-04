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
matplotlib.use("TKAgg")
import matplotlib.pyplot as plt
import numpy

from cite_lib import check_content

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

  feature_matrix, mean, std = feature_scaling(feature_matrix)
  print "Feature matrix mean: %s"  % mean
  print "Feature matrix standard deviation: %s" % std

  # Add the bias or zero-th value
  bias_matrix = numpy.ones((feature_matrix.shape[0],1))
  feature_matrix = numpy.concatenate((bias_matrix, feature_matrix), axis=1)

  print "...loaded feature matrix:\n"
  print "Number of data entries (rows): %d\nNumber of features (columns):  %d" % feature_matrix.shape


  # Machine Learning
  # Linear Regression - albeit the data does not look so linear by itself
  # Parameter matrix
  parameter_matrix = numpy.ones((feature_matrix.shape[1], 1))
  print "Parameter matrix (rows):       %d\n              (columns):       %d" % parameter_matrix.shape


  print "Calculating the cost function..."
  J_theta = cost_function(feature_matrix, parameter_matrix, measured_matrix)
  print "...J(theta): %f" % J_theta

  print "Gradient descent..."
  print "initial theta: %s" % parameter_matrix.T
  for i in range(1,200):
   
    parameter_matrix = gradient_descent(feature_matrix, parameter_matrix, measured_matrix, alpha=0.1)
    J_theta = cost_function(feature_matrix, parameter_matrix, measured_matrix)
 
    print "   i: %d" % i
    print "   theta: %s" % parameter_matrix.T
    print "   cost: %f" % J_theta
    print ""
  print "...end"
  # Load figure canvas

  fig = plt.figure(0)
  ax1 = fig.add_subplot(111)
  ax1.errorbar(feature_matrix[:,3], measured_matrix, fmt="o", color="blue")
  ax1.set_xlabel("Publication year")
  ax1.set_ylabel("Citation count")

  plt.show()

  

if __name__=='__main__':
  main()
