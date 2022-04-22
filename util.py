from itertools import chain, combinations


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
        return [x for x in combinations(group, subset_length)]
    return list(chain.from_iterable(combinations(group, r) for r in range(start, len(group)+1)))


def reverse_bisort(a, x, lo=0, hi=None):
    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        if x > a[mid]:
            hi = mid
        else:
            lo = mid+1
    return lo


class RepresentativeSkylineGraph:
    def __init__(self, dsg, group) -> None:
        self.dsg = dsg
        self.group = group
        self.graph = {}

        self.merge_child_in_graph(self.group)

    def merge_child_in_graph(self, group):
        for parent_point in group:
            children_set = [parent_point] + self.dsg[parent_point].children
            for child_point in list(children_set):
                if self.check_point_have_one_parent_in_group(self.group, child_point) and child_point not in self.group:
                    self.graph[parent_point]['weight'] += 1
                    children_set.remove(child_point)
                else:
                    if child_point not in self.graph:
                        self.graph[child_point] = {
                            'weight': 1,
                            'children_set': []
                        }
            self.graph[parent_point]['children_set'] += children_set

    def check_point_have_one_parent_in_group(self, group, point):
        parents = self.dsg[point].parents
        parent_points = set(group).intersection(set(parents))
        return len(parent_points) == 1


class BipartiteGraph:
    def __init__(self, group_types, group):
        # group types = aplicants
        # group = jobs
        self.group_types = group_types
        self.group = group
        self.matrix = [[0] * len(self.group)
                       for _ in range(len(self.group_types))]

        self.assign_group(self.group_types, self.group)

    def assign_group(self, group_types, group):
        for idx_gt in range(len(group_types)):
            for g in group_types[idx_gt]:
                idx_grp = group.index(g)
                self.matrix[idx_gt][idx_grp] = 1


class MaximumBipartiteMatching:
    def max_matching(self, graph):
        len_grp_types = len(graph.group_types)
        len_group = len(graph.group)
        assign = [-1] * len_group
        total_match = 0

        for gt in range(len_grp_types):
            visited = [False] * len_group
            if self.bipartite_match(graph, gt, visited, assign):
                total_match += 1
        return total_match

    def bipartite_match(self, graph, group_types, visited, assign):
        for i in range(len(graph.group)):
            if graph.matrix[group_types][i] == 1 and not visited[i]:
                visited[i] = True
                assigned = assign[i]
                if assigned < 0 or self.bipartite_match(graph, assigned, visited, assign):
                    assign[i] = group_types
                    return True
        return False
