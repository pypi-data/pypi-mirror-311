import numpy as np
from MachineLearning_MohamadElMokdad import LinearRegression
from MachineLearning_MohamadElMokdad.costfunctions import MSE
class PolynomialRegression():
  def __init__(self,degree=2,cost_func=MSE,optimizer=None,method='gradient',regularization=None,alpha=0.1):
    self.degree=degree
    self.linear_model=LinearRegression(cost_func=cost_func, optimizer=optimizer, method=method, regularization=regularization, alpha=alpha)

  def _poly_features(self,X):
    X_poly=X
    for d in range (2,self.degree+1):
      X_poly=np.c_[X_poly,X**d]
    return X_poly
  def fit(self,X,y_actual,n):
    X_poly=self._poly_features(X)
    self.linear_model.fit(X_poly, y_actual,n)
    return self.linear_model.theta
  def predict(self,X):
    X_poly=self._poly_features(X)
    return self.linear_model.predict(X_poly)

  def normalize_features(self, x):
    """ Normalize features using Z-score normalization """
    self.mean = np.mean(x, axis=0)
    self.std = np.std(x, axis=0)
    return (x - self.mean) / self.std