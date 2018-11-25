import time
from collections import namedtuple
from functools import partial
from queue import LifoQueue

from problems.abstract_problem import AbstractProblem
from strategies.abstract_strategy import AbstractStrategy

Node = namedtuple('Node', 'parent_node, depth, state, action')


class IterativeDepthFirstSearch(AbstractStrategy):
    root = None
    goal_node = None

    def find_solution(self):
        self.start_time = time.monotonic()

        depth_limit = 0

        solution_found = False
        while not solution_found:
            depth_limit += 1
            solution_found = self.iddfs(depth_limit)

        self.stop_time = time.monotonic()

    def iddfs(self, depth_limit: int):
        # build and traverse tree
        self.root = Node(
            parent_node=None,
            depth=1,
            state=self.problem.create_initial_state(),
            action="",
        )
        lifo_queue = LifoQueue()
        lifo_queue.put(self.root)

        while not lifo_queue.empty():
            # examine the next node
            this_node = lifo_queue.get()
            # is this node the goal?
            if self.problem.is_goal_state(this_node.state):
                self.goal_node = this_node
                return (True, depth_limit, self.get_solution())
            # don't add child nodes if max depth is reached
            if this_node.depth >= depth_limit:
                continue
            # add child nodes for each possible action
            for action in self.problem.get_actions():
                child_node = Node(
                    parent_node=this_node,
                    depth=this_node.depth + 1,
                    state=partial(action, this_node.state)(),
                    action=action,
                )
                lifo_queue.put(child_node)
        return (False, depth_limit, None)

    def get_solution(self):
        solution = super().get_solution() + '\n'
        # backtrace from goal_node to root
        path = []
        node = self.goal_node
        while node != self.root:
            path.append(node)
            node = node[0]
        path.reverse()

        for node in path:
            solution += "Action: {:50} State: {}".format(
                str(node.action), str(node.state))

        return solution

    def print_resource_usage_report(self):
        print("Time taken: {:.3f} seconds".format(
            self.stop_time - self.start_time))
