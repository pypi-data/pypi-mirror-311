from .DecisionTree import DecisionTree
import numpy as np
import numpy as np

class RandomForest:
    def __init__(self, n_trees=100, max_depth=10, min_samples_split=2, criteria='gini'):
        """
        Initializes the RandomForestModel with the specified parameters.

        Parameters:
        - n_trees: Number of trees in the forest.
        - max_depth: Maximum depth of each tree.
        - min_samples_split: Minimum number of samples required to split a node.
        - criteria: The criterion used to evaluate splits ('gini' or 'entropy').
        """
        self.n_trees = n_trees
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.criteria = criteria
        self.trees = []

    def bootstrap_sample(self, X, y):
        """
        Generates a bootstrap sample (random sample with replacement) from the dataset.

        Parameters:
        - X: Input features of the dataset.
        - y: Target labels of the dataset.

        Returns:
        - A tuple containing the bootstrap sample of features (X_sample) and target labels (y_sample).
        """
        n_samples = X.shape[0]
        idxs = np.random.choice(n_samples, size=n_samples, replace=True)
        return X[idxs], y[idxs]

    def most_common_label(self, y):
        """
        Determines the most common label in the target array.

        Parameters:
        - y: Array of target labels.

        Returns:
        - The most common label in the target array.
        """
        labels, counts = np.unique(y, return_counts=True)
        return labels[np.argmax(counts)]

    def train(self, X, y):
        """
        Trains the random forest by creating and training multiple decision trees.

        Parameters:
        - X: The training dataset.
        - y: The target labels for the training dataset.

        Returns:
        - None
        """
        self.trees = []

        for _ in range(self.n_trees):
            # Initialize a new decision tree with the specified parameters
            tree = DecisionTree(max_depth=self.max_depth, min_samples_split=self.min_samples_split, criteria=self.criteria)
            # Generate a bootstrap sample from the dataset
            X_sample, y_sample = self.bootstrap_sample(X, y)
            # Train the decision tree on the bootstrap sample
            tree.train(X_sample, y_sample)
            # Add the trained tree to the forest
            self.trees.append(tree)

    def predict(self, X):
        """
        Predicts class labels for the given dataset using the trained random forest.

        Parameters:
        - X: The dataset for which to make predictions.

        Returns:
        - An array of predicted class labels.
        """
        # Collect predictions from each tree
        tree_preds = np.array([tree.predict(X) for tree in self.trees])
        # Transpose to get predictions for each sample
        tree_preds = tree_preds.T
        # For each sample, determine the most common label across all trees
        y_pred = np.array([self.most_common_label(tree_pred) for tree_pred in tree_preds])
        return y_pred

    def accuracy(self, y_true, y_pred):
        """
        Calculates the accuracy of the model based on true and predicted labels.

        Parameters:
        - y_true: True target labels.
        - y_pred: Predicted target labels.

        Returns:
        - The accuracy of the predictions.
        """
        accuracy = np.sum(y_true == y_pred) / len(y_true)
        return accuracy

    def confusion_matrix(self, y_true, y_pred):
        """
        Generates a confusion matrix to evaluate the accuracy of the classification.

        Parameters:
        - y_true: True target labels.
        - y_pred: Predicted target labels.

        Returns:
        - A confusion matrix as a NumPy array.
        """
        unique_labels = np.unique(y_true)
        num_labels = len(unique_labels)
        confusion_matrix = np.zeros((num_labels, num_labels))
        for i in range(num_labels):
            for j in range(num_labels):
                confusion_matrix[i, j] = np.sum((y_true == unique_labels[i]) & (y_pred == unique_labels[j]))
        return confusion_matrix
