from collections import defaultdict
from datetime import datetime
from itertools import chain
import os
import random

from clusterization_indices.davies_bouldin import DaviesBouldin
from clusterization_indices.xie_beni2 import XieBenniIndex
from clusterizations import FuzzyCMeans
from collectors import get_synops
from rules.rule import RuleGenerator, CompositionRule
from synop_parser import Normalizer
from visualization.visualize_clusters import ClusterVisualizer
import stations


NUM_CLUSTERS       = 7
RANDOM_INTS_RANGE  = 1000
SEPARATOR          = "\n----------------------------------\n"
WRITE_INFO         = True

def generate_random_membership_vector(num_clusters):
    rand_ints     = [random.randint(1, RANDOM_INTS_RANGE) for _ in xrange(num_clusters)]
    sum_rand_ints = sum(rand_ints)
    return [1. * rand_int / sum_rand_ints for rand_int in rand_ints]

def generate_random_membership_vectors(size, num_clusters):
    random.seed((datetime.now() - datetime(1900,1,1)).total_seconds())
    return [generate_random_membership_vector(num_clusters) for _ in xrange(size)]

def clusterize_stations(training_data, num_clusters=NUM_CLUSTERS, write_info=WRITE_INFO):
    header = " | ".join("Cluster %s" % i for i in range(1, num_clusters + 1)) + "\n"

    membership_degrees = generate_random_membership_vectors(len(training_data), num_clusters)
    if write_info:
        filename = 'exec_results\\Starting Membership Degrees.txt'
        check_and_create_file_dir(filename)
        with open(filename, "w+") as f:
            f.write( header )
            for membership_degree in membership_degrees:
                f.write(" | ".join(map(lambda x: "%8.7f" % x, membership_degree)) + '\n')

    clusterizer = FuzzyCMeans(training_data, membership_degrees)
    clusterizer()
    if write_info:
        filename = 'exec_results\\Cluster Table for Stations.txt'
        check_and_create_file_dir(filename)
        with open(filename, "w+") as f:
            f.write(header)
            for ind, station in enumerate(stations.STATIONS_INFORMATION):
                f.write(" | ".join(map(lambda x: "%8.7f" % x, clusterizer.membership_degrees[ind])) +\
                        " -> " + "%25s" % station.country + " " + "%25s" % station.city + " " + "%6s\n" % station.wmoind)

    return clusterizer

def analyzing_clusters_with_indices(training_data, min_clusters=3, max_clusters=12):
    filename = 'exec_results\\Cluster Analysis.txt'
    check_and_create_file_dir(filename)
    with open(filename, "w+") as f:
        f.write('Start of cluster analysis.\nTrying Davies-Bouldin Index with minimum %s and maximum %s clusters:\n' % (min_clusters, max_clusters)) 
        davies_bouldin = DaviesBouldin()
        davies_bouldin_results = []
        for num_clusters in range(min_clusters, max_clusters + 1):
            clusterizer = clusterize_stations(training_data, num_clusters=num_clusters, write_info=False)
            davies_bouldin_result = davies_bouldin.calculate_from_fuzzy_data(training_data, clusterizer.membership_degrees, clusterizer.centers)
            davies_bouldin_results.append([davies_bouldin_result, num_clusters])
            #TODO add results for the FuzzyCMeans
            f.write("Clusters %s. Davies-Bouldin Index: %s.\n" % (num_clusters, davies_bouldin_result))

        best_davies_bouldin_result = min(davies_bouldin_results)
        f.write("Best index result for %s clusters. Value of Davies-Bouldin index %s.\n" % (best_davies_bouldin_result[1], best_davies_bouldin_result[0]))    

        f.write('Start of cluster analysis.\nTrying Xie-Benni Index with minimum %s and maximum %s clusters:\n' % (min_clusters, max_clusters)) 
        xie_benni = XieBenniIndex()
        xie_benni_results = []
        for num_clusters in range(min_clusters, max_clusters + 1):
            clusterizer = clusterize_stations(training_data, num_clusters=num_clusters, write_info=False)
            xie_benni_result = xie_benni.calculate(training_data, clusterizer.membership_degrees, clusterizer.centers)
            xie_benni_results.append([xie_benni_result, num_clusters])
            f.write("Clusters %s. Xie-Benni Index: %s.\n" % (num_clusters, xie_benni_result))

        best_xie_benni_result = min(xie_benni_results)
        f.write("Best index result for %s clusters. Value of Xie-Benni index %s.\n" % (best_xie_benni_result[1], best_xie_benni_result[0]))    

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

def get_normed_rule_membership_vector(vector):
    vector_sum = sum(vector)
    return map(lambda x: x / vector_sum, vector)

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
    analyzing_clusters_with_indices(ordered_synop_normalized_vectors)

    # using indexize_cluster to separate clusters data to into
    # cluster number (zerobased)  fields of dictionary.
    indexed_clusters = indexize_cluster(ordered_synop_vectors, clusterizer.membership_degrees)
    if WRITE_INFO:
        filename = 'exec_results\\Data divided by Clusters.txt'
        check_and_create_file_dir(filename)
        with open(filename, "w+") as f:
            for cluster_index, indexed_cluster in indexed_clusters.items():
                f.write("____________Cluster %s____________\n" % cluster_index)
                f.write('\n'.join(map(str, indexed_cluster['data'])))
                f.write(SEPARATOR)
                f.write('\n'.join(map(str, indexed_cluster['membership_degrees'])))
                f.write(SEPARATOR + '\n\n')

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

if __name__ == '__main__':
    main()