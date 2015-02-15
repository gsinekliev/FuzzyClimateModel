from rules.fuzzy_sets import FuzzyTriangle

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
        # TODO: make rules by adding a fuzzy set for each attribute of synop_object and using cluster_index as consquent
        #for synop, membership_vector in zip( synop_objects, membership_matrix ):
        #    for attribute in synop.attributes_dict():
        #        rule.add_antecedent( Antecedent( FuzzyTriangle.from_cluster_data(  ) ),  )