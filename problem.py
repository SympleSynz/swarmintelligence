import abc

"""
Generic problem to be subclassed for ACO instances
"""


class Problem(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def components(self):
        """
        Return a set of all possible decision variables
        Returns:
            A set of all solution components.
        """
        ...

    @abc.abstractmethod
    def build(self):
        """
        Build up a solution. This is the bulk of the problem representation since it encodes any constraints.
        Returns:
            A generator which yields a list of (component, heuristic value) tuples, corresponding to valid solution compoenents.
            Receives solution compoenents to add via send().
        Raises:
            StopIteration when no solution components are viable.
        """
        ...

    @abc.abstractmethod
    def score(self, sol):
        """
        Score the solution
        Args:
            sol: A list of variables that represent the solution.
        Returns:
            A non-negative score.
        Raises:
            ValueError if the solution is not valid.
        """
        ...
