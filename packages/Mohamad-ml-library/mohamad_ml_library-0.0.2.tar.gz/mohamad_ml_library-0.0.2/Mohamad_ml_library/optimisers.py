import numpy as np
class GradientDescent:
  def __init__(self,learning_rate=0.01,clip_norm=None, clip_value=None):
    self.learning_rate=learning_rate
    self.clip_norm = clip_norm
    self.clip_value = clip_value

  def step(self, params, grads):
    for i, (param, grad) in enumerate(zip(params, grads)):
        if self.clip_norm is not None:
            norm = np.linalg.norm(grad)
            if norm > self.clip_norm:
                grad = grad * (self.clip_norm / norm)
        if self.clip_value is not None:
            grad = np.clip(grad, -self.clip_value, self.clip_value)
        params[i] -= self.learning_rate * grad
class SGD:
  def __init__(self,learning_rate=0.01,batch_size=1, clip_norm=None, clip_value=None):
    self.learning_rate=learning_rate
    self.batch_size=batch_size
    self.clip_norm = clip_norm
    self.clip_value = clip_value

  def step(self, params, grads):
    for i, (param, grad) in enumerate(zip(params, grads)):
        if self.clip_norm is not None:
            norm = np.linalg.norm(grad)
            if norm > self.clip_norm:
                grad = grad * (self.clip_norm / norm)
        if self.clip_value is not None:
            grad = np.clip(grad, -self.clip_value, self.clip_value)
        params[i] -= self.learning_rate * grad

class Momentum:
  def __init__(self,learning_rate=0.01,beta=0.9,batch_size=1, clip_norm=None, clip_value=None):
    self.learning_rate=learning_rate
    self.beta=beta
    self.batch_size=batch_size
    self.V=None
    self.clip_norm = clip_norm
    self.clip_value = clip_value
  def zero_grad(self):
    if self.V is not None:
        self.V = [np.zeros_like(v) for v in self.V]
  def step(self, params, grads):
    if self.V is None:
      self.V = [np.zeros_like(param) for param in params]
    for i, (param, grad) in enumerate(zip(params, grads)):
        if self.clip_norm is not None:
            norm = np.linalg.norm(grad)
            if norm > self.clip_norm:
                grad = grad * (self.clip_norm / norm)
        if self.clip_value is not None:
            grad = np.clip(grad, -self.clip_value, self.clip_value)
        self.V[i] = self.beta * self.V[i] + (1 - self.beta) * grad
        params[i] -= self.learning_rate * self.V[i]



class RMSprop:
  def __init__(self,learning_rate=0.01,beta=0.9,epsilon=1e-8,batch_size=1, clip_norm=None, clip_value=None):
    self.learning_rate=learning_rate
    self.beta=beta
    self.batch_size=batch_size
    self.epsilon=epsilon
    self.S=None
    self.clip_norm = clip_norm
    self.clip_value = clip_value
  def zero_grad(self):
    if self.S is not None:
        self.S = [np.zeros_like(s) for s in self.S]
  def step(self, params, grads):
    if self.S is None:
      self.S = [np.zeros_like(param) for param in params]
    for i, (param, grad) in enumerate(zip(params, grads)):
        if self.clip_norm is not None:
            norm = np.linalg.norm(grad)
            if norm > self.clip_norm:
                grad = grad * (self.clip_norm / norm)
        if self.clip_value is not None:
            grad = np.clip(grad, -self.clip_value, self.clip_value)
        self.S[i] = self.beta * self.S[i] + (1 - self.beta) * (grad**2)
        params[i] -= self.learning_rate * grad / (np.sqrt(self.S[i]) + self.epsilon)

class Adam:
  def __init__(self,learning_rate=0.01,beta1=0.9,beta2=0.99,epsilon=1e-8,batch_size=1, clip_norm=None, clip_value=None):
    self.learning_rate=learning_rate
    self.beta1=beta1
    self.beta2=beta2
    self.batch_size=batch_size
    self.epsilon=epsilon
    self.V=None
    self.S=None
    self.t=0
    self.clip_norm = clip_norm
    self.clip_value = clip_value
  def zero_grad(self):
    if self.V is not None:
        self.V = [np.zeros_like(v) for v in self.V]
    if self.S is not None:
        self.S = [np.zeros_like(s) for s in self.S]
  def step(self, params, grads):
    if self.V is None:
      self.V = [np.zeros_like(param) for param in params]
      self.S = [np.zeros_like(param) for param in params]

    self.t+=1
    for i, (param, grad) in enumerate(zip(params, grads)):
        if self.clip_norm is not None:
            norm = np.linalg.norm(grad)
            if norm > self.clip_norm:
                grad = grad * (self.clip_norm / norm)
        if self.clip_value is not None:
            grad = np.clip(grad, -self.clip_value, self.clip_value)
        self.V[i] = self.beta1 * self.V[i] + (1 - self.beta1) * grad
        self.S[i] = self.beta2 * self.S[i] + (1 - self.beta2) * (grad**2)
        Vcorrect = self.V[i] / (1 - self.beta1 ** self.t)
        Scorrect = self.S[i] / (1 - self.beta2 ** self.t)
        params[i] -= self.learning_rate*(Vcorrect/(np.sqrt(Scorrect) + self.epsilon))