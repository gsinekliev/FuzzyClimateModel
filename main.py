import os
import random

import input as inp
from clusterizations import FuzzyCMeans
from clusterization_indices.davies_bouldin import DavisBouldin
from clusterization_indices.xie_beni2 import XieBenniIndex
from rules.rule import RuleGenerator, CompositionRule
from collectors import get_synops

from visualization.visualize_clusters import ClusterVisualizer
import stations
from synop_parser import Normalizer

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


def clusterize_stations( ordered_synop_normalized_vectors, month, year=2015 ):
    training_data       = ordered_synop_normalized_vectors
    print '_______________TRAINING_DATA_______________'
    print training_data
    membership_degrees  = generate_random_membership_vectors( len( training_data ), NUM_CLUSTERS )
    # membership_degrees  = generate_random_membership_vectors( len( training_data ), NUM_CLUSTERS )
    print '____________MEMBERSHIP_DEGREES_____________'
    print membership_degrees
    clusterizer         = FuzzyCMeans( training_data, membership_degrees )
    clusterizer()
    print " Cluster 1 | Cluster 2 | Cluster 3 | Cluster 4 | Cluster 5 "
    for ind, station in enumerate( stations.STATIONS_INFORMATION ):
        print " " + " | ".join( map( lambda x: "%8.7f" % x, clusterizer.membership_degrees[ ind ] ) ) + " -> " + "%25s" % station.country + " " + "%25s" % station.city + " " + "%6s" % station.wmoind

    return clusterizer

from collections import defaultdict

def get_index_of_max_item( vector ):
    max_ind, max_value = -1, 0
    for ind in xrange( len( vector ) ):
        if vector[ ind ] > max_value:
            max_value = vector[ ind ]
            max_ind = ind

    return max_ind


def indexize_cluster(clusterizer, ordered_synop_vectors):
    indexed_clusters = defaultdict(lambda: defaultdict(list, []))
    for ind in xrange(len(clusterizer.membership_degrees)):
        cluster_index = get_index_of_max_item( clusterizer.membership_degrees[ind])
        indexed_clusters[cluster_index]['raw_data'].append(ordered_synop_vectors[ind])
        indexed_clusters[cluster_index]['data'].append(Normalizer.get_unnormalized_vector(ordered_synop_vectors[ind]))
        indexed_clusters[cluster_index]['membership_degrees'].append(clusterizer.membership_degrees[ind])

    return indexed_clusters


if __name__ == '__main__':
    # main()
    station_indices = [ st_info.wmoind for st_info in stations.STATIONS_INFORMATION ]
    month  = '01'
    synops = get_synops(station_indices, month)
    print '___________GETTING_SYNOP_RESULTS___________'
    print synops
    ordered_synops                   = [synops[ station_index ] for station_index in station_indices]
    ordered_synop_vectors            = [synop.vector() for synop in ordered_synops]
    print '______ORDERED_NORMALIZED_VECTORS___________'
    print '\n'.join( map( str, ordered_synop_vectors ) )
    ordered_synop_normalized_vectors = [ synop.normalized_vector() for synop in ordered_synops ]
    clusterizer = clusterize_stations(ordered_synop_normalized_vectors, month)
    indexed_clusters = indexize_cluster(clusterizer, ordered_synop_vectors)

    clusters_count = len(clusterizer.membership_degrees[0])


    # for cluster_index, indexed_cluster in indexed_clusters.items():
    #     print "_________________________Cluster " + str(cluster_index)
    #     print '\n'.join( map( str, indexed_cluster[ 'data' ] ) )
    #     # print "----------------------------------"
    #     # print '\n'.join( map( str, indexed_cluster[ 'raw_data' ] ) )
    #     print "----------------------------------"
    #     print '\n'.join( map( str, indexed_cluster[ 'membership_degrees' ] ) )

    composer = CompositionRule()
    denormed_vectors = [ Normalizer.get_unnormalized_vector(ordered_synop_vector)
                             for ordered_synop_vector in ordered_synop_vectors ]
    for cluster_index in xrange(clusters_count):
        composer.add_cluster_rule(RuleGenerator.generate_rule(denormed_vectors,
                                                              clusterizer.membership_degrees,
                                                              cluster_index))

    print "__________________COMPOSE_RULES__________________"
    test_set = []
    for indexed_cluster in indexed_clusters.values():
        for ind in xrange(len(indexed_cluster['data'])):
            test_set.append((indexed_cluster['data'][ind], indexed_cluster['membership_degrees'][ind]))

    print test_set
    for ind, item in enumerate( test_set ):
        print '=======================TEST %s=======================' % ind
        print composer.conclusion_vector(item[0])
        print item[1]

    #ClusterVisualizer.visualize_clusters(ordered_synops, clusterizer.membership_degrees)
