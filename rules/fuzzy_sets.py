__author__ = 'Admin'

'''
Creates fuzzy triangle or other shape from cluster index
'''
class FuzzyTriangle(object):
    def __init__( self, left, top, right ):
        self._left  = left
        self._top   = top
        self._right = right

    '''
    creates fuzzy triangle set from set of values and membership_vector that contains the membership degree
    of each element
    '''
    @classmethod
    def from_cluster_data(cls, values, membership_vector, threshold = 0. ):
        average = sum([ value*membership for value, membership in zip(values,membership_vector) ]) \
                  / sum( membership_vector )

        filteredValues = [value for value, membership in zip(values,membership_vector) if membership > threshold]
        minValue = min( filteredValues )
        maxValue = max( filteredValues )

        return cls( minValue, average, maxValue )

    def get_membership_degree(self, value):
        if value <= self._left or value >= self._right:
            return 0
        elif value <= self._top:
            return ( value - self._left ) / ( self._top - self._left )
        else:
            return ( self._right - value ) / ( self._right - self._top )



