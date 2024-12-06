import numpy as np
# Linear Regression Model using Gradient Descent

class LinearRegression:
    """
    A simple linear regression model that uses gradient descent for optimization.
    
    Attributes:
        learning_rate (float): The step size used for updating the weights.
        epochs (int): The number of iterations to run gradient descent.
        W (numpy.ndarray): The weights of the model.
        b (float): The bias term of the model.
    """

    def __init__(self, learning_rate=0.01, epochs=1000):
        """
        Initializes the LinearRegressionModel with a specified learning rate and number of epochs.
        
        Args:
            learning_rate (float): The learning rate for gradient descent. Default is 0.01.
            epochs (int): The number of epochs for training the model. Default is 1000.
        """
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.W = None
        self.b = None

    def predict(self, X):
        """
        Makes predictions based on the current weights and bias.
        
        Args:
            X (numpy.ndarray): The input features, a 2D array of shape (num_samples, num_features).
        
        Returns:
            numpy.ndarray: Predicted values, a 1D array of shape (num_samples,).
        """
        return np.dot(X, self.W) + self.b  # y = w1*x1 + w2*x2 + ... + wn*xn + b

    def compute_loss(self, Y, Y_pred):
        """
        Computes the Mean Squared Error (MSE) loss between the actual and predicted values.
        
        Args:
            Y (numpy.ndarray): The actual target values, a 1D array of shape (num_samples,).
            Y_pred (numpy.ndarray): The predicted values, a 1D array of shape (num_samples,).
        
        Returns:
            float: The mean squared error loss.
        """
        return np.mean((Y_pred - Y) ** 2)

    def train(self, X, Y,print_loss=False):
        """
        Trains the linear regression model using gradient descent.
        
        Args:
            X (numpy.ndarray): The input features, a 2D array of shape (num_samples, num_features).
            Y (numpy.ndarray): The actual target values, a 1D array of shape (num_samples,).
            print_loss (bool): Whether to print the loss during training for every 100 epochs. Default is False.
        
        Side effects:
            Updates the weights (W) and bias (b) of the model.
        """
        num_samples, num_features = X.shape
        self.W = np.zeros(num_features)  # Initialize weights to zero
        self.b = 0.0  # Initialize bias to zero

        for epoch in range(self.epochs):
            # Make predictions
            Y_pred = self.predict(X)
            # Calculate loss
            loss = self.compute_loss(Y, Y_pred)

            # Compute gradients
            dw = (1 / num_samples) * np.dot(X.T, (Y_pred - Y))  # Gradient of weights
            db = (1 / num_samples) * np.sum(Y_pred - Y)  # Gradient of bias

            # Clip gradients to avoid overflow
            grad_clip_value = 1e10
            dw = np.clip(dw, -grad_clip_value, grad_clip_value)
            db = np.clip(db, -grad_clip_value, grad_clip_value)

            # Update weights and bias
            self.W -= self.learning_rate * dw
            self.b -= self.learning_rate * db

            # Print loss every 100 epochs
            if epoch % 100 == 0 and print_loss:
                print(f"Epoch {epoch}, Loss: {loss}")

