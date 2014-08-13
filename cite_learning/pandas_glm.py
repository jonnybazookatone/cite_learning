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
import matplotlib.pyplot as plt
import numpy

from cite_lib import load_data_vlad, check_content

def main():

  import statsmodels.api as sm
  import statsmodels.formula.api as smf
  import pandas as pd

  df = pd.read_csv("cilearn.csv", encoding="utf-8")

  df["CitationCount"] += 1

  formula = 'CitationCount ~ LengthOfAbstract + LengthOfTitle + NumberOfAuthors'

  family = sm.families.Binomial()

  mod1 = smf.glm(formula=formula, data=df, family=family)
  mod1.fit()
  print mod1.summary()


  # Load figure canvas
  plot = False
  if plot:
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
