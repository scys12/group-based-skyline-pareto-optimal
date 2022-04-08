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
