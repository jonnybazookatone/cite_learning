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

from cite_lib import check_content, gradient_descent, \
                     cost_function, h_x, feature_scaling, \
                     load_data_vlad

def main():

  feature_matrix, measured_matrix = load_data_vlad()

  feature_matrix, mean, std = feature_scaling(feature_matrix)
  print "Feature matrix mean: %s"  % mean
  print "Feature matrix standard deviation: %s" % std

  # Add the bias or zero-th value
  bias_matrix = numpy.ones((feature_matrix.shape[0],1))
  feature_matrix = numpy.concatenate((bias_matrix, feature_matrix), axis=1)

  print "...loaded feature matrix:\n"
  print "Number of data entries (rows): %d\nNumber of features (columns):  %d" % feature_matrix.shape


  print "Randomly shuffling matrix..."
  shuffle_matrix = numpy.concatenate((measured_matrix, feature_matrix), axis=1)
  numpy.random.shuffle(shuffle_matrix)
  measured_matrix = numpy.array(shuffle_matrix[:,0:1])
  feature_matrix = shuffle_matrix[:,1:]

  # Machine Learning
  # Linear Regression - albeit the data does not look so linear by itself
  # Parameter matrix
  parameter_matrix = numpy.ones((feature_matrix.shape[1], 1))
  print "Parameter matrix (rows):       %d\n              (columns):       %d" % parameter_matrix.shape


  print "Seprating into learning data set and cross validation data set..."
  m, n = feature_matrix.shape
  lrn_m = int(numpy.ceil(0.6*m))
  cross_validation_x = feature_matrix[lrn_m:,:]
  cross_validation_y = measured_matrix[lrn_m:,:]

  feature_matrix = feature_matrix[0:lrn_m,:]
  measured_matrix = measured_matrix[0:lrn_m,:]
  print "New feature matrix:          %d x %d" % (feature_matrix.shape)
  print "New cross validation matrix: %d x %d" % (cross_validation_x.shape)

  print "Calculating the cost function..."
  J_theta = cost_function(feature_matrix, parameter_matrix, measured_matrix)
  print "...J(theta): %f" % J_theta

  print "Gradient descent..."
  print "initial theta: %s" % parameter_matrix.T

  J_lrn, J_cv = [], []

  num_iter = 200
  for i in range(1,num_iter):
   
    parameter_matrix = gradient_descent(feature_matrix, parameter_matrix, measured_matrix, alpha=0.1)
    J_lrn.append(cost_function(feature_matrix, parameter_matrix, measured_matrix))
    J_cv.append(cost_function(cross_validation_x, parameter_matrix, cross_validation_y))


  J_lrn, J_cv = numpy.array(J_lrn), numpy.array(J_cv)

  print "...end"
  # Load figure canvas

  fig = plt.figure(0)
  ax1 = fig.add_subplot(111)
  ax1.errorbar(range(1,num_iter), J_lrn, fmt="o", ls="-", label="J learn", color="blue")
  ax1.errorbar(range(1,num_iter), J_cv, fmt="o", ls="-", label="J cv", color="red")
  ax1.set_xlabel("Number of iterations")
  ax1.set_ylabel("Cost function")

  leg1 = ax1.legend(loc=0, numpoints=1, scatterpoints=1)

  plt.show()

  

if __name__=='__main__':
  main()
