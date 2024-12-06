import numpy as np
def MSE(y_pred,y_actual):
  return np.mean((y_actual-y_pred)**2)


def MAE(y_pred,y_actual):
  return np.mean(np.abs(y_actual-y_pred))


def huber(y_pred,y_actual,delta=2):
  err=y_actual-y_pred
  is_small=np.abs(err)<=delta
  squared=0.5*err**2
  linear=delta*np.abs(err)-0.5*delta**2 # 0.5*delta**2 is used to ensure a smooth transition from the squared error to the linear one
  return np.where(is_small,squared,linear).mean()


def MSE_grad(X,y_pred,y_actual,model='Linear Regression'):
  if model == 'Linear Regression':
    n=X.shape[0]
    dJ=(2/n)*np.dot(X.T,(y_pred-y_actual))
  elif model =='MLP':
    dJ=(2/y_actual.shape[0])*(y_pred-y_actual)
  return dJ


def MAE_grad(X,y_pred,y_actual,model='Linear Regression'):
  n=X.shape[0]
  sign=np.sign(y_pred-y_actual)
  if model == 'Linear Regression':
    dJ=(1/n)*np.dot(X.T,sign)
  elif model =='MLP':
    dJ=sign / n
  return dJ


def huber_grad(X, y_pred, y_actual, delta=2):
    n = X.shape[0]
    error = y_pred-y_actual
    is_small_error = np.abs(error) <= delta
    dJ = np.where(is_small_error, error, delta * np.sign(error))
    dJ = (1 / n) * np.dot(X.T, dJ)
    return dJ

cost_gradient_mapping = {
    MSE: MSE_grad,
    MAE: MAE_grad,
    huber: huber_grad
}