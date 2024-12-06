import numpy as np

class DecisionTreeRegressor:
    def __init__(self, max_depth=10):
        self.max_depth = max_depth
        self.tree = None

    class Leaf:
        def __init__(self, y):
            self.prediction = np.mean(y)  # Mean value of the targets for regression

    class DecisionNode:
        def __init__(self, feature, threshold, left, right):
            self.feature = feature
            self.threshold = threshold
            self.left = left
            self.right = right

    def fit(self, X, y):
        """Fit the tree to the training data."""
        self.tree = self._build_tree(X, y)

    def _build_tree(self, X, y, depth=0):
        """Recursively build the decision tree."""
        if depth >= self.max_depth or len(y) <= 1:
            return self.Leaf(y)

        best_feature, best_threshold = self._find_best_split(X, y)
        if best_feature is None:
            return self.Leaf(y)

        left_indices = X[:, best_feature] <= best_threshold
        right_indices = X[:, best_feature] > best_threshold

        left_child = self._build_tree(X[left_indices], y[left_indices], depth + 1)
        right_child = self._build_tree(X[right_indices], y[right_indices], depth + 1)

        return self.DecisionNode(feature=best_feature, threshold=best_threshold, left=left_child, right=right_child)

    def _find_best_split(self, X, y):
        """Find the best feature and threshold to split the data."""
        best_gain = -1
        best_feature, best_threshold = None, None

        for feature in range(X.shape[1]):
            thresholds = np.unique(X[:, feature])
            for threshold in thresholds:
                gain = self._variance_reduction(y, X[:, feature], threshold)
                if gain > best_gain:
                    best_gain, best_feature, best_threshold = gain, feature, threshold

        return best_feature, best_threshold

    def _variance_reduction(self, y, feature_column, threshold):
        """Calculate variance reduction (quality of the split)."""
        parent_variance = np.var(y)
        left_indices = feature_column <= threshold
        right_indices = feature_column > threshold

        if len(y[left_indices]) == 0 or len(y[right_indices]) == 0:
            return 0

        n = len(y)
        n_left, n_right = len(y[left_indices]), len(y[right_indices])
        weighted_variance = (n_left / n) * np.var(y[left_indices]) + (n_right / n) * np.var(y[right_indices])

        return parent_variance - weighted_variance

    def predict(self, X):
        """Predict target values for the input data."""
        return np.array([self._predict_row(row, self.tree) for row in X])

    def _predict_row(self, row, node):
        """Traverse the tree to make a prediction for a single row."""
        if isinstance(node, self.Leaf):
            return node.prediction
        if row[node.feature] <= node.threshold:
            return self._predict_row(row, node.left)
        else:
            return self._predict_row(row, node.right)
