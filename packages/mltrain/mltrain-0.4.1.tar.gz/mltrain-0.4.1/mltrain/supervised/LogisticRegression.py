import tensorflow as tf
import numpy as np


# Logistic Regression Model using TensorFlow for multiple features

class LogisticRegression:
    """
    A logistic regression model for binary classification using TensorFlow.

    Attributes:
        epochs (int): Number of epochs for training.
        learning_rate (float): Learning rate for gradient descent.
        W (tf.Variable): The weight vector of the model.
        b (tf.Variable): The bias term of the model.
        threshold_value (float): The threshold used for classification.
    """

    def __init__(self, epochs=1000, learning_rate=0.001, threshold_value=0.5):
        """
        Initializes the LogisticRegressionModel with the specified parameters.

        Args:
            epochs (int): The number of training epochs. Default is 1000.
            learning_rate (float): The learning rate for gradient descent. Default is 0.001.
            threshold_value (float): The threshold value for classifying predictions as 0 or 1. Default is 0.5.
        """
        self.epochs = epochs
        self.learning_rate = learning_rate
        self.W = None  # Weight vector will be initialized during training
        self.b = tf.Variable(np.random.rand(), dtype=tf.float32)  # Single bias term
        self.threshold_value = threshold_value

    def sigmoid(self, z):
        """
        Computes the sigmoid function for the input tensor `z`.

        Args:
            z (tf.Tensor): The input tensor, representing the linear combination of inputs and weights.

        Returns:
            tf.Tensor: The sigmoid activation of `z`.
        """
        return 1 / (1 + tf.exp(-z))

    def log_loss(self, y_true, y_pred):
        """
        Computes the binary cross-entropy loss (log loss) between the true labels and the predicted probabilities.

        Args:
            y_true (tf.Tensor): The true binary labels, a tensor of shape (num_samples,).
            y_pred (tf.Tensor): The predicted probabilities, a tensor of shape (num_samples,).

        Returns:
            tf.Tensor: The mean binary cross-entropy loss.
        """
        small_value = 1e-9  # Very small value to prevent log(0)
        y_pred = tf.clip_by_value(y_pred, small_value, 1 - small_value)
        loss = -tf.reduce_mean(y_true * tf.math.log(y_pred) + (1 - y_true) * tf.math.log(1 - y_pred))
        return loss

    def predict(self, X_pred):
        """
        Predicts the probability that each input sample belongs to the positive class (1).

        Args:
            X_pred (tf.Tensor or np.ndarray): The input features for which to predict probabilities.

        Returns:
            tf.Tensor: The predicted probabilities, a tensor of shape (num_samples,).
        """
        X_pred = tf.convert_to_tensor(X_pred, dtype=tf.float32)
        return self.sigmoid(tf.add(tf.matmul(X_pred, self.W), self.b))

    def train(self, x_train, y_train,print_loss=False):
        """
        Trains the logistic regression model using gradient descent.

        Args:
            x_train (tf.Tensor or np.ndarray): The input features for training, a tensor or array of shape (num_samples, num_features).
            y_train (tf.Tensor or np.ndarray): The true binary labels, a tensor or array of shape (num_samples,).
            print_loss (bool): Whether to print the loss during training for every 100 epochs. Default is False.

        Side effects:
            Updates the weight vector (W) and bias (b) of the model.
        """
        num_samples, num_features = x_train.shape
        self.W = tf.Variable(np.random.rand(num_features), dtype=tf.float32)  # Initialize weight vector
        x_train = tf.convert_to_tensor(x_train, dtype=tf.float32)  # Ensure input is a Tensor
        y_train = tf.convert_to_tensor(y_train, dtype=tf.float32)
        
        for epoch in range(self.epochs):
            with tf.GradientTape() as tape:
                y_pred = self.predict(x_train)
                loss = self.log_loss(y_train, y_pred)

            gradients = tape.gradient(loss, [self.W, self.b])

            if gradients[0] is None or gradients[1] is None:
                print("Gradient computation failed. Please check the computation graph.")
                continue

            self.W.assign_sub(self.learning_rate * gradients[0])
            self.b.assign_sub(self.learning_rate * gradients[1])

            if epoch % 100 == 0 and print_loss:
                print(f"Epoch {epoch}, Loss = {loss}")

    def predict_exact(self, X_pred):
        """
        Predicts the binary class (0 or 1) for each input sample based on the threshold value.

        Args:
            X_pred (tf.Tensor or np.ndarray): The input features for which to predict classes.

        Returns:
            tf.Tensor: The predicted binary classes, a tensor of shape (num_samples,).
        """
        return tf.where(self.predict(X_pred) >= self.threshold_value, 1, 0)
