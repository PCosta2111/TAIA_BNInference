#!/usr/bin/env python

"""
This is a script that parses a BIF (Bayesian Implementation Format) file passed by the command line.
"""
# ==========================================================================
# =               THIS CODE BELONGS TO @atcbosselut GitHub.com             =
# =   https://github.com/atcbosselut/bif-parser/blob/master/BIFParser.py   =
# ==========================================================================


from __future__ import division

import re
from pprint import pprint

import Node

__author__ = "Antoine Bosselut"
__version__ = "1.0.2"
__maintainer__ = "Antoine Bosselut"
__email__ = "antoine.bosselut@uw.edu"
__status__ = "Prototype"


def fix_white_space(bif_white):
    i = 0
    while i < len(bif_white):
        if bif_white[i] == "\n":  # or a[i] == "}\n":
            # Remove whitespace lines
            del bif_white[i]
        else:
            # Add a space after every piece of punctuation. This will make all distinct words separated only by punctuation
            # distinct entries in the list of values when we split a line
            bif_white[i] = re.sub('([,])', r'\1 ', bif_white[i])

            # Get rid of white space at the beginning and end
            bif_white[i] = bif_white[i].strip()
            i += 1
    # print BIF_white
    return bif_white


def parse_bif(bif):
    i = 0
    nodes = []
    while i < len(bif):
        line_list = bif[i].split()
        # If this line is a variable declaration
        if line_list[0] == 'variable':
            name = line_list[1]
            i = i + 1
            # While the end of the declaration is not parsed
            while bif[i] != '}':
                line_list = bif[i].split()
                if line_list[0] == 'type':
                    # Parse the variable type - will be discrete in most cases
                    the_type = line_list[1]

                    # Parse the number of states
                    num_states = int(line_list[3])

                    # Remove commas from the names of possible states for this variable
                    line_list[6:6 + num_states] = [x.strip(",") for x in
                                                   line_list[6:6 + num_states]]

                    # Set a tuple containing the states
                    the_states = tuple(line_list[6:6 + num_states])

                    # Set property to be null string
                    the_property = ""
                elif line_list[0] == 'property':
                    # If there is a property, record it
                    the_property = " ".join(line_list[1:])
                i += 1
            # Append the new node to the list of nodes
            # THIS IS WHERE YOU MUST CHANGE THE INSTANTIATION OF A NODE IF YOU CHANGE THE CONSTRUCTOR IN THE NODE CLASS
            nodes.append(Node.Node(name, the_type, num_states, the_states, the_property))
        elif line_list[0] == 'probability':
            # If this is declaration is a probability distribution

            # Add spaces before and after parentheses
            bif[i] = re.sub('([()])', r' \1 ', bif[i])

            line_list = bif[i].split()

            # Find the query variable
            for theNode in nodes:
                if theNode.get_name() == line_list[2]:
                    temp = theNode
                    break

            # Add parents to the query variables if there are any
            if line_list[3] == '|':
                j = 4
                while line_list[j] != ')':
                    for parent in nodes:
                        # Find the parents in the list of nodes
                        if parent.get_name() == line_list[j].strip(","):
                            temp.add_parent([parent])
                            parent.add_children([temp])
                            break;
                    j += 1
            i += 1
            the_cpd = {}
            # While the end of the declaration is not parsed
            while bif[i] != '}':
                line_list = bif[i].split()

                if line_list[0] == 'table':
                    # Get rid of the identifier
                    del line_list[0]

                    # Get rid of commas and semicolons
                    prob = [x.translate({ord(','): None, ord(';'): None}) for x in line_list]

                    # Store the distribution (this is a marginal distribution)
                    the_cpd[temp.get_states()] = tuple([float(h) for h in prob])

                elif line_list[0][0] == "(":
                    # Remove all punctuation from the evidence names and the probability values
                    line_list = [states.translate(
                        {ord(','): None, ord(';'): None, ord('('): None, ord(')'): None}) for states
                        in line_list]

                    # In the CPD dictionary key, the states of the node are stored first. The
                    # second tuple is that of the parent values
                    the_cpd[(temp.get_states(), tuple(line_list[:temp.num_parents()]))] = tuple(
                        [float(h) for h in line_list[temp.num_parents():]])
                i += 1
            # print the_cpd
            temp.set_dist(the_cpd)
        else:
            i = i + 1
    return nodes


def print_nodes(nodes):
    for a in nodes:
        print(a.get_name())
        print("Parents: ")
        for b in a.parents:
            print(b.get_name())
        print("CPD: ")
        pprint(a.get_dist())
        print("Children: ")
        for c in a.children:
            print(c.get_name())
        print("")


'''def printFactors(factors):
    for a in factors:
        print a.get'''
