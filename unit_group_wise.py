class SETree:
    def __init__(self, ug, points, level, dsg, point_index=-1, unit_groups=None) -> None:
        self.unit_groups = ug
        self.points = set(points)
        self.level = level
        self.children = []
        self.tail_sets = []
        self.tail_set_points = set()
        self.point_index = point_index
        self.add_tail_sets(dsg, unit_groups)

    def add_tail_sets(self, dsg, unit_groups):
        dsg_keys = list(reversed(dsg))
        for point in dsg_keys:
            if dsg[point].point_index <= self.point_index:
                if unit_groups is not None:
                    self.tail_set_points.update(unit_groups[point])
                if dsg[point].point_index < self.point_index:
                    self.tail_sets.append(point)

    def __str__(self):
        return str({
            'points': self.points,
            'level': self.level,
            'point_index': self.point_index,
            'unit_groups': self.unit_groups
        })


class GSkylineGroup:
    def __init__(self, dsg, group_size) -> None:
        self.dsg = dsg
        self.group_size = group_size
        self.unit_group = {}
        self.skyline_groups = []
        self.temp_groups = []

    def create_unit_group(self):
        for point_key in list(self.dsg):
            unit_group = self.dsg[point_key].parents + \
                [point_key]
            if len(unit_group) >= self.group_size:
                if len(unit_group) == self.group_size:
                    sg = SETree([point_key], unit_group, self.group_size,
                                self.dsg, self.dsg[point_key].point_index)
                    self.temp_groups.append(sg)
                del self.dsg[point_key]
            else:
                self.unit_group[point_key] = unit_group

    def initialize_first_unit_groups(self):
        candidate_groups = []
        for point_key in reversed(self.dsg):
            group = SETree([point_key], self.unit_group[point_key], 1,
                           self.dsg, self.dsg[point_key].point_index, self.unit_group)
            candidate_groups.append(group)
        return candidate_groups

    def verificate_g_skyline_group(self, group):
        points = set()
        size = len(group)
        for point in group:
            points.update(self.unit_group[point])
        total = len({point for point in points})
        return total == size

    def processing(self):
        self.create_unit_group()
        root = SETree([], [], 0, self.dsg)
        first_level_groups = self.initialize_first_unit_groups()

        for group in first_level_groups:
            if len(group.tail_set_points) <= self.group_size:
                if len(group.tail_set_points) == self.group_size:
                    group.points = group.tail_set_points
                    self.temp_groups.append(group)
                break
            self.skyline_groups = [
                [root],
                [group]
            ]
            i = 2
            while len(self.skyline_groups[i-1]) > 0 and i <= self.group_size:
                for candidate_group in list(self.skyline_groups[i-1]):
                    parent_set = set()
                    for ug in candidate_group.unit_groups:
                        parent_set.update(self.dsg[ug].parents)
                    for ug in list(candidate_group.tail_sets):
                        if ug in parent_set:
                            candidate_group.tail_sets.remove(ug)
                    for ug in candidate_group.tail_sets:
                        new_ug = candidate_group.unit_groups.copy()
                        new_ug.append(ug)
                        new_points = candidate_group.points.copy()
                        new_points.update(self.unit_group[ug])
                        if len(new_ug) == i and len(new_points) <= self.group_size:
                            if len(self.skyline_groups) == i:
                                self.skyline_groups.append([])
                            g = SETree(new_ug, new_points, i, self.dsg,
                                       self.dsg[ug].point_index)
                            if len(new_points) == self.group_size:
                                self.temp_groups.append(g)
                            else:
                                self.skyline_groups[i].append(g)

                    self.skyline_groups[i-1].remove(candidate_group)
                i += 1
