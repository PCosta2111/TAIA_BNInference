class Probability:

    def __init__(self, target, universe) -> None:
        self.target = target
        self.universe = universe

    def __contains__(self, variable):
        if variable.name == self.target[0].name:
            return True
        for (n, _) in self.universe:
            if n.name == variable.name:
                return True

    def __str__(self) -> str:
        s = 'Pr( '
        s = s + self.target[0].name + '=' + str(self.target[1])
        if not self.universe:
            return s + ' )'
        s = s + ' | '
        for (xi, n) in self.universe:
            s = s + xi.name + '=' + str(n) + ", "
        s = s[:-2] + ' )'
        return s

    def __repr__(self):
        return self.__str__()

    def get_all_probabilities(self, v, nodes):
        values = self.get_var_values(nodes, v)
        probs = []
        for value in values:
            if self.target[0].name == v[0].name:
                x = (self.target[0], value)
            else:
                x = self.target
            u = []
            for (xi, i) in self.universe:
                if xi.name == v[0].name:
                    u.extend([(xi, value)])
                else:
                    u.extend([(xi, i)])
            probs.append(Probability(x, u))
        return probs

    def get_var_values(self, nodes, v):
        if len(v[0].parents) == 0:
            d = v[0].get_dist()
            k = list(d.keys())[0]
            return list(filter(lambda a: a != v[1], k))
        else:
            d = v[0].get_dist()
            k = list(d.keys())[0][0]
            return list(filter(lambda a: a != v[1], k))

    @staticmethod
    def get_prob_list_value(prob_list):
        res = 1
        for p in prob_list:
            prob = p.target
            if len(prob[0].parents) == 0:
                d = prob[0].get_dist()
                k = list(d.keys())[0]
                p_pos = k.index(prob[1])
                res = res * d[k][p_pos]
            else:
                n_k = tuple(v for (_, v) in p.universe)
                d = prob[0].get_dist()
                my_ps = list(d.keys())[0][0]
                p_pos = my_ps.index(prob[1])
                k = tuple([my_ps, n_k])
                v = d[k][p_pos]
                res = res * v
        return res

    @staticmethod
    def get_key(p):
        if not p.target[0].parents:
            return 'True', 'False'
        u = []
        for (xi, i) in p.universe:
            u.append(str(bool(i)))
        return ('True', 'False'), tuple(u)

