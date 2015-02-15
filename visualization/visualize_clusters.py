import matplotlib
import pylab
import numpy
from itertools import cycle

from collections import defaultdict

class ClusterVisualizer(object):
    @classmethod
    def visualize_clusters(cls, synop_objects, membership_matrix):
        '''
        visualize clusters and cluster centers
        '''

        #group clusters
        print synop_objects[0]

        cities_dict = {}
        for i in xrange(0, len(membership_matrix)):
            maximal_membership = max(membership_matrix[i])
            cluster_index = [index for index, value in enumerate(membership_matrix[i])
                             if value == maximal_membership][0]
            cities_dict[i] = cluster_index

        clusters_dict = defaultdict(list)
        for city_index, cluster_index in cities_dict.iteritems():
            clusters_dict[cluster_index].append(city_index)

        col_gen = cycle('bgrcmk')

        for cluster_index, cities_list in clusters_dict.iteritems():
            matplotlib.pyplot.scatter([getattr(synop_objects[i], 'temperature').value for i in cities_list],
                                      [getattr(synop_objects[i], 'station_pressure').value for i in cities_list],
                                       color=col_gen.next())

        matplotlib.pyplot.xlabel('temperature', fontsize=16)
        matplotlib.pyplot.ylabel('pressure', fontsize=16)

        matplotlib.pyplot.show()
