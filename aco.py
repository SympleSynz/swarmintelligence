import itertools
from operator import itemgetter
import random


class ACO:
    def __init__(self, prob, alpha=0.5, beta=0.5, c=0.5, xi=0.5, rho=0.5, q0=0.5):
        """
        Args:
            prob: An object for which isinstance(prob, problem.Problem) holds
            alpha: Pheromone exponent for the transition probabilities
            beta: Heuristic exponent for the transition probabilities
            c: Initial pheromone value
            xi: Individual pheromone evaporation rate for ACS solution construction
            rho: Per iteration pheromone evaporation rate
            q0: Probability of selecting max for pseudorandom proportional selection
        """
        self.prob = prob
        self.alpha = alpha
        self.beta = beta
        self.c = c
        self.xi = xi
        self.rho = rho
        self.q0 = q0

        self.pheromones = {comp: c for comp in prob.components()}

        self.best = None
        self.best_score = -1

        self.sols_per_iter = 1

    def optimize(self, n_iters=0):
        for i in range(n_iters):
            sols = []
            while len(sols) < self.sols_per_iter:
                s = []
                builder = self.prob.build()
                comps = next(builder)
                while comps:
                    try:
                        new_comp = self._choose_comp(comps)
                        self._acs_evap(new_comp)
                        s.append(new_comp)
                        comps = builder.send(new_comp)
                    except StopIteration:
                        break
                try:
                    score = self.prob.score(s)
                except ValueError:
                    continue

                sols.append((s, score))

            iter_sol, iter_score = max(sols, key=itemgetter(1))

            if iter_score > self.best_score:
                self.best_score = iter_score
                self.best = iter_sol

            self._update_pheromones()

        return self.best, self.best_score

    def _acs_evap(self, comp):
        # TODO: Investigate replacing c with a different tau_0
        # This enforces tau_min = xi * c
        self.pheromones[comp] = (1-self.xi) * self.pheromones[comp] + self.xi * self.c

    def _update_pheromones(self):
        # BS Pheromone update with normalization (HCF)

        om_rho = 1 - self.rho
        for comp in self.best:
            self.pheromones[comp] = om_rho * self.pheromones[comp] + self.rho

    def _choose_comp(self, comps):
        weights = list((comp, self.pheromones[comp]**self.alpha * heuristic**self.beta) for comp, heuristic in comps)

        # Pseudo-random proportional update (ACS)
        if random.random() < self.q0:
            comp, weight = max(weights, key=itemgetter(1))
            return comp
        else:
            weights = list(itertools.accumulate(weights, lambda acc, t: (t[0], acc[1] + t[1])))
            _, total_weight = weights[-1]
            threshold = random.random() * total_weight
            return next(comp for comp, w in weights if w >= threshold)
