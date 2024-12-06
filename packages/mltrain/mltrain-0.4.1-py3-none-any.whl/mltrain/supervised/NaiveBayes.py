import numpy as np
class NaiveBayes:
    def __init__(self):
        """
        Initializes the Naive Bayes model with empty dictionaries for storing
        class statistics such as mean, variance, prior probabilities, and class labels.
        """
        self.mean = {}
        self.var = {}
        self.class_prob = {}
        self.prior = {}
        self.classes = None

    def train(self, X, y):
        """
        Trains the Naive Bayes model by calculating the mean, variance, and prior probability
        for each class based on the provided training data.
        
        Parameters:
        - X (array-like): Input features for training.
        - y (array-like): Corresponding labels for the input features.
        
        Returns:
        - None: This method does not return any value.
        """
        X = np.array(X)
        y = np.array(y)

        # Find unique classes and their counts
        self.classes, self.classes_count = np.unique(y, return_counts=True)

        n_samples, n_features = X.shape

        for c in self.classes:
            # Create a boolean mask for the current class
            class_mask = (y == c)
            class_features = X[class_mask]
            
            # Calculate mean and variance for each feature in the class
            self.mean[c] = np.mean(class_features, axis=0)
            self.var[c] = np.var(class_features, axis=0)
            
            # Calculate prior probability of the class
            self.prior[c] = self.classes_count[c] / n_samples

    def predict(self, X):
        """
        Predicts the class labels for the provided input samples based on the trained model.
        
        Parameters:
        - X (array-like): Input features for which to predict the class labels.
        
        Returns:
        - numpy.ndarray: Predicted class labels for each input sample.
        """
        y_pred = []

        for sample in X:
            class_likelihoods = []

            for c in self.classes:
                mean = self.mean[c]
                var = self.var[c]
                prior = self.prior[c]

                # Calculate the likelihood of each feature value given the class
                likelihood = -0.5 * np.sum(np.log(2 * np.pi * var))
                likelihood -= 0.5 * np.sum(((sample - mean) ** 2) / var)

                # Combine likelihood with prior
                class_likelihoods.append(likelihood + np.log(prior))

            # Predict the class with the highest likelihood
            y_pred.append(self.classes[np.argmax(class_likelihoods)])

        return np.array(y_pred)

    def accuracy(self, y_true, y_pred):
        """
        Calculates the accuracy of the model's predictions.
        
        Parameters:
        - y_true (array-like): True class labels.
        - y_pred (array-like): Predicted class labels.
        
        Returns:
        - float: The accuracy of the predictions.
        """
        accuracy = np.sum(y_true == y_pred) / len(y_true)
        return accuracy

    def confusion_matrix(self, y_true, y_pred):
        """
        Computes the confusion matrix to evaluate the performance of the classification model.
        
        Parameters:
        - y_true (array-like): True class labels.
        - y_pred (array-like): Predicted class labels.
        
        Returns:
        - numpy.ndarray: The confusion matrix.
        """
        labels, counts = np.unique(y_true, return_counts=True)
        matrix = np.zeros((len(labels), len(labels)))

        for i in range(len(y_true)):
            matrix[int(y_true[i]), int(y_pred[i])] += 1

        return matrix
