import numpy as np
import matplotlib.pyplot as plt

class PCA:
    """
    A simple implementation of Principal Component Analysis (PCA).

    Parameters:
    n_components: int
        The number of principal components to retain after dimensionality reduction.

    Attributes:
    pc: ndarray
        The principal components (eigenvectors) after fitting the model.
    mean: ndarray
        The mean of the features in the original data.
    """

    def __init__(self, n_components=2):
        """
        Initializes the PCA model with the specified number of components.

        Parameters:
        n_components: int
            Number of principal components to retain.
        """
        self.n_components = n_components
        self.pc = None
        self.mean = None

    def train(self, X):
        """
        Fits the PCA model to the input data.

        Parameters:
        X: ndarray
            The input data to perform PCA on, with shape (n_samples, n_features).

        Returns:
        pc: ndarray
            The principal components after fitting the model.

        Raises:
        ValueError: If the number of components is greater than the number of features.
        """
        X = np.array(X)
        if self.n_components > X.shape[1]:
            raise ValueError("n_components are more than Features... Please reduce n_components")

        # 1. Standardize the Data
        self.mean = np.mean(X, axis=0)
        X_centered = X - self.mean

        # 2. Build Co-Variance Matrix
        cov = np.cov(X_centered.T)

        # 3. Calculate EigenVectors and EigenValues
        eigenvalues, eigenvectors = np.linalg.eigh(cov)

        # Sort the eigenvectors by decreasing eigenvalues
        idx = np.argsort(eigenvalues)[::-1]
        eigenvectors = eigenvectors[:, idx]
        eigenvalues = eigenvalues[idx]

        # 4. Return the principal components
        self.pc = eigenvectors[:, :self.n_components]
        return self.pc

    def transform(self, X):
        """
        Applies the dimensionality reduction on the input data.

        Parameters:
        X: ndarray
            The input data to transform, with shape (n_samples, n_features).

        Returns:
        transformed_X: ndarray
            The data transformed into the principal component space.
        """
        X_centered = X - self.mean
        return np.dot(X_centered, self.pc)

    def train_transform(self, X, plot_graph=False):
        """
        Fits the PCA model and transforms the input data in one step.
        Optionally, plots the data in the reduced principal component space.

        Parameters:
        X: ndarray
            The input data to fit and transform, with shape (n_samples, n_features).
        plot_graph: bool, optional
            Whether to plot the transformed data. Only works for 1, 2, or 3 components.

        Returns:
        transformed_X: ndarray
            The data transformed into the principal component space.
        """
        self.train(X)
        transformed_X = self.transform(X)

        # Plot the transformed data if requested
        if plot_graph and self.n_components == 2:
            plt.scatter(transformed_X[:, 0], transformed_X[:, 1])
            plt.xlabel('PC1')
            plt.ylabel('PC2')
            plt.title("PCA")
            plt.show()
        elif plot_graph and self.n_components == 3:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(transformed_X[:, 0], transformed_X[:, 1], transformed_X[:, 2])
            ax.set_xlabel('PC1')
            ax.set_ylabel('PC2')
            ax.set_zlabel('PC3')
            plt.title("PCA")
            plt.show()
        elif plot_graph and self.n_components == 1:
            plt.scatter(transformed_X[:, 0], np.zeros(len(transformed_X)))
            plt.xlabel('PC1')
            plt.title("PCA")
            plt.show()

        return transformed_X
