from itertools import chain, combinations


class KeyWrapper:
    def __init__(self, iterable, key):
        self.it = iterable
        self.key = key

    def __getitem__(self, i):
        return self.key[self.it[i]]

    def __len__(self):
        return len(self.it)


def create_subset(list, subset_length):
    return [x for x in combinations(list, subset_length)]


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
