import abc

"""
Generic problem to be subclassed for ACO instances
"""


class Problem(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def available_moves(self):
        """
        Give the currently available moves. These may be any hashable objects.
        Returns:
            A set of moves.
        """
        ...

    @abc.abstractmethod
    def make_move(self, move):
        """
        Make a move, possibly updating the result of available_moves()
        Args:
            move: The move to make. This should be a move that was returned by available_moves.
        """
        ...

    @abc.abstractmethod
    def heuristic(self):
        """
        Returns:
            A non-negative value representing the estimated value of the current
            solution state.
        """
        ...

    @abc.abstractmethod
    def score(self):
        """
        Score the problem state. This should only be called when available_moves returns
        an empty set.
        Returns:
            A non-negative score.
        """
