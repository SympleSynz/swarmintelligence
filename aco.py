class ACO:
    def __init__(self, prob, alpha=0.5, beta=0.5):
        """
        Args:
            prob: An object for which isinstance(prob, problem.Problem) holds
            alpha: Pheromone exponent for the transition probabilities
            beta: Heuristic exponent for the transition probabilities
        """
        self.prob = prob
        self.alpha = alpha
        self.beta = beta
