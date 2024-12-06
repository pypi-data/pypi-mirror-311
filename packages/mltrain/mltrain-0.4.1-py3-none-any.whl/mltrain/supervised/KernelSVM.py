import numpy as np

class KernelSVM:
    def __init__(self, C=1.0, kernel_type='rbf', epochs=1000, learning_rate=0.01, gamma=0.5, coef0=0, degree=3):
        """
        Initializes the Kernel SVM model with the specified hyperparameters.

        Parameters:
        - C: Regularization parameter. The strength of the regularization is inversely proportional to C.
        - kernel_type: The type of kernel function to use ('linear', 'polynomial', 'rbf', 'sigmoid').
        - epochs: The number of iterations over the training data.
        - learning_rate: The learning rate for the gradient descent optimization.
        - gamma: Kernel coefficient for 'rbf', 'polynomial', and 'sigmoid'.
        - coef0: Independent term in kernel function. It is only significant in 'polynomial' and 'sigmoid'.
        - degree: Degree of the polynomial kernel function ('polynomial').
        """
        self.C = C
        self.epochs = epochs
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.coef0 = coef0
        self.degree = degree
        self.kernel_type = kernel_type
        self.alpha = None
        self.b = None
        self.support_vectors = None
        self.support_labels = None
        self._y = None

    def kernel(self, x1, x2):
        """
        Computes the kernel function between two data points.

        Parameters:
        - x1: The first data point.
        - x2: The second data point.

        Returns:
        - The result of the kernel function applied to x1 and x2.
        """
        if self.kernel_type == 'linear':
            return np.dot(x1, x2)

        elif self.kernel_type == 'polynomial':
            return (self.gamma * np.dot(x1, x2) + self.coef0) ** self.degree

        elif self.kernel_type == 'rbf':
            return np.exp(-self.gamma * np.linalg.norm(x1 - x2) ** 2)

        elif self.kernel_type == 'sigmoid':
            return np.tanh(self.gamma * np.dot(x1, x2) + self.coef0)

        else:
            raise ValueError(f'Invalid Kernel {self.kernel}')

    def train(self, X, y):
        """
        Trains the Kernel SVM model using the provided dataset.

        Parameters:
        - X: The training data.
        - y: The target labels.

        Notes:
        - The training process involves updating the dual coefficients (alpha) and the bias term (b)
          using gradient descent.
        - The kernel matrix is precomputed to optimize the training process.
        """
        X = np.array(X)
        y = np.array(y)
        n_samples, n_features = X.shape
        y_ = np.where(y <= 0, -1, 1)  # Convert labels to -1 and 1
        self._y = y_

        self.alpha = np.zeros(n_samples)
        self.b = 0.0

        # Create the Kernel matrix
        K = np.zeros((n_samples, n_samples))
        for i in range(n_samples):
            for j in range(n_samples):
                K[i, j] = self.kernel(X[i], X[j])

        # Gradient descent optimization
        for _ in range(self.epochs):
            for i in range(n_samples):
                # Compute decision value
                decision_value = np.sum(self.alpha * y_ * K[:, i]) + self.b

                condition = y[i] * decision_value

                # Update alpha and bias
                if condition >= 1:
                    self.alpha[i] -= self.learning_rate * (self.alpha[i] - self.C * np.sum(y_ * K[:, i]))

                else:
                    self.alpha[i] -= self.learning_rate * (self.alpha[i] + self.C * (np.sum(y_ * K[:, i]) - 1))

                self.b -= self.learning_rate * y_[i] * (self.alpha[i] - self.C)

        # Identify support vectors (those with non-zero alpha)
        support_vector_indices = np.abs(self.alpha) > 1e-4
        self.support_vectors = X[support_vector_indices]
        self.support_labels = y_[support_vector_indices]
        self.alpha = self.alpha[support_vector_indices]

    def predict(self, X):
        """
        Predicts the class labels for the provided data points.

        Parameters:
        - X: The data points to classify.

        Returns:
        - An array of predicted class labels.
        """
        X = np.array(X)
        y_pred = []
        for x in X:
            prediction = np.sum(self.alpha * self.support_labels * np.array([self.kernel(x, sv) for sv in self.support_vectors])) + self.b
            y_pred.append(np.sign(prediction))

        return np.array(y_pred)

    def accuracy(self, y_true, y_pred):
        """
        Computes the accuracy of the model.

        Parameters:
        - y_true: The true class labels.
        - y_pred: The predicted class labels.

        Returns:
        - The accuracy score as a float.
        """
        return np.sum(y_true == y_pred) / len(y_true)

    def confusion_matrix(self, y_true, y_pred):
        """
        Computes the confusion matrix to evaluate the accuracy of the classification.

        Parameters:
        - y_true: The true class labels.
        - y_pred: The predicted class labels.

        Returns:
        - A confusion matrix as a 2D array.
        """
        unique_labels = np.unique(y_true)
        n_labels = len(unique_labels)

        matrix = np.zeros((n_labels, n_labels), dtype=np.int64)

        for i in range(len(y_true)):
            matrix[int(y_true[i]), int(y_pred[i])] += 1

        return matrix
