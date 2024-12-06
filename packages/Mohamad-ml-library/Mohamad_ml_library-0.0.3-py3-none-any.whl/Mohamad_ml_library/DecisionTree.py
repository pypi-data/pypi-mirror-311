import numpy as np
class DecisionTree:
  def __init__(self,max_depth=10,criterion="entropy"):
    self.max_depth=max_depth
    self.tree=None
    self.criterion=criterion

  class leaf:
    def __init__(self,y):
      self.predictions=self.compute_class_counts(y)
    def compute_class_counts(self,y):
      classes,counts=np.unique(y,return_counts=True)
      return list(zip(classes,counts))
    def most_common_class(self):
      classes,counts=zip(*self.predictions)
      return classes[np.argmax(counts)]

  class DecisionNode:
    def __init__(self,feature,threshold,left,right):
      self.feature=feature
      self.threshold=threshold
      self.left=left
      self.right=right

  def fit(self,X,y):
    self.tree=self._build_tree(X,y)

  def _build_tree(self,X,y,depth=0):

    if depth>=self.max_depth or len(np.unique(y)) == 1:
      return self.leaf(y)

    best_feature, best_threshold = self._find_best_split(X, y)

    if best_feature is None:
      return self.leaf(y)

    left_indices = X[:, best_feature] <= best_threshold
    right_indices = X[:, best_feature] > best_threshold
    left_child = self._build_tree(X[left_indices], y[left_indices], depth + 1)
    right_child = self._build_tree(X[right_indices], y[right_indices], depth + 1)

    return self.DecisionNode(feature=best_feature, threshold=best_threshold, left=left_child, right=right_child)

  def _find_best_split(self, X, y):
    best_gain = -1
    best_feature, best_threshold = None, None

    for feature in range(X.shape[1]):
        thresholds = np.unique(X[:, feature])
        for threshold in thresholds:
            gain = self._information_gain(y, X[:, feature], threshold)
            if gain > best_gain:
                best_gain, best_feature, best_threshold = gain, feature, threshold

    return best_feature, best_threshold

  def _information_gain(self, y, feature_column, threshold):
    parent_impurity = self._calculate_impurity(y)
    left_indices = feature_column <= threshold
    right_indices = feature_column > threshold

    if len(y[left_indices]) == 0 or len(y[right_indices]) == 0:
        return 0

    n = len(y)
    n_left, n_right = len(y[left_indices]), len(y[right_indices])
    child_impurity = (n_left / n) * self._calculate_impurity(y[left_indices]) + (n_right / n) * self._calculate_impurity(y[right_indices])

    return parent_impurity - child_impurity

  def _calculate_impurity(self, y):
        # Choose impurity measure based on the criterion
        if self.criterion == "entropy":
            return self._entropy(y)
        elif self.criterion == "gini":
            return self._gini(y)
        else:
            raise ValueError("Criterion must be 'entropy' or 'gini'.")

  def _entropy(self, y):
    classes, counts = np.unique(y, return_counts=True)
    probabilities = counts / counts.sum()
    return -np.sum(probabilities * np.log2(probabilities))

  def _gini(self, y):
        classes, counts = np.unique(y, return_counts=True)
        probabilities = counts / counts.sum()
        return np.sum(probabilities * (1 - probabilities))


  def predict(self, X):
    return np.array([self._predict_row(row, self.tree) for row in X])

  def _predict_row(self, row, node):
      if isinstance(node, self.leaf):
          return node.most_common_class()
      if row[node.feature] <= node.threshold:
          return self._predict_row(row, node.left)
      else:
          return self._predict_row(row, node.right)