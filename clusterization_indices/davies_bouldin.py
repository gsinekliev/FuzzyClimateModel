__author__ = 'Admin'

from math import sqrt
from itertools import combinations
from utils import euclidean_distance
'''
Clusters should be list of clusters ( arrrays of vectors )}
Davis-bouldin index works with strict clustering so each element should be in one cluster
'''

class DavisBouldin(object):
    def __init__(self, clusters, centers):
        self.clusters = clusters
        self.centers = centers

    '''
    fuzzy_membership should be ELEMENTSxCLUSTERS matrix
    '''
    @classmethod
    def from_fuzzy_data( cls, individuals, fuzzy_membership, centers ):
        clusters = [[] for i in range (len(fuzzy_membership[0]))] # initialize empty clusters
        for i in range(len(individuals)):
            print "____________________"
            print len(fuzzy_membership[i])
            max_membership = max( fuzzy_membership[i])
            print "Max membership is " + str(max_membership)
            max_cluster = [ (index,value)
                            for index,value in enumerate(fuzzy_membership[ i ] ) if value == max_membership ][0][0]
            print "Max cluster index is " + str(max_cluster)
            clusters[ max_cluster ].append( individuals[i] )

        return cls( clusters, centers )

    def calculate(self):
        print "________________ENTER CALCULATE___________________"
        result =  max( [self.calculate_cluster_index(first, second)
                      for (first, second) in combinations(zip(self.clusters, self.centers), 2 )])
        print "___________________DONE________________"
        print result

    '''
    each argument is in the form ( vectors, center )
    '''
    def calculate_cluster_index(self, first, second):
        return ( self.calculate_scatter(first[0], first[1])
                 + self.calculate_scatter(second[0], second[1]) )    \
               / euclidean_distance(first[1], second[1])

    def calculate_scatter( self, cluster, center ):
        summed_distances = sum( [ euclidean_distance( individual, center ) for individual in cluster ] )
        return ( summed_distances+0. ) / len( cluster )