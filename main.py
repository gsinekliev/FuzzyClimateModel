from collections import defaultdict
from itertools import chain
import os
import random

from clusterization_indices.davies_bouldin import DavisBouldin
from clusterization_indices.xie_beni2 import XieBenniIndex
from clusterizations import FuzzyCMeans
from collectors import get_synops
from rules.rule import RuleGenerator, CompositionRule
from synop_parser import Normalizer
from visualization.visualize_clusters import ClusterVisualizer
import stations

NUM_CLUSTERS      = 5
RANDOM_INTS_RANGE = 1000
WRITE_INFO        = False

def generate_random_membership_vector(num_clusters):
    rand_ints     = [random.randint(1, RANDOM_INTS_RANGE) for _ in xrange(num_clusters)]
    sum_rand_ints = sum(rand_ints)
    return [1. * rand_int / sum_rand_ints for rand_int in rand_ints]

def generate_random_membership_vectors(size, num_clusters):
    return [generate_random_membership_vector(num_clusters) for _ in xrange(size)]

def clusterize_stations(training_data):
    header = "Cluster 1 | Cluster 2 | Cluster 3 | Cluster 4 | Cluster 5\n"

    #Q could be moved in function to use stored or newly generated values. 
    membership_degrees = generate_random_membership_vectors(len(training_data), NUM_CLUSTERS)
    if WRITE_INFO:
        filename = 'exec_results\\Starting Membership Degrees.txt'
        check_and_create_file_dir(filename)
        with open(filename, "w+") as f:
            f.write( header )
            for membership_degree in membership_degrees:
                f.write(" | ".join(map(lambda x: "%8.7f" % x, membership_degree)) + '\n')

    clusterizer = FuzzyCMeans(training_data, membership_degrees)
    clusterizer()
    if WRITE_INFO:
        filename = 'exec_results\\Cluster Table for Stations.txt'
        check_and_create_file_dir(filename)
        with open(filename, "w+") as f:
            f.write(header)
            for ind, station in enumerate(stations.STATIONS_INFORMATION):
                f.write(" | ".join(map(lambda x: "%8.7f" % x, clusterizer.membership_degrees[ind])) +\
                        " -> " + "%25s" % station.country + " " + "%25s" % station.city + " " + "%6s\n" % station.wmoind)

    return clusterizer

def get_cluster_index_from_membership_degrees(vector):
    max_ind, max_value = 0, 0
    for ind in xrange(len(vector)):
        if vector[ind] > max_value:
            max_value = vector[ind]
            max_ind   = ind

    return max_ind

def indexize_cluster(ordered_synop_vectors, membership_degrees):
    indexed_clusters = defaultdict(lambda: defaultdict(list, []))
    for ind in xrange(len(membership_degrees)):
        cluster_index = get_cluster_index_from_membership_degrees(membership_degrees[ind])
        indexed_clusters[cluster_index]['data'].append(Normalizer.get_unnormed_vector(ordered_synop_vectors[ind]))
        indexed_clusters[cluster_index]['membership_degrees'].append(membership_degrees[ind])

    return indexed_clusters

def check_and_create_file_dir(filename):
    if not os.access(filename, os.R_OK):
        filedir = os.path.dirname(filename)
        if not os.path.exists(filedir):
            os.makedirs(filedir)

def main(month='01', year=2015):
    """ Main entrance to the program, arguments are used to
        declare month and year of observations.
    """
    # ordered wmo_indece
    station_wmo_indices = [station_info.wmoind for station_info in stations.STATIONS_INFORMATION]

    # synops is a dictionary of wmo_index pointing synop data for station.
    synops = get_synops(station_wmo_indices, month, year)

    # using stations order to generate ordered lists of synop objects, synop vectors, synop normalized vectors
    ordered_synop_objects            = [synops[station_index] for station_index in station_wmo_indices]

    ordered_synop_vectors            = [synop.vector() for synop in ordered_synop_objects]
    ordered_synop_normalized_vectors = [synop.normalized_vector() for synop in ordered_synop_objects]

    # calling clusterize which will generate random membership degrees,
    # and will call FuzzyCMeans to calculate actuoal membership degrees
    clusterizer = clusterize_stations(ordered_synop_normalized_vectors)

    # analyzing clusters
    if WRITE_INFO:
        print 'Analyzing clusters:'
        davis_bouldin = DavisBouldin()
        print "Bouldin index " + str(davis_bouldin.calculate_from_fuzzy_data(ordered_synop_normalized_vectors,
                                                        clusterizer.membership_degrees, clusterizer.centers))

        xie_beni = XieBenniIndex()
        print "Xie Beni index " + str(xie_beni.calculate(ordered_synop_normalized_vectors,
                                    clusterizer.membership_degrees, clusterizer.centers))

    # using indexize_cluster to separate clusters data to into
    # cluster number (zerobased)  fields of dictionary.
    indexed_clusters = indexize_cluster(ordered_synop_vectors, clusterizer.membership_degrees)
    if WRITE_INFO:
        filename = 'exec_results\\Data divided by Clusters.txt'
        check_and_create_file_dir(filename)
        with open(filename, "w+") as f:
            separator = "\n----------------------------------\n"
            for cluster_index, indexed_cluster in indexed_clusters.items():
                f.write("____________Cluster %s____________\n" % cluster_index)
                f.write('\n'.join(map(str, indexed_cluster['data'])))
                f.write(separator)
                f.write('\n'.join(map(str, indexed_cluster['membership_degrees'])))
                f.write(separator + '\n\n')

    clusters_count = len(clusterizer.centers)
    composer = CompositionRule()
    denormed_vectors = [ Normalizer.get_unnormed_vector(ordered_synop_vector)
                             for ordered_synop_vector in ordered_synop_vectors ]
    for cluster_index in xrange(clusters_count):
        composer.add_cluster_rule(RuleGenerator.generate_rule(denormed_vectors,
                                                              clusterizer.membership_degrees,
                                                              cluster_index))
                                                              
    if WRITE_INFO:
        filename = 'exec_results\\Testing Composition Rule with Training Data.txt'
        check_and_create_file_dir(filename)
        with open(filename, "w+") as f:
            test_set = chain.from_iterable(zip(indexed_cluster['data'],indexed_cluster['membership_degrees'])
                                           for indexed_cluster in indexed_clusters.values())
            for ind, item in enumerate(test_set):
                f.write('=======================TEST %s=======================\n' % ind)
                f.write(' '.join(map(str, get_normed_rule_membership_vector(composer.conclusion_vector(item[0])))))
                f.write('\n')
                f.write(' '.join(map(str, item[1])))
                f.write('\n\n')

    ClusterVisualizer.visualize_clusters(ordered_synop_objects, clusterizer.membership_degrees)

def get_normed_rule_membership_vector(vector):
    summed = sum(vector)
    result = [i/summed for i in vector]
    return result

if __name__ == '__main__':
    WRITE_INFO   = True
    # NUM_CLUSTERS = 7
    main()