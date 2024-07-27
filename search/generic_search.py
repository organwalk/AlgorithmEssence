from heapq import heappush, heappop
from typing import List, Generic, TypeVar, Optional

T = TypeVar('T')


class PriorityQueue(Generic[T]):
    def __init__(self) -> None:
        self._container: List[T] = []

    @property
    def empty(self) -> bool:
        return not self._container

    def push(self, item: T) -> None:
        heappush(self._container, item)

    def pop(self) -> T:
        return heappop(self._container)

    def __repr__(self) -> str:
        return repr(self._container)


class Node(Generic[T]):
    def __init__(self, state: T, parent: Optional['Node'], cost: float = 0.0, heuristic: float = 0.0) -> None:
        self.state: T = state
        self.parent: Optional[Node] = parent
        self.cost: float = cost
        self.heuristic: float = heuristic

    def __lt__(self, other: 'Node') -> bool:
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)


def node_to_path(node: Node[T]) -> List[T]:
    path: List[T] = [node.state]
    # work backwards from end to front
    while node.parent is not None:
        node = node.parent
        path.append(node.state)
    path.reverse()
    return path


def astar(initial, goal_test, successors, heuristic):
    frontier = PriorityQueue()  # 优先队列，出队时自动得到最小代价
    frontier.push(Node(initial, None, 0.0, heuristic(initial)))
    explored = {initial: 0.0}

    # 不断探索未访问区域
    while not frontier.empty:
        # 将最小代价节点设为行动节点
        current_node = frontier.pop()
        current_state = current_node.state
        # 如果行动节点即目标节点，则搜索结束
        if goal_test(current_state):
            return current_node
        # 否则继续探索邻近区域
        for child in successors(current_state):
            new_cost = current_node.cost + 1
            if child not in explored or explored[child] > new_cost:
                explored[child] = new_cost
                frontier.push(Node(child, current_node, new_cost, heuristic(child)))
    return None
