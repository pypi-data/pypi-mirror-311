import numpy as np
from MachineLearning_MohamadElMokdad.costfunctions import cost_gradient_mapping
from MachineLearning_MohamadElMokdad.costfunctions import MSE
from MachineLearning_MohamadElMokdad.optimisers import GradientDescent
class LinearRegression:
  def __init__(self,cost_func=MSE,optimizer=None,method='gradient',regularization=None,alpha=0.1):
    self.method=method
    self.regularization=regularization
    self.alpha=alpha
    if self.method == 'gradient':
      self.cost_function = cost_func
      self.gradient_func = cost_gradient_mapping[cost_func]
      if optimizer is None:
        self.optimizer = GradientDescent(learning_rate=0.01)
      else:
        optimizer.grad = self._reg_gradient_func
        self.optimizer = optimizer
    self.theta = None

  def _reg_gradient_func(self,X,y_pred,y_actual,theta):
    dJ=self.gradient_func(X,y_pred,y_actual)
    if self.regularization=='L2':
      dJ[1:]+=self.alpha*theta[1:]
    elif self.regularization=='L1':
      dJ[1:]+=self.alpha*np.sign(theta[1:])
    return dJ

  def _predict(self, X, theta):
    return np.dot(X, theta)

  def fit(self, X, y,n):
    X_aug = np.hstack((np.ones((X.shape[0], 1)), X))
    self.theta = np.zeros(X_aug.shape[1])
    if self.method == 'direct':
      if self.regularization=='L2':
        identity = self.alpha * np.eye(X_aug.shape[1])  # Regularization term
        identity[0, 0] = 0 
        self.theta = np.linalg.inv(X_aug.T @ X_aug+identity) @ X_aug.T @ y
      else:
        self.theta = np.linalg.inv(X_aug.T @ X_aug) @ X_aug.T @ y

    elif isinstance(self.optimizer, GradientDescent):
      for _ in range(n):
        y_pred=self._predict(X_aug,self.theta)
        dJ = self._reg_gradient_func(X_aug, y_pred, y, self.theta)
        self.optimizer.step([self.theta], [dJ])
        
    else:
      for _ in range(n):
        indices=np.random.permutation(X_aug.shape[0])
        X_shuffled=X_aug[indices]
        y_shuffled=y[indices]
        batch_size=self.optimizer.batch_size
        for i in range(0,X_aug.shape[0],batch_size):
          X_batch=X_shuffled[i:i+batch_size]
          y_batch=y_shuffled[i:i+batch_size]
          y_pred=self._predict(X_batch,self.theta)
          dJ=self._reg_gradient_func(X_batch,y_pred,y_batch,self.theta)
          self.optimizer.step([self.theta], [dJ])
    return self.theta
  def predict(self, X):
    X_aug = np.c_[np.ones(X.shape[0]), X]
    predictions= self._predict(X_aug, self.theta)
    return np.array(predictions)


