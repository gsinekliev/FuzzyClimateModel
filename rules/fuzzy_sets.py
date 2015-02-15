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
    def from_cluster_data(cls, values, membership_vector, threshold=0.):
        list = [(value, membership) for value, membership in zip(values, membership_vector) if membership > threshold]

        value_list = map(lambda x: x[0], list)
        membership_list = map(lambda x : x[1], list)

        min_value = min(value_list)
        max_value = max(value_list)
        average = sum([ value*membership for value, membership in zip(value_list, membership_list)]) \
                  		/ sum(membership_list)

        delta =(max_value - min_value)/100.0

        instance = cls(min_value - delta, average, max_value + delta)
        return instance

    def __repr__(self):
        print 'Triangle'
        print 'left: ' + str(self._left)
        print 'middle:' + str(self._top)
        print 'right:' + str(self._right)

    def get_membership_degree(self, value):
        result = 0
        if value <= self._left or value >= self._right:
            result = 0
        elif value <= self._top:
            result = (value - self._left) / (self._top - self._left)
        else:
            result = (self._right - value) / (self._right - self._top)
            
        return result



