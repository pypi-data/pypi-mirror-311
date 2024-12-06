import numpy as np
from collections import deque

class DBSCAN:
    def __init__(self, epsilon=0.5, min_points=5):
        """
        Initializes the DBSCAN model with the specified parameters.

        Parameters:
        - epsilon: The maximum distance between two samples for one to be considered as in the neighborhood of the other.
        - min_points: The number of samples in a neighborhood for a point to be considered as a core point.
        """
        self.epsilon = epsilon
        self.min_points = min_points
        self.labels = None
        self.cluster_id = 0

    def train(self, X):
        """
        Trains the DBSCAN model using the provided dataset.

        Parameters:
        - X: The input data points.

        Returns:
        - The labels assigned to each point in the dataset. A label of -1 indicates noise.
        """
        n_samples = X.shape[0]
        self.labels = np.full(n_samples, -1)  # Initialize all points as noise (-1)
        visited_samples = np.zeros(n_samples, dtype=bool)  # Keep track of visited points
        distance_matrix = self.compute_distance_matrix(X)  # Precompute the distance matrix

        for i in range(n_samples):
            if not visited_samples[i]:
                visited_samples[i] = True
                neighbours = self.region_query(i, distance_matrix)  # Find neighbors within epsilon

                if len(neighbours) >= self.min_points:
                    # If the point is a core point, form a cluster
                    self.append_cluster(i, neighbours, visited_samples, distance_matrix, self.cluster_id)
                    self.cluster_id += 1
                else:
                    self.labels[i] = -1  # Mark it as noise

        return self.labels

    def compute_distance_matrix(self, X):
        """
        Computes the pairwise distance matrix for the dataset.

        Parameters:
        - X: The input data points.

        Returns:
        - A distance matrix where the entry (i, j) represents the distance between point i and point j.
        """
        n_samples = X.shape[0]
        distance_matrix = np.zeros((n_samples, n_samples))

        for i in range(n_samples):
            for j in range(i + 1, n_samples):
                distance_matrix[i, j] = distance_matrix[j, i] = np.linalg.norm(X[i] - X[j])

        return distance_matrix

    def region_query(self, i, distance_matrix):
        """
        Finds all points within epsilon distance from point i.

        Parameters:
        - i: The index of the point to query.
        - distance_matrix: The precomputed distance matrix.

        Returns:
        - An array of indices of all points within epsilon distance from point i.
        """
        return np.where(distance_matrix[i] <= self.epsilon)[0]

    def append_cluster(self, i, neighbours, visited_samples, distance_matrix, cluster_id):
        """
        Expands the cluster by adding all density-reachable points.

        Parameters:
        - i: The index of the initial core point.
        - neighbours: The initial set of neighbors within epsilon distance.
        - visited_samples: A boolean array indicating whether each point has been visited.
        - distance_matrix: The precomputed distance matrix.
        - cluster_id: The current cluster id to assign to points.
        """
        self.labels[i] = cluster_id
        queue = deque(neighbours)  # Use a queue to manage the expansion process

        while queue:
            j = queue.popleft()

            if not visited_samples[j]:
                visited_samples[j] = True
                new_neighbours = self.region_query(j, distance_matrix)

                if len(new_neighbours) >= self.min_points:
                    queue.extend(new_neighbours)  # Continue expanding the cluster

            if self.labels[j] == -1:  # If the point was previously marked as noise, reassign it to the cluster
                self.labels[j] = cluster_id

    def get_labels(self):
        """
        Returns the labels assigned to the data points after training.

        Returns:
        - An array of labels where each label corresponds to a cluster id, or -1 for noise.
        """
        return self.labels
