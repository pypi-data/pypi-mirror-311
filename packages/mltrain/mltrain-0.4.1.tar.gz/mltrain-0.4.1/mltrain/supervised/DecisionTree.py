import numpy as np

# Creating Node class
class Node:
    def __init__(self, feature=None, threshold=None, left=None, right=None, value=None):
        """
        Initializes a node in the decision tree, which can either be a decision node
        with a feature and threshold, or a leaf node with a specific value.
        
        Parameters:
        - feature: The feature index used for splitting the data at this node.
        - threshold: The threshold value for the feature at this node.
        - left: The left child node (for values less than or equal to the threshold).
        - right: The right child node (for values greater than the threshold).
        - value: The class label if this node is a leaf node.
        """
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value

    def is_leaf_node(self):
        """
        Checks if the current node is a leaf node.
        
        Returns:
        - True if the node is a leaf node (contains a class label), otherwise False.
        """
        return self.value is not None

# Implementing DecisionTreeModel
class DecisionTree:
    def __init__(self, max_depth=10, min_samples_split=2, criteria='gini'):
        """
        Initializes the DecisionTreeModel with specified parameters.
        
        Parameters:
        - max_depth: The maximum depth the tree can grow to.
        - min_samples_split: The minimum number of samples required to split a node.
        - criteria: The criterion used for splitting ('gini' or 'entropy').
        """
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.tree = None
        self.criteria = criteria

    def traverse_tree(self, x, node):
        """
        Traverses the tree to make a prediction for a single sample.
        
        Parameters:
        - x: The input sample.
        - node: The current node in the tree.
        
        Returns:
        - The predicted class label for the input sample.
        """
        if node.is_leaf_node():
            return node.value
        if x[node.feature] <= node.threshold:
            return self.traverse_tree(x, node.left)
        return self.traverse_tree(x, node.right)

    def most_common_label(self, y):
        """
        Determines the most common label in the target array.
        
        Parameters:
        - y: The array of target labels.
        
        Returns:
        - The most common label in the target array.
        """
        labels, counts = np.unique(y, return_counts=True)  # Links labels with their count
        return labels[np.argmax(counts)]  # Returns the label with the highest count

    def predict(self, X):
        """
        Predicts class labels for the given dataset.
        
        Parameters:
        - X: The dataset for which to make predictions.
        
        Returns:
        - An array of predicted class labels.
        """
        return np.array([self.traverse_tree(x, self.tree) for x in X])

    def split(self, X, y, feature, threshold):
        """
        Splits the dataset based on the specified feature and threshold.
        
        Parameters:
        - X: The dataset to be split.
        - y: The target labels.
        - feature: The feature index used for splitting.
        - threshold: The threshold value for splitting.
        
        Returns:
        - Indices of the left and right subsets after the split.
        """
        left_idx = np.where(X[:, feature] <= threshold)[0]
        right_idx = np.where(X[:, feature] > threshold)[0]
        return left_idx, right_idx

    def entropy(self, y):
        """
        Calculates the entropy of the target labels.
        
        Parameters:
        - y: The array of target labels.
        
        Returns:
        - The entropy value.
        """
        labels, counts = np.unique(y, return_counts=True)
        p = counts / counts.sum()
        return -np.sum(p * np.log2(p))

    def gini(self, y):
        """
        Calculates the Gini impurity of the target labels.
        
        Parameters:
        - y: The array of target labels.
        
        Returns:
        - The Gini impurity value.
        """
        labels, counts = np.unique(y, return_counts=True)
        p = counts / counts.sum()
        return 1 - np.sum(p**2)

    def information_gain(self, X, y, feature, threshold):
        """
        Calculates the information gain from splitting the data on a specific feature and threshold.
        
        Parameters:
        - X: The dataset being split.
        - y: The target labels.
        - feature: The feature index used for splitting.
        - threshold: The threshold value for splitting.
        
        Returns:
        - The information gain from the split.
        """
        if self.criteria == 'gini':
            parent_loss = self.gini(y)
        else:
            parent_loss = self.entropy(y)

        left_idx, right_idx = self.split(X, y, feature, threshold)
        if len(left_idx) == 0 or len(right_idx) == 0:
            return 0
        n, n_left, n_right = len(y), len(left_idx), len(right_idx)

        loss_left = self.gini(y[left_idx]) if self.criteria == 'gini' else self.entropy(y[left_idx])
        loss_right = self.gini(y[right_idx]) if self.criteria == 'gini' else self.entropy(y[right_idx])

        child_loss = (n_left/n) * loss_left + (n_right/n) * loss_right

        return parent_loss - child_loss

    def best_split(self, X, y, features):
        """
        Finds the best feature and threshold to split the data to maximize information gain.
        
        Parameters:
        - X: The dataset to be split.
        - y: The target labels.
        - features: The list of feature indices to consider for splitting.
        
        Returns:
        - The best feature index and threshold value for the split.
        """
        best_feature, best_threshold, best_gain = None, None, -1

        for feature in features:
            X_column = X[:, feature]
            thresholds = np.unique(X_column)

            for threshold in thresholds:
                gain = self.information_gain(X, y, feature, threshold)

                if gain > best_gain:
                    best_gain = gain
                    best_feature = feature
                    best_threshold = threshold
        return best_feature, best_threshold

    def build_tree(self, X, y, depth=0):
        """
        Recursively builds the decision tree by finding the best splits and creating nodes.
        
        Parameters:
        - X: The dataset to build the tree on.
        - y: The target labels.
        - depth: The current depth of the tree.
        
        Returns:
        - The root node of the decision tree.
        """
        n_samples, n_features = X.shape
        n_labels = len(np.unique(y))

        # Stopping condition
        if (depth >= self.max_depth or n_labels == 1 or n_samples < self.min_samples_split):
            leaf_value = self.most_common_label(y)
            return Node(value=leaf_value)

        # Finding the best split
        best_feature, best_threshold = self.best_split(X, y, range(n_features))
        left_idx, right_idx = self.split(X, y, best_feature, best_threshold)

        left_node = self.build_tree(X[left_idx], y[left_idx], depth + 1)
        right_node = self.build_tree(X[right_idx], y[right_idx], depth + 1)
        return Node(best_feature, best_threshold, left_node, right_node)

    def train(self, X, y):
        """
        Trains the decision tree model on the given dataset.
        
        Parameters:
        - X: The training dataset.
        - y: The target labels for the training dataset.
        
        Returns:
        - None
        """
        self.tree = self.build_tree(X, y)
