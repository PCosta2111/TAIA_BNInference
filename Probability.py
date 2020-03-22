class Probability:

    def __init__(self, target, universe) -> None:
        self.target = target
        self.universe = universe

    def __contains__(self, variable):
        if variable.name == self.target[0][0].name:
            return True
        for (n, _) in self.universe:
            if n.name == variable.name:
                return True

    def __str__(self) -> str:
        s = 'Pr( '
        for (xi, n) in self.target:
            if n:
                s = s + xi.name + ', '
            else:
                s = s + ' not ' + xi.name + ', '
        if not self.universe:
            return s[:-2] + ' )'
        s = s[:-2] + ' | '
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
        x = []
        for (xi, i) in self.target:
            if xi.name == v.name:
                x.extend([(xi, not i)])
            else:
                x.extend([(xi, i)])
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
            res = res * prob[0][0].get_dist()[key][int(not (prob[0][1]))]
        return res

    @staticmethod
    def get_key(p):
        if not p.target[0][0].parents:
            return 'True', 'False'
        u = []
        for (xi, i) in p.universe:
            u.append(str(bool(i)))
        return ('True', 'False'), tuple(u)

    @staticmethod
    def estimate(prob, nodes):
        pos_prob = []
        for p in all_probs:
            if prob.target[0][0] in p:
                pos_prob.extend([p])
        neg_prob = [p.negate(prob.target[0][0]) for p in pos_prob]
        res = Probability.get_prob_list_value(pos_prob) / (
                Probability.get_prob_list_value(pos_prob) + Probability.get_prob_list_value(neg_prob))
        print(pos_prob)
        print("--------------------------------------------- = " + str(res))
        print(str(pos_prob) + ' + ' + str(neg_prob))
        print("")
        return xi