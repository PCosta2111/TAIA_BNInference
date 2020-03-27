import random
from pprint import pprint
import numpy as np


def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier


def process_arguments(args, nodes, encode_dict):
    t = None
    t_xi, t_val = args.target.split('=')
    for n in nodes:
        if n.name == t_xi:
            t = (n, encode_dict[t_val])
            break
    u = []
    if args.universe:
        for u_var in args.universe:
            u_xi, u_val = u_var.split('=')
            for n in nodes:
                if n.name == u_xi:
                    u.append((n, encode_dict[u_val]))
                    break
    return t, u


def is_in_prob_list(xi, prob_lst):
    for (n, v) in prob_lst:
        if n.name == xi.name:
            return n, v
    return None


def get_random_value(n, nodes):
    for nod in nodes:
        dist = n.get_dist()
        for key, _ in dist.items():
            if nod.name == n.name:
                if len(n.parents) == 0:
                    return random.choice(key)
                else:
                    return random.choice(key[0])


def get_value_var(n, target, universe, encode_dict, nodes):
    if n.name == target[0].name:
        return target[1]
    else:
        k = is_in_prob_list(n, universe)
        if k:
            return k[1]
    return get_random_value(n, nodes)


def encode_nodes(nodes):
    encode_dict = {}
    int_label = 0
    for n in nodes:
        dist = n.get_dist()
        new_dist = {}
        for key, prob in dist.items():
            new_key = []
            if len(n.parents) == 0:
                for val in key:
                    if val in encode_dict:
                        new_key.append(encode_dict[val])
                    else:
                        encode_dict[val] = int_label
                        new_key.append(encode_dict[val])
                        int_label += 1
            else:
                for t in key:
                    new_tuple = []
                    for val in t:
                        if val in encode_dict:
                            new_tuple.append(encode_dict[val])
                        elif val is not None:
                            encode_dict[val] = int_label
                            new_tuple.append(encode_dict[val])
                            int_label += 1
                    new_key.append(tuple(new_tuple))
            new_dist[tuple(new_key)] = prob
        n.set_dist(new_dist)
    return nodes, encode_dict


def get_new_vi_x(xi, v):
    key = val = None
    if not xi.parents:
        d = xi.get_dist()
        key, val = list(d.items())[0]
    else:
        parents_value = tuple([v[p] for p in xi.parents])
        for k, v in xi.get_dist().items():
            my_val, par_val = k[0], k[1]
            if par_val == parents_value:
                key = my_val
                val = v
                break
    prob_cumsum = np.cumsum(list(val))
    k = 0
    r = random.uniform(0, 1)
    if r < prob_cumsum[0]:
        return key[0]
    for p in prob_cumsum:
        if r > p:
            return key[k + 1]
        k += 1
    return key[k]

    #
