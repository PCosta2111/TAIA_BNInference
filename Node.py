"""
This is a class that implements a node in a Bayesian network.
The distribution field is a dictionary containing the conditional probability distribution of the node given its parents.
The keys to the dictionary are tuples containing the names of the possible states of the node and the evidence of the parents
for each line in the CPD table. If a node has no parents, the distribution will store the marginal distribution.
This is my implementation for a node. Feel free to alter it based on your own design for what a node should look like.
If you change the node constructor parameters, however, remember to change the BIF parse script so that the number of variables
received by the constructor is the same as the number of variables given to the constructor.
"""
from __future__ import division

__author__ = "Antoine Bosselut"
__version__ = "1.0.4"
__maintainer__ = "Antoine Bosselut"
__email__ = "antoine.bosselut@uw.edu"
__status__ = "Prototype"

from pprint import pprint


class Node:
    def __init__(self, the_name, the_type, number_states, the_states, the_property):
        self.name = the_name
        self.myType = the_type
        self.numStates = number_states
        self.states = the_states
        self.parents = []
        self.children = []
        self.information = []
        self.dist = None
        self.myProperty = the_property
        self.marginal = None

    # Add children when building the BN
    def add_children(self, the_children):
        for a in the_children:
            self.children.append(a)

    # Add parents to a state when building the BN
    def add_parent(self, the_parents):
        for a in the_parents:
            self.parents.append(a)

    # Check whether this is a root state with no parents
    def is_root(self):
        return self.num_parents() == 0

    # Check whether this is a leaf state with no parents
    def is_leaf(self):
        return self.num_children() == 0

    # Get the name of the node
    def get_name(self):
        return self.name

    # Return the number of children of this node
    def num_children(self):
        return len(self.children)

    # Return the possible states of the node
    def get_states(self):
        return self.states

    # Return the number of states this node has
    def num_states(self):
        return self.numStates

    # Return the number of parents of this node
    def num_parents(self):
        return len(self.parents)

    # Return the parents of the node
    def get_parents(self):
        return self.parents

    # Return the children of the node
    def get_children(self):
        return self.children

    # Set the Probability Distribution of this node
    def set_dist(self, distribution):
        self.dist = distribution
        # If this is a root value, set the distribution to be the marginal
        if self.is_root():
            self.marginal = {}
            for key, value in distribution.items():
                i = 0
                while i < len(value):
                    self.marginal[(key[i],)] = value[i]
                    i += 1

    # Return the probability distribution of thise node
    def get_dist(self):
        return self.dist

    # receive the information from a factor based on new information.
    # Organize this information where it belongs in the information vector
    def receive_marginal(self, message, factor):
        if not self.information:
            self.information = [0] * (self.num_children() + (not self.is_root()))
        # If this node is the child in the CPD for the factor, set the information index to 0.
        if factor.getIndex(self.get_name()) == 0:
            self.information[0] = message
        else:
            child_name = factor.getFields()[0].get_name()
            i = 0
            while i < len(self.children):
                if child_name == self.children[i].get_name():
                    break
                i += 1
            self.information[i + (not self.is_root())] = message

    def update_marginal(self):
        if self.is_root():
            pass
        else:
            thesum = 0
            vals = {(state,): 1 for state in self.states}
            # For each factor we receive information from
            for a in self.information:
                # For this evidence in the message
                for ev in a.keys():
                    vals[ev] = vals[ev] * a[ev]

            for val in vals.values():
                thesum += val

            for key in vals.keys():
                if thesum != 0:
                    vals[key] = vals[key] / thesum
            self.marginal = vals

    # Return marginal distribution of node variable in node
    def get_marginal(self):
        return self.marginal

    def send_marginal(self, target_factor):
        index = -1
        cache_query = target_factor.getFields()[0].get_name()
        if self.is_root():
            return self.marginal

        if cache_query == self.name:
            index = 0
        else:
            j = 0
            while j < len(self.children):
                if cache_query == self.get_children()[j].get_name():
                    index = j + (not self.is_root())
                j += 1
        the_sum = 0
        vals = {(state,): 1 for state in self.states}
        i = 0
        while i < len(self.information):
            if i != index:
                for ev in self.information[i].keys():
                    vals[ev] = vals[ev] * self.information[i][ev]
            i += 1
        for val in vals.values():
            the_sum += val

        for key in vals.keys():
            vals[key] = vals[key] / the_sum
        return vals

    # Print the characteristics of this node
    def print_node(self):
        print(self.get_name())
        print("Parents: ")
        for b in self.parents:
            print(b.get_name())
            print("CPD: ")
            pprint(self.get_dist())
            print("Children: ")
            for c in b.children:
                print(c.get_name())
                print("")

    def __repr__(self) -> str:
        return self.name

