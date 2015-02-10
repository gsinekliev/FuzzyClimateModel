import os
import random

import input as inp
from clusterizations import FuzzyCMeans

NUM_CLUSTERS      = 5
RANDOM_INTS_RANGE = 1000

def get_input_data( filename ):
    return inp.InputDataUtilities.getNumpyArrayListFromFile( os.getcwd() + '\\Data\\' + filename )

def generate_random_membership_vector( num_clusters ):
    rand_ints     = [ random.randint( 1, RANDOM_INTS_RANGE ) for _ in xrange( num_clusters ) ]
    # print rand_ints
    sum_rand_ints = sum( rand_ints )
    # print sum_rand_ints
    result = [ 1. * rand_int / sum_rand_ints for rand_int in rand_ints ]
    # print result
    return result

def generate_random_membership_vectors( size, num_clusters ):
    return [ generate_random_membership_vector( num_clusters ) for _ in xrange( size ) ]

import math
def normalize_training_data( training_data ):
    return [ map( lambda x: x / math.sqrt( sum( map( lambda x: x*x, item ) ) ), item ) for item in training_data ]

def main():
    # filename = 'data_norm_2012_2013.npy'
    # filename = 'data_temp_2012_2013.npy'
    filename = 'data_january_2012_2013.npy'
    training_data = [ t.flatten() for t in get_input_data( filename ) ]
    training_data = normalize_training_data( training_data )
    # print training_data

    membership_degrees = generate_random_membership_vectors( len( training_data ), NUM_CLUSTERS )
    # print membership_degrees

    clusterizer = FuzzyCMeans( training_data, membership_degrees )
    clusterizer()

    print '+++++++++++++++++++++++++++++++++'
    # for membership_degree in clusterizer.membership_degrees[ :10 ]:
    # for ind in xrange( 10 ):
    #     print '======================================='
    #     print zip( membership_degrees[ ind ], clusterizer.membership_degrees[ ind ] )
    #     print membership_degrees[ ind ]
    #     print clusterizer.membership_degrees[ ind ]

    # print '___________________________ITERATIONS___________________________'
    # print clusterizer.iterations

    # for center in clusterizer.centers:
    #     print '======================================='
    #     print center
    
    # for membership_degree in membership_degrees[ :10 ]:
    #     print '======================================='
    #     print membership_degree

    count = [ 0 ] * 5
    for membership_degree in clusterizer.membership_degrees:
        max_ind = 0
        for ind in xrange( 1, NUM_CLUSTERS ):
            if membership_degree[ ind ] > membership_degree[ max_ind ]:
                max_ind = ind

        count[ max_ind ] += 1

    print count
    print clusterizer.iterations

    # named_training_data = zip( inp.perc_cities, training_data)
    # print named_training_data

if __name__ == '__main__':
    main()