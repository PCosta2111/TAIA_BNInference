import random


def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier


def process_arguments(args, nodes):
    t = None
    if 'not_' in args.target:
        t_value = False
    else:
        t_value = True
    t_name = args.target.replace('not_', '')
    for n in nodes:
        if n.name == t_name:
            t = (n, t_value)
            break
    u = []
    if args.universe:
        for u_var in args.universe:
            if 'not_' in u_var:
                u_value = False
            else:
                u_value = True
            u_name = u_var.replace('not_', '')
            for n in nodes:
                if n.name == u_name:
                    u.append((n, u_value))
                    break
    return t, u


def is_in_prob_list(xi, prob_lst):
    for (n, v) in prob_lst:
        if n.name == xi.name:
            return n, v
    return None


def get_value_var(n, target, universe):
    if n.name == target[0].name:
        return target[1]
    else:
        k = is_in_prob_list(n, universe)
        if k:
            return k[1]
    return bool(truncate(random.uniform(0, 2)))
