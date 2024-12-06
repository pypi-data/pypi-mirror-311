import numpy as np

class KMeans:
    def __init__(self, k=3, epochs=100):
        """
        Initializes the KMeans model with the specified parameters.

        Parameters:
        - k: The number of clusters to form.
        - epochs: The maximum number of iterations for the algorithm.
        """
        self.k = k
        self.epochs = epochs
        self.centroids = None

    def euclidean(self, x1, x2):
        """
        Computes the Euclidean distance between two points.

        Parameters:
        - x1: The first data point.
        - x2: The second data point.

        Returns:
        - The Euclidean distance between x1 and x2.
        """
        return np.sqrt(np.sum((x1 - x2) ** 2))

    def get_cluster_labels(self, clusters, X):
        """
        Assigns labels to each data point based on the cluster it belongs to.

        Parameters:
        - clusters: A list of clusters, where each cluster is a list of indices of the data points.
        - X: The dataset.

        Returns:
        - An array of cluster labels for each data point in X.
        """
        labels = np.empty(X.shape[0])

        for cluster_idx, cluster in enumerate(clusters):
            for idx in cluster:
                labels[idx] = cluster_idx

        return labels

    def closest_centroid(self, x1):
        """
        Finds the index of the closest centroid to the given data point.

        Parameters:
        - x1: The data point.

        Returns:
        - The index of the closest centroid.
        """
        distances = [self.euclidean(x1, centroid) for centroid in self.centroids]
        return np.argmin(distances)

    def create_clusters(self, X):
        """
        Creates clusters by assigning each data point to the closest centroid.

        Parameters:
        - X: The dataset.

        Returns:
        - A list of clusters, where each cluster is a list of indices of the data points.
        """
        clusters = [[] for _ in range(self.k)]

        for idx, x1 in enumerate(X):
            closest_centroid_idx = self.closest_centroid(x1)
            clusters[closest_centroid_idx].append(idx)

        return clusters

    def create_new_centroids(self, clusters, X):
        """
        Updates the centroids by calculating the mean of all data points in each cluster.

        Parameters:
        - clusters: A list of clusters, where each cluster is a list of indices of the data points.
        - X: The dataset.

        Returns:
        - An array of updated centroids.
        """
        centroids = np.zeros((self.k, X.shape[1]))

        for idx, cluster in enumerate(clusters):
            cluster_mean = np.mean(X[cluster], axis=0)
            centroids[idx] = cluster_mean

        return centroids

    def train(self, X):
        """
        Trains the KMeans model by repeatedly assigning data points to the closest centroid
        and updating the centroids.

        Parameters:
        - X: The dataset.

        Returns:
        - An array of cluster labels for each data point in X.
        """
        # Initialize centroids by randomly selecting k data points from X
        self.centroids = X[np.random.choice(X.shape[0], self.k, replace=False)]

        for _ in range(self.epochs):
            # Create clusters by assigning data points to the closest centroid
            clusters = self.create_clusters(X)

            # Save old centroids to check for convergence
            old_centroids = self.centroids
            # Update centroids by calculating the mean of data points in each cluster
            self.centroids = self.create_new_centroids(clusters, X)

            # If centroids do not change, break the loop
            if np.all(old_centroids == self.centroids):
                break

        # Return the final cluster labels
        return self.get_cluster_labels(clusters, X)
