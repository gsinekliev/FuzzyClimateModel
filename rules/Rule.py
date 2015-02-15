from rules.fuzzy_sets import FuzzyTriangle
from synop_parser import Synop

__author__ = 'Admin'

class Antecedent:
    def __init(self, fuzzyInput, label):
        self.fuzzyInput = fuzzyInput
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
    def add_antecedent(self, antecedent ):
        self._if_part.append(antecedent)

    def add_consequent(self, cluster_index):
        self._then_part = cluster_index

    def rule_confidence_level(self):
        return self._and_operation([antecedent.get_membership_degree for antecedent in self._if_part])

class RuleGenerator(object):
    def __init__(self):
        pass

    def generate_rule(self, synop_objects, membership_matrix, cluster_index):
        rule = Rule()

        attributes_values = {key : [ getattr(synop, key) for synop in synop_objects ] for key in Synop().attributes()}
        for label, values in attributes_values:
            membership_vector = [ row[ cluster_index ] for row in membership_matrix ]
            rule.add_antecedent(Antecedent(FuzzyTriangle.from_cluster_data( values, membership_vector, 0.25 )))

        rule.add_consequent(cluster_index)
        return rule
