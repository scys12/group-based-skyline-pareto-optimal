from itertools import chain, combinations
import sys
from timeit import default_timer as timer
from math import comb


class KeyWrapper:
    def __init__(self, iterable, key):
        self.it = iterable
        self.key = key

    def __getitem__(self, i):
        return self.key[self.it[i]]

    def __len__(self):
        return len(self.it)


def create_subset(group, start, subset_length):
    if subset_length > len(group):
        subset_length = len(group)
    if start < 0:
        return combinations(group, subset_length)
    return list(
        chain.from_iterable(
            combinations(group, r) for r in range(start, len(group) + 1)
        )
    )


def reverse_bisort(a, x, lo=0, hi=None):
    if lo < 0:
        raise ValueError("lo must be non-negative")
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if x > a[mid]:
            hi = mid
        else:
            lo = mid + 1
    return lo


class RepresentativeSkylineGraph:
    def __init__(self, dsg, group):
        self.graph = {}
        self.merge_child_in_graph(dsg, group)

    def merge_child_in_graph(self, dsg, group):
        for parent_point in group:
            children_set = [parent_point] + dsg[parent_point]["children"]
            for child_point in list(children_set):
                if (
                    self.check_point_have_one_parent_in_group(dsg, group, child_point)
                    and child_point not in group
                ):
                    self.graph[parent_point]["weight"] += 1
                    children_set.remove(child_point)
                else:
                    if child_point not in self.graph:
                        self.graph[child_point] = {"weight": 1, "children_set": []}
            self.graph[parent_point]["children_set"].append(children_set)

    def check_point_have_one_parent_in_group(self, dsg, group, point):
        parents = dsg[point]["parents"]
        parent_points = set(group).intersection(set(parents))
        return len(parent_points) == 1


class MaximumBipartiteMatchingGraph:
    def __init__(self, group_types, group):
        self.group_types = group_types
        self.group = group
        self.matrix = [[] for _ in range(len(self.group_types) + 1)]

        self.pairV = [0] * (len(self.group_types) + 1)
        self.pairU = [0] * (len(self.group) + 1)
        self.dist = [-1] * (len(self.group_types) + 1)

        self.assign_group(self.group_types, self.group)

    def assign_group(self, group_types, group):
        for idx_gt in range(len(group_types)):
            for g in group_types[idx_gt]:
                idx_grp = group.index(g)
                self.matrix[idx_gt + 1].append(idx_grp + 1)

    def max_matching(self):
        result = 0
        while self.bfs():
            for u in range(1, len(self.group_types) + 1):
                if self.pairU[u] == 0 and self.dfs(u):
                    result += 1
        return result

    def dfs(self, u):
        if u != 0:
            for v in self.matrix[u]:
                if self.dist[self.pairV[v]] == self.dist[u] + 1:
                    if self.dfs(self.pairV[v]):
                        self.pairV[v] = u
                        self.pairU[u] = v
                        return True
            self.dist[u] = sys.maxsize
            return False
        return True

    def bfs(self):
        queue = []
        for u in range(1, len(self.group_types) + 1):
            if self.pairU[u] == 0:
                self.dist[u] = 0
                queue.append(u)
            else:
                self.dist[u] = sys.maxsize

        self.dist[0] = sys.maxsize

        while len(queue) != 0:
            u = queue.pop()
            if self.dist[u] < self.dist[0]:
                for v in self.matrix[u]:
                    if self.dist[self.pairV[v]] == sys.maxsize:
                        self.dist[self.pairV[v]] = self.dist[u] + 1
                        queue.append(self.pairV[v])

        return self.dist[0] != sys.maxsize


def get_top_points_by_approximate(points, group_size, k):
    total_points = len(points)
    LIMIT = 100000000
    while comb(total_points, group_size) > LIMIT and k < LIMIT:
        if comb(total_points - 1, group_size) < k:
            break
        total_points -= 1
    return points[:total_points]


def benchmark_time(func, *args):
    start = timer()
    result = func(*args)
    end = timer()
    return result, end - start
