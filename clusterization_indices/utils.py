__author__ = 'Admin'

from math import sqrt

def euclidean_distance( first, second ):
    sum = 0
    for i,j in zip( first, second ):
        sum += abs( i - j )**2
    return sqrt( sum )

if __name__ == "__main__":
    print "Euclidean distance between"
    print "(0,0) and (1 1)"
    print euclidean_distance([0,0],[1,1] )
    print "(1,2) and (1,2 )"
    print euclidean_distance((1,2),(1,2) )