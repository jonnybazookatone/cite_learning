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
  import statsmodels.genmod as smg
  import pandas as pd
  from sklearn.cross_validation import train_test_split
  from sklearn.decomposition import PCA

  n_components = 3
  pca = PCA()

  df = pd.read_csv("cilearn.csv", encoding="utf-8")
  df.drop("BibCode", axis=1, inplace=True)

  print df

  pca.fit(df[["LengthOfAbstract","LengthOfTitle","NumberOfAuthors","PubYear"]])
  M_pca = pca.fit_transform(df)
  M_df = {}
  M_df["CitationCount"] = df["CitationCount"].values

  for i in range(n_components):
    M_df["PC{0:d}".format(i+1)] = M_pca[:,i]

  df_glm = pd.DataFrame(M_df)

  test, train = train_test_split(df_glm, test_size=int(0.1*len(df_glm)), random_state=42)

  print test
  ## Redefine some DataFrames, otherwise they are just numpy arrays
  col_train = {}
  col_test = {}
  try:
    col_train["CitationCount"] = train[:,0]
    col_test["CitationCount"] = test[:,0]
    for i in range(n_components):
      col_train["PC{0:d}".format(i+1)] = train[:,i+1]
      col_test["PC{0:d}".format(i+1)] = test[:,i+1]

  except:
    col_train["CitationCount"] = train["CitationCount"].values
    col_test["CitationCount"] = test["CitationCount"].values
    for i in range(n_components):
      col_train["PC{0:d}".format(i+1)] = train["PC{0:d}".format(i+1)]
      col_test["PC{0:d}".format(i+1)] = test["PC{0:d}".format(i+1)]

  df_test = pd.DataFrame(col_test)
  df_train = pd.DataFrame(col_train)

  poly = lambda x, power: x**power

  formula = 'CitationCount ~ poly(PC2,2)*poly(PC3,2) + PC1*PC2*PC3'

  family = sm.families.Poisson(link=smg.families.links.log)
  #family = sm.families.NegativeBinomial(link=smg.families.links.log)

  model = smf.glm(formula=formula, data=df_train, family=family)
  result = model.fit()
  print result.summary()

  # Load figure canvas
  plot = True
  if plot:
    import seaborn as sns
    fig = plt.figure(0)
    ax1 = fig.add_subplot(111)

    #ax1.errorbar(df_test["CitationCount"], result.predict(df_test), fmt="o")
    x = df_test["CitationCount"]
    y = result.predict(df_test)
    sns.jointplot(x, y, kind="hex");

    ax1.set_xlabel("Measured")
    ax1.set_ylabel("Predicted")

    x = numpy.arange(1,2000,10)
    ax1.plot(x,x)
    #ax1.set_xscale("log")
    #ax1.set_yscale("log")

    plt.show()

  

if __name__=='__main__':
  main()
