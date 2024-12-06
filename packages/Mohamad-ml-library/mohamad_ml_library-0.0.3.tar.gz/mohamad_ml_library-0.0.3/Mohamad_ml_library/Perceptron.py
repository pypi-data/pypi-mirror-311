import numpy as np
from Mohamad_ml_library.activationfunctions import unit_step
class Perceptron:
  def __init__(self,learning_rate=0.01,max_iterations=1000,activation_func=unit_step):
    self.learning_rate=learning_rate
    self.max_iterations=max_iterations
    self.activation_func=activation_func
    self.weights=None

  def fit(self,X,y_actual):
    X_aug = np.c_[np.ones(X.shape[0]), X]
    n_samples,n_features=X_aug.shape
    self.weights=np.zeros(n_features)

    for _ in range(self.max_iterations):
      for i,x_i in enumerate(X_aug):
        y_pred= self.activation_func.activation(np.dot(x_i,self.weights))

        if y_actual[i]!=y_pred:
          update=self.learning_rate*(y_actual[i]-y_pred)
          self.weights+=update*x_i
  def predict(self,X):
      X_aug = np.c_[np.ones(X.shape[0]), X]
      linear_out=np.dot(X_aug,self.weights)
      y_pred = np.array([self.activation_func.predict(x) for x in linear_out])
      return np.array(y_pred)