from GraphSearch.PriorityQueue import PriorityQueue
from GraphSearch import utility
import math
from copy import copy


def breadth_first_search(graph, start, goal):
    if start == goal:
        return []
    frontier = [(start, [])]
    cnt = 1
    while len(frontier) > 0:
        cnt += 1
        current, path = frontier[0]
        frontier = frontier[1:]
        temp_path = copy(path)
        temp_path.append(current)
        if current == goal:
            return temp_path
        for neighbor in graph[current]:
            if neighbor == goal:
                temp_path.append(neighbor)
                return temp_path

            if neighbor not in graph.get_explored_nodes() and not in_frontier(neighbor, frontier):
                frontier.append((neighbor, temp_path))

    return temp_path


def in_frontier(v, frontier):
    for node in frontier:
        if v == node:
            return True
    return False


def uniform_cost_search(graph, start, goal):
    if start == goal:
        return []
    frontier = PriorityQueue()
    frontier.append((0, (start, [])))
    cnt = 1
    while frontier.has_next():
        cnt += 1
        cost, node = frontier.pop()
        current, path = node
        temp_path = copy(path)
        temp_path.append(current)
        if current == goal:
            return temp_path

        for neighbor in graph[current]:

            if neighbor not in graph.get_explored_nodes() and not frontier.__contains__(neighbor):
                n_weight = get_weight(graph, neighbor, current)
                n_weight += cost
                frontier.append((n_weight, (neighbor, temp_path)))
    return None


def get_weight(g, neighbor, node):
    w = g[node][neighbor]['weight']
    return w


def euclidean_dist_heuristic(graph, v, goal):
    x1, y1 = graph.nodes[v]['pos']
    # print(x1, y1)
    x2, y2 = graph.nodes[goal]['pos']
    # print(x2, y2)
    y = y2-y1
    y = y**2
    x = x2-x1
    x = x**2
    edh = math.sqrt(y+x)
    # print(edh)
    return edh


def a_star(graph, start, goal, heuristic=euclidean_dist_heuristic):
    if start == goal:
        return []
    frontier = PriorityQueue()
    frontier.append((0, (start, [])))
    while frontier.has_next():
        cost, node = frontier.pop()
        current, path = node
        pos_edh = heuristic(graph, current, goal)
        cost -= pos_edh
        temp_path = copy(path)
        temp_path.append(current)
        if current == goal:
            return temp_path

        for neighbor in graph[current]:
            neg_edh = heuristic(graph, neighbor, goal)
            if neighbor not in graph.get_explored_nodes() and not frontier.__contains__(neighbor):
                n_weight = get_weight(graph, neighbor, current)
                n_weight += cost
                n_weight += neg_edh
                frontier.append((n_weight, (neighbor, temp_path)))
    return None
