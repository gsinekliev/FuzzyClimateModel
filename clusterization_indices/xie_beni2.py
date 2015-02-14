__author__ = 'Admin'

from utils import euclidean_distance
from itertools import combinations

'''
This index measures the within-group variance of distances between individual and cluster center
Also takes into account the squared distance between cluster centers
http://homes.di.unimi.it/~valenti/SlideCorsi/Bioinformatica05/Fuzzy-Clustering-lecture-Babuska.pdf
'''
class XieBenniIndex:
    def __init__(self, fuzzyness_parameter = 2, xie_beni_constant = 1):
        self._m = fuzzyness_parameter
        self._c = xie_beni_constant

    '''
    fuzzy_membership should be ELEMENTSxCLUSTERS matrix
    '''
    def calculate(self, individuals, membership_matrix, centers ):
        min_cluster_distance = min( [ euclidean_distance( first, second )**2
                                      for first,second in combinations(centers,2) ] )

        sum = 0
        for cluster_index in xrange(len(centers)):
            for individual_index in xrange(len(individuals)):
                membership = membership_matrix[ individual_index ][ cluster_index ]**self._m
                distance = euclidean_distance( individuals[ individual_index ], centers[ cluster_index ] )**2
                sum += membership * distance

        return sum / min_cluster_distance * self._c




