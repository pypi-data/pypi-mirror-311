import numpy as np
class KNN:
    def __init__(self, k=3, distance_metric='euclidean', purpose='classification'):
        """
        Initializes the KNN model with the specified parameters.
        
        Parameters:
        - k (int): The number of nearest neighbors to consider. Default is 3.
        - distance_metric (str): The distance metric to use, either 'euclidean' or 'manhattan'. Default is 'euclidean'.
        - purpose (str): The purpose of the model, either 'classification' or 'regression'. Default is 'classification'.
        """
        self.k = k
        self.distance_metric = distance_metric
        self.purpose = purpose

    def euclidean(self, x1, x2):
        """
        Calculates the Euclidean distance between two vectors.
        
        Parameters:
        - x1 (array-like): The first vector.
        - x2 (array-like): The second vector.
        
        Returns:
        - float: The Euclidean distance between x1 and x2.
        """
        return np.sqrt(np.sum((x2 - x1) ** 2))

    def manhattan(self, x1, x2):
        """
        Calculates the Manhattan distance between two vectors.
        
        Parameters:
        - x1 (array-like): The first vector.
        - x2 (array-like): The second vector.
        
        Returns:
        - float: The Manhattan distance between x1 and x2.
        """
        return np.sum(np.abs(x2 - x1))

    def train(self, X, y):
        """
        Trains the KNN model by storing the training data.
        
        Parameters:
        - X (array-like): Input features for training.
        - y (array-like): Corresponding labels for the input features.
        
        Returns:
        - None: This method does not return any value.
        """
        X = np.array(X)
        y = np.array(y)
        self.X_train = X
        self.y_train = y

    def predict_single(self, x):
        """
        Predicts the label or value for a single input sample.
        
        Parameters:
        - x (array-like): Input features for which to predict the label or value.
        
        Returns:
        - For classification: The most common label among the k nearest neighbors.
        - For regression: The mean value of the k nearest neighbors.
        
        Raises:
        - ValueError: If an invalid distance metric or purpose is provided.
        - ValueError: If k is greater than the number of training samples.
        """
        distances = []

        if self.distance_metric == 'manhattan':
            distances = [self.manhattan(x, x_train) for x_train in self.X_train]
        elif self.distance_metric == 'euclidean':
            distances = [self.euclidean(x, x_train) for x_train in self.X_train]
        else:
            raise ValueError(f'Invalid Distance Metric {self.distance_metric}')

        if self.k > len(self.X_train):
            raise ValueError(f'k cannot be greater than the number of training samples. k: {self.k}, number of training samples: {len(self.X_train)}')

        # Get k nearest samples, labels
        k_indices = np.argsort(distances)[:self.k]
        k_nearest_labels = [self.y_train[i] for i in k_indices]

        # Majority vote
        if self.purpose == 'classification':
            most_common = np.bincount(k_nearest_labels).argmax()
            return most_common
        elif self.purpose == 'regression':
            return np.mean(k_nearest_labels)
        else:
            raise ValueError(f'Invalid Purpose {self.purpose}')

    def predict(self, X):
        """
        Predicts labels or values for multiple input samples.
        
        Parameters:
        - X (array-like): Input features for which to predict labels or values.
        
        Returns:
        - numpy.ndarray: Predicted labels or values for each input sample.
        """
        return np.array([self.predict_single(x) for x in X])

    def mean_squared_error(self, y_true, y_pred):
        """
        Calculates the Mean Squared Error (MSE) between true and predicted values.
        
        Parameters:
        - y_true (array-like): True labels or values.
        - y_pred (array-like): Predicted labels or values.
        
        Returns:
        - float: The Mean Squared Error.
        
        Raises:
        - ValueError: If the purpose is not set to 'regression'.
        """
        if self.purpose != 'regression':
            raise ValueError("Mean Squared Error is only applicable for regression tasks.")
        return np.mean((y_true - y_pred) ** 2)

    def accuracy(self, y_true, y_pred):
        """
        Calculates the accuracy of predictions for classification tasks.
        
        Parameters:
        - y_true (array-like): True labels.
        - y_pred (array-like): Predicted labels.
        
        Returns:
        - float: The accuracy of the predictions.
        
        Raises:
        - ValueError: If the purpose is not set to 'classification'.
        """
        if self.purpose != 'classification':
            raise ValueError("Accuracy is only applicable for classification tasks.")
        accuracy = np.sum(y_true == y_pred) / len(y_true)
        return accuracy

    def confusion_matrix(self, y_true, y_pred):
        """
        Computes the confusion matrix for classification tasks.
        
        Parameters:
        - y_true (array-like): True labels.
        - y_pred (array-like): Predicted labels.
        
        Returns:
        - numpy.ndarray: The confusion matrix.
        
        Raises:
        - ValueError: If the purpose is not set to 'classification'.
        """
        if self.purpose != 'classification':
            raise ValueError("Confusion matrix is only applicable for classification tasks.")
        unique_labels = np.unique(y_true)
        n_labels = len(unique_labels)

        matrix = np.zeros((n_labels, n_labels), dtype=int)

        for i in range(len(y_true)):
            matrix[int(y_true[i]), int(y_pred[i])] += 1

        return matrix
