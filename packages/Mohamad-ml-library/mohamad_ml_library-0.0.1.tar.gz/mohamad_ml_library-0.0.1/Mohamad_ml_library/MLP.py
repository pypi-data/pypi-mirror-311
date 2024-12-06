import numpy as np
from MachineLearning_MohamadElMokdad.costfunctions import cost_gradient_mapping
from MachineLearning_MohamadElMokdad.costfunctions import MSE
from MachineLearning_MohamadElMokdad.optimisers import GradientDescent
from MachineLearning_MohamadElMokdad.activationfunctions import ReLU,sigmoid,tanh,unit_step
class MLP:
  def __init__(self,layer_sizes,activations,cost_func=MSE,learning_rate=0.01,optimizer=None,dropoutlayers=None):

    self.layer_sizes=layer_sizes
    self.learning_rate=learning_rate
    self.activations=activations
    self.cost_function = cost_func
    self.cost_gradient_func = cost_gradient_mapping[cost_func]

    if optimizer is None:
      self.optimizer = GradientDescent(learning_rate=0.01)
    else:
      self.optimizer = optimizer

    if dropoutlayers is None:
      self.dropoutlayers=[0.0]*(len(layer_sizes)-1)
    else:
      self.dropoutlayers=dropoutlayers

    self.weights=[]
    self.biases=[]

    for i in range(len(layer_sizes)-1):
      weights=np.random.randn(layer_sizes[i],layer_sizes[i+1])
      bias = np.zeros((1, layer_sizes[i + 1]))
      self.weights.append(weights)
      self.biases.append(bias)

  def _apply_dropout(self, activation, p):
    if p < 0 or p > 1:
          raise ValueError(
              f"dropout probability has to be between 0 and 1, but got {p}"
          )
    mask = (np.random.rand(*activation.shape) > p).astype(np.float32)
    return activation * mask / (1 - p)

  def _forward(self,X,training=True):
    A=[X]
    Z=[]
    for i,(w,b) in enumerate(zip(self.weights,self.biases)):
      z=A[-1]@w+b
      a=self.activations[i].activation(z)
      if training==True and i < len(self.weights) - 1:
        a=self._apply_dropout(a, self.dropoutlayers[i])
      Z.append(z)
      A.append(a)
    return A,Z

  def _backward(self,y,A,Z,X):

    weights_grad=[np.zeros_like(w) for w in self.weights]
    bias_grad=[np.zeros_like(b) for b in self.biases]

    delta=self.cost_gradient_func(X,A[-1],y,model='MLP')*self.activations[-1].activation_prime(Z[-1]) #output layer error


    weights_grad[-1]=A[-2].T@delta
    bias_grad[-1]=np.sum(delta, axis=0, keepdims=True)

    for l in range(2,len(self.layer_sizes)):
      delta=(delta @ self.weights[-l + 1].T)*self.activations[-l].activation_prime(Z[-l])
      weights_grad[-l]=A[-l-1].T@delta
      bias_grad[-l]=np.sum(delta, axis=0, keepdims=True)
    return weights_grad, bias_grad

  def train(self,X,y,epochs=100):
    for epoch in range(epochs):
      if isinstance(self.optimizer, GradientDescent):
          A,Z=self._forward(X)
          weight_grads, bias_grads = self._backward(y, A, Z)
          self.optimizer.step(self.weights, weight_grads)
          self.optimizer.step(self.biases, bias_grads)
          loss = np.mean((A[-1] - y) ** 2)
          # if epoch % 10 == 0:
          #   print(f"Epoch {epoch}: Loss = {loss}")
      else:
        batch_size = self.optimizer.batch_size
        n_samples = X.shape[0]
        indices=np.random.permutation(n_samples)
        X_shuffled=X[indices]
        y_shuffled=y[indices]
        for i in range(0,n_samples,batch_size):
          X_batch=X_shuffled[i:i+batch_size]
          y_batch=y_shuffled[i:i+batch_size]
          A,Z=self._forward(X_batch)
          weight_grads, bias_grads = self._backward(y_batch, A, Z,X_batch)
          params = self.weights + self.biases
          grads = weight_grads + bias_grads
          self.optimizer.step(params,grads)
        # loss = np.mean((A[-1] - y_batch) ** 2)
        # if epoch % 10 == 0:
        #   print(f"Epoch {epoch}: Loss = {loss}")


  def predict(self,X):
    A,_=self._forward(X,training=False)
    return A[-1]