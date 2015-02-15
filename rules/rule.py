__author__ = 'Admin'

from rules.fuzzy_sets import FuzzyTriangle
from synop_parser import Synop


class Antecedent(object):
    def __init__(self, fuzzy_input, label):
        self.fuzzy_input = fuzzy_input
        self.label = label

'''
Represents fuzzy rule
'''
class Rule(object):
    def __init__(self, and_operation = min):
        self._if_part = []   # list of input fuzzy sets
        self._then_part = -1 # index if cluster
        self._and_operation = and_operation

    '''
    Antecedent is fuzzy set for
    '''
    def add_antecedent(self, antecedent):
        self._if_part.append(antecedent)

    def add_consequent(self, cluster_index):
        self._then_part = cluster_index

    def rule_confidence_level(self, input_vector):
        return self._and_operation( [ antecedent.fuzzy_input.get_membership_degree( input_vector[ ind ] )
                                      for ind, antecedent in enumerate( self._if_part ) ] )

class RuleGenerator(object):
    @staticmethod
    def generate_rule(synop_objects, membership_matrix, cluster_index):
        """
            for one cluster passing synop_objects, membership_matrix for them and cluster_index
        """
        rule = Rule()
        
        attributes_values = {key : [ getattr(synop, key) for synop in synop_objects ] for key in Synop().attributes()}
        for label, values in attributes_values:
            membership_vector = [ row[ cluster_index ] for row in membership_matrix ]
            rule.add_antecedent(Antecedent(FuzzyTriangle.from_cluster_data( values, membership_vector, 0.25 )))

        rule.add_consequent(cluster_index)
        return rule

class CompositionRule( object ):
    def __init__( self, cluster_rules=[] ):
        self.cluster_rules = cluster_rules

    def add_cluster_rule( self, rule ):
        self.cluster_rules.append( rule )

    def conclusion_vector( self, input_vector ):
        return [ cluster_rule.rule_confidence_level( input_vector ) for cluster_rule in self.cluster_rules ]