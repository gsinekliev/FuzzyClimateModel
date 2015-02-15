import os
import random

import input as inp
from clusterizations import FuzzyCMeans
from clusterization_indices.davies_bouldin import DavisBouldin
from clusterization_indices.xie_beni2 import XieBenniIndex
from collectors import get_synops
import stations

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

    print training_data
    print "_______________________"
    training_data = normalize_training_data( training_data )
    print training_data

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
        # cities_dict[   ]
        count[ max_ind ] += 1

    print clusterizer.membership_degrees
    print len( membership_degrees )

    # cities_dict = {}
    # for i in xrange( 0, len( clusterizer.membership_degrees ) ):
    #     maximalMembership = max(clusterizer.membership_degrees[ i ] )
    #     clusterIndex = [ k for k,j in enumerate(clusterizer.membership_degrees[ i ] ) if j == maximalMembership ][0]
    #     cities_dict[ inp.cities_names[ i ] ] = clusterIndex;
    #
    # print cities_dict
    #
    # from collections import defaultdict
    #
    # clusters_dict = defaultdict(list)
    # for city_name, cluster_index in cities_dict.iteritems():
    #     print city_name + "-->" + str(cluster_index)
    #     clusters_dict[ cluster_index ].append( city_name )
    #
    # for key,value in clusters_dict.iteritems():
    #     print "Cluster " + str( key )
    #     print '\n'.join( value )
    #     print "________________"

    d_bouldinCalculator = DavisBouldin()
    print "Bouldin index" + str( d_bouldinCalculator.calculate_from_fuzzy_data(training_data, clusterizer.membership_degrees,
                                                           clusterizer.centers) )

    xie_beni = XieBenniIndex()
    print "Xie Beni index" + \
          str(xie_beni.calculate( training_data, clusterizer.membership_degrees, clusterizer.centers ))


    #cities_dict = { inp.cities_names[ index ] : membership_degree[ index ] for index in xrange( len( clusterizer.membership_degrees) ) }

    #print cities_dict

    #print count


    #print clusterizer.iterations

    # named_training_data = zip( inp.perc_cities, training_data)
    # print named_training_data


def clusterize_stations( station_indices, month, year=2015 ):
    synops              = get_synops( station_indices, month, year )
    print '___________GETTING_SYNOP_RESULTS___________'
    print synops
    training_data       = [ synops[ station_index ].normalized_vector() for station_index in station_indices ]
    print '_______________TRAINING_DATA_______________'
    print training_data
    membership_degrees  = generate_random_membership_vectors( len( training_data ), NUM_CLUSTERS )
    print '____________MEMBERSHIP_DEGREES_____________'
    print membership_degrees
    clusterizer         = FuzzyCMeans( training_data, membership_degrees )
    clusterizer()
    print " Cluster 1 | Cluster 2 | Cluster 3 | Cluster 4 | Cluster 5 "
    for ind, station in enumerate( stations.STATIONS_INFORMATION ):
        print " " + " | ".join( map( lambda x: "%8.7f" % x, clusterizer.membership_degrees[ ind ] ) ) + " -> " + "%25s" % station.country + " " + "%25s" % station.city + " " + "%6s" % station.wmoind

    # for membership_degree in clusterizer.membership_degrees[ :10 ]:
    # for ind in xrange( 10 ):
if __name__ == '__main__':
    # main()

    results = clusterize_stations( [ st_info.wmoind for st_info in stations.STATIONS_INFORMATION ], '01' )