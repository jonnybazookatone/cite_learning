Cite Learn
----------

A machine learning tool that predicts the number of citations based on an input criteria of the author. It utilises Generalised Linear Models, more specifically Poisson or negative Binomial regression to fit to the citation number (or rate).

# Currently implemented

* PCA deconstruction of the input variables - removes covariance
* Fitting with a FLM

# Not implemented

* Determine the functional form on the fly based on the input
* Meaningful text extraction from abstracts or titles (see TextBlob on github)

Test Dataset
------------

The test dataset is obtained from ESO. It is a bibliographic record of publications that referenced ESO instruments from 2000-2013. This is courtesy of Uta and also V. Sudilovsky.
