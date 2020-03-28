import argparse

import pandas as pd

from BIFParser import fix_white_space, parse_bif, print_nodes
from Probability import Probability
from Utils import process_arguments, get_value_var, encode_nodes, get_new_vi_x, is_in_prob_list

parser = argparse.ArgumentParser(description='Estimate a probability.')
parser.add_argument('-t', '--target', metavar='xi')
parser.add_argument('-u', '--universe', nargs='+')
parser.add_argument('-i', '--maxiter', metavar='20000', default=20000, type=int)
parser.add_argument('-c', '--converfactor', metavar='0.001', default=0.001, type=float)
parser.add_argument('-r', '--repeat', metavar='1', default=1, type=int)
parser.add_argument('-b', '--bnet', metavar='earthquake.bif', default="earthquake.bif")
args = parser.parse_args()

f = open(args.bnet, "r")
BIF = f.readlines()
BIF = fix_white_space(BIF)
nodes = parse_bif(BIF)
# print_nodes(nodes)
nodes, encode_dict = encode_nodes(nodes)
t, u = process_arguments(args, nodes, encode_dict)
print(t, u)


def initialize_variables():
    lst = []
    for nod in nodes:
        p = Probability((nod, v[nod]), [(p, v[p]) for p in nod.parents])
        lst.insert(0, p)
    return lst


def estimate(xi, all_probs):
    pos_prob = []
    for p in all_probs:
        if xi[0] in p:
            pos_prob.extend([p])
    prob_variations = [p.get_all_probabilities(xi, nodes) for p in pos_prob]
    prob_variations = [Probability.get_prob_list_value(lst) for lst in prob_variations]
    try:
        res = Probability.get_prob_list_value(pos_prob) / (
            Probability.get_prob_list_value(pos_prob) + sum(prob_variations))
    except ZeroDivisionError:
        return 0
    return res


for it in range(0, args.repeat):
    v = {}
    new_vi = {}
    for n in nodes:
        v[n] = get_value_var(n, t, u, encode_dict, nodes)
    prob_lst = initialize_variables()
    cols = [n.name for n in nodes]
    df = pd.DataFrame(columns=cols)
    i = 0
    prev_prob = 0

    print("Processing inference number : " + str(it))
    while len(df) < args.maxiter:
        for xi in nodes:
            probability = estimate((xi, v[xi]), prob_lst)
            if not is_in_prob_list(xi, u):
                new_vi[xi] = get_new_vi_x(xi, v)
            else:
                new_vi[xi] = v[xi]
        v = new_vi
        prob_lst = initialize_variables()
        i += 1
        if i > 1000:
            df.loc[len(df)] = list(v.values())
        if i % 5000 == 0:
            curr_prob = len(df[df[t[0].name] == t[1]]) / len(df)
            if (abs(curr_prob) - prev_prob) <= args.converfactor:
                print("   => Results appear to have converged after " + str(
                    len(df) + 1000) + " iterations. Result: " + str(len(df[df[t[0].name] == t[1]]) / len(df)))
                break
            prev_prob = curr_prob
    if len(df) >= args.maxiter:
        print("   => Maximum number of iterations reached. Result: " + str(len(df[df[t[0].name] == t[1]]) / len(df)))
