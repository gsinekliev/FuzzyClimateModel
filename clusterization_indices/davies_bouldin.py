__author__ = 'Admin'

from itertools import combinations
from math import sqrt
from utils import euclidean_distance


class DaviesBouldin(object):
    """ Clusters should be list of clusters (arrays of vectors)
        Davis-Bouldin index works with strict clustering (Crisp Sets),
        so each element should be in one cluster
    """
    @classmethod
    def calculate_from_fuzzy_data( cls, individuals, fuzzy_membership, centers ):
        """ Parameter fuzzy_membership should be ELEMENTS x CLUSTERS matrix
        """
        clusters = [[] for _ in range(len(fuzzy_membership[0]))] # initialize empty clusters
        for ind in range(len(individuals)):
            max_membership = max(fuzzy_membership[ind])
            max_cluster    = [(index, value) for index, value in enumerate(fuzzy_membership[ind]) if value == max_membership][0][0]
            clusters[max_cluster].append(individuals[ind])

        return cls.calculate(clusters, centers)

    @classmethod
    def calculate(cls, clusters, centers):
        """ Average of maximal cluster indices between all centroids and centroid
        """
        centroids = zip(clusters, centers)
        return sum(max(cls.calculate_cluster_index(first, second) for second in centroids if list(second[1]) != list(first[1])) for first in centroids) / len(clusters)

    @classmethod
    def calculate_cluster_index(cls, first, second):
        """ Both first and second are in the form (vectors, center)
        """
        return (cls.calculate_scatter(*first) + cls.calculate_scatter(*second)) / euclidean_distance(first[1], second[1])

    @classmethod
    def calculate_scatter(cls, cluster_individuals, center):
        """ Calculates the scatter of cluster.
        """
        return (sum(euclidean_distance(individual, center) for individual in cluster_individuals) + 0.) / len(cluster_individuals)