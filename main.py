import argparse
import random
import pandas as pd
from BIFParser import fix_white_space, parse_bif, print_nodes
from Probability import Probability
from Utils import process_arguments, get_value_var, is_in_prob_list

parser = argparse.ArgumentParser(description='Estimate a probability.')
parser.add_argument('-t', '--target', metavar='xi')
parser.add_argument('-u', '--universe', nargs='+')
args = parser.parse_args()

f = open("alarm.bif", "r")
BIF = f.readlines()
BIF = fix_white_space(BIF)
nodes = parse_bif(BIF)
print_nodes(nodes)
t, u = process_arguments(args, nodes)

v = {}
for n in nodes:
    v[n] = get_value_var(n, t, u)


def initialize_variables():
    lst = []
    for nod in nodes:
        p = Probability([(nod, v[nod])], [(p, v[p]) for p in nod.parents])
        lst.insert(0, p)
    return lst


def estimate(xi, all_probs):
    pos_prob = []
    for p in all_probs:
        if xi in p:
            pos_prob.extend([p])
    neg_prob = [p.negate(xi) for p in pos_prob]
    res = Probability.get_prob_list_value(pos_prob) / (
            Probability.get_prob_list_value(pos_prob) + Probability.get_prob_list_value(neg_prob))
    return res


prob_lst = initialize_variables()
cols = [n.name for n in nodes]
df = pd.DataFrame(columns=cols)
i = 0
prev_prob = 0

while len(df) < 20000:
    for xi in nodes:
        probability = estimate(xi, prob_lst)
        if not is_in_prob_list(xi, u):
            r = random.uniform(0, 1)
            if r > probability:
                v[xi] = not (v[xi])
    prob_lst = initialize_variables()
    i += 1
    if i > 1000:
        df.loc[len(df)] = list(v.values())
    if i % 5000 == 0:
        curr_prob = len(df[df[t[0].name]]) / len(df)
        if (abs(curr_prob) - prev_prob) <= 0.001:
            break
        prev_prob = curr_prob

print(df)
print(len(df[df[t[0].name]]) / len(df))
