from abc import ABC, abstractmethod

from problems.abstract_problem import AbstractProblem


class AbstractStrategy(ABC):

    def __init__(self, problem: AbstractProblem):
        self.problem = problem

    @abstractmethod
    def find_solution(self):
        pass

    @abstractmethod
    def get_solution(self):
        # return "Initial State:" + str(self.problem.create_initial_state())
        return "Initial State:" + str(self.problem.create_initial_state())

    def print_resource_usage_report(self):
        pass
