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

import matplotlib.pyplot as plt
import numpy
import random
#from scipy.optimize import minimize
import time
from scipy.optimize import fmin as minimize

from cite_lib import check_content

def gradient_descent_poisson(x, theta, y, alpha=0.3):

  # Normal gradient descent
  # m - number of entries
  # n - number of features

  h_x = numpy.dot(theta.T,x.T).T

  print y.shape
  print (numpy.dot((y+numpy.exp(h_x)).T,x)).shape

  #dJ_dTheta = 
  
  print theta.shape
  print dJ_dTheta.shape
  theta -= alpha * dJ_dTheta
  print theta.shape
  sys.exit(0)

  return theta

def gradient_descent(x, theta, y, alpha=0.3):

  # Normal gradient descent
  # m - number of entries
  # n - number of features

  
  m, n = x.shape
  theta -= (alpha/m) * numpy.dot((numpy.dot(theta.T, x.T).T - y).T, x).T

  
  return theta


def cost_function_poisson(x, theta, y):
  y +=1
  h_x = numpy.dot(theta.T,x.T)
  j_1 = numpy.dot(y.T, numpy.log(y)) - numpy.dot(y.T, h_x.T) 
  j_2  = (numpy.exp(h_x) - y).sum()
  j = 2*(j_1 + j_2)

  return j

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
  print("Loading data from SQL database...")
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
  print("Feature matrix mean: {0}".format(mean))
  print("Feature matrix standard deviation: {0}".format(std))

  # Add the bias or zero-th value
  bias_matrix = numpy.ones((feature_matrix.shape[0],1))
  feature_matrix = numpy.concatenate((bias_matrix, feature_matrix), axis=1)

  print("...loaded feature matrix:\n")
  print("Number of data entries (rows, columns): {0}".format(feature_matrix.shape))


  # Machine Learning
  # Linear Regression - albeit the data does not look so linear by itself
  # Parameter matrix
  parameter_matrix = numpy.ones((feature_matrix.shape[1], 1))
  print("Parameter matrix (rows, columns):       {0}".format(parameter_matrix.shape))


  print("Calculating the cost function...")
  J_theta = cost_function(feature_matrix, parameter_matrix, measured_matrix)
  print("...J(theta): {0:f}".format(J_theta))

  par_init = numpy.array([random.random()*10-5 for i in parameter_matrix])
  #fnc = lambda par: cost_function(feature_matrix, par, measured_matrix)
  
  print("Initialising parameter matrix to: {0}".format((par_init)))

  t_start = time.time()

  J_p_theta = cost_function_poisson(feature_matrix, par_init, measured_matrix)
  print(J_p_theta)
  
  par_init = gradient_descent_poisson(feature_matrix, par_init, measured_matrix, alpha=0.1)
  # J_p_theta = cost_function_poisson(feature_matrix, par_init, measured_matrix)
  print(par_init)
  
  
  
  
  t_end = time.time()

  time_taken = (t_end - t_start)/60. # minutes
  print("Time taken: {0} minutes".format(time_taken))
 
  #fig = plt.figure(0)
  #ax1 = fig.add_subplot(111)
  #ax1.errorbar(feature_matrix[:,3], measured_matrix, fmt="o", color="blue")
  #ax1.set_xlabel("Publication year")
  #ax1.set_ylabel("Citation count")

  #plt.show()

  

if __name__=='__main__':
  main()
