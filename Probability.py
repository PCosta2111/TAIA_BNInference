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
        if self.target[1]:
            s = s + self.target[0].name + ' '
        else:
            s = s + ' not ' + self.target[0].name + ' '
        if not self.universe:
            return s + ' )'
        s = s + ' | '
        for (xi, n) in self.universe:
            if n:
                s = s + xi.name + ', '
            else:
                s = s + ' not ' + xi.name + ', '
        s = s[:-2] + ' )'
        return s

    def __repr__(self):
        return self.__str__()

    def negate(self, v):
        if self.target[0].name == v.name:
            x = (self.target[0], not self.target[1])
        else:
            x = self.target
        u = []
        for (xi, i) in self.universe:
            if xi.name == v.name:
                u.extend([(xi, not i)])
            else:
                u.extend([(xi, i)])
        return Probability(x, u)

    @staticmethod
    def get_prob_list_value(prob_list):
        res = 1
        for p in prob_list:
            prob = p.target
            key = Probability.get_key(p)
            res = res * prob[0].get_dist()[key][int(not (prob[1]))]
        return res

    @staticmethod
    def get_key(p):
        if not p.target[0].parents:
            return 'True', 'False'
        u = []
        for (xi, i) in p.universe:
            u.append(str(bool(i)))
        return ('True', 'False'), tuple(u)
