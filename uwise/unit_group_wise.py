from memory_profiler import profile


class GSkylineGroup:
    class SETreeNode:
        def __init__(self, ug, points, parent_set, point_index=-1):
            self.parent_set = parent_set
            self.point_index = point_index
            self.tail_sets = list()
            self.unit_groups = ug
            self.points = points

        def get_tail_sets(self, dsg_keys):
            for i in range(self.point_index-1, -1, -1):
                yield dsg_keys[i]
        
        def get_tail_set_points(self, dsg_keys, unit_groups):
            tail_set_points = set()
            for i in range(self.point_index, -1, -1):
                tail_set_points.update(unit_groups[dsg_keys[i]])
            return tail_set_points

        def __str__(self):
            return str({
                'points': self.points,
                'point_index': self.point_index,
                'unit_groups': self.unit_groups,
                'tail_sets': self.tail_sets
            })

    def __init__(self, dsg, group_size):
        self.dsg = dsg
        self.group_size = group_size
        self.unit_group = {}
        self.skyline_groups = []
        self.create_unit_group(self.dsg)
        self.dsg_keys = list(dsg)

    def create_unit_group(self, dsg):
        removed_dsg = 0
        for point_key in list(dsg):
            unit_group_points = set()
            unit_group_points.update(dsg[point_key].parents)
            unit_group_points.add(point_key)
            dsg[point_key].point_index -= removed_dsg
            if len(unit_group_points) >= self.group_size:
                if len(unit_group_points) == self.group_size:
                    self.skyline_groups.append(unit_group_points)
                del dsg[point_key]
                removed_dsg += 1
            else:
                self.unit_group[point_key] = unit_group_points

    def get_first_unit_groups(self, dsg, unit_group):
        for point_key in reversed(dsg):
            group = self.SETreeNode([point_key], unit_group[point_key], set(), dsg[point_key].point_index)
            yield group

    def processing(self):
        
        for group in self.get_first_unit_groups(self.dsg, self.unit_group):
            tail_set_points = group.get_tail_set_points(self.dsg_keys, self.unit_group)
            if len(tail_set_points) <= self.group_size:
                if len(tail_set_points) == self.group_size:
                    yield tail_set_points
                break
            temp_groups = [group]
            i = 2
            while len(temp_groups) > 0 and i <= self.group_size:
                candidate_groups = []
                for candidate_group in temp_groups:
                    parent_set = set(self.dsg[candidate_group.unit_groups[-1]].parents)
                    parent_set.update(candidate_group.parent_set)
                    for ug in candidate_group.get_tail_sets(self.dsg_keys):
                        if ug in parent_set:
                            continue                        
                        new_points = candidate_group.points.copy()
                        new_points.update(self.unit_group[ug])
                        if len(new_points) == self.group_size:
                                yield new_points
                        elif len(new_points) < self.group_size:
                                new_ug = candidate_group.unit_groups + [ug]
                                g = self.SETreeNode(new_ug, new_points, parent_set, self.dsg[ug].point_index)
                                candidate_groups.append(g)
                temp_groups = candidate_groups
                i += 1
