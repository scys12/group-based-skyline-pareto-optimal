from skyline import Skyline


class SkylineLayer:
    def __init__(self, points, d, group_size):
        self.points = []
        self.d = d
        self.group_size = group_size
        for p in points:
            self.points.append(Skyline(p))
        self.points[0].layer = 1
        self.tail_points = [self.points[0]]
        if self.d <= 2:
            self.layers = {
                1: [self.points[0].point]
            }
        else:
            self.layers = {
                1: [self.points[0].point]
            }
            for i in range(2, self.group_size+1):
                self.layers[i] = []

        self.max_layer = 1

    def processing_two_dimensional_points(self):
        for i in range(1, len(self.points)):
            if not self.tail_points[0].dominate(self.points[i]):
                self.points[i].layer = 1
                self.tail_points[0] = self.points[i]
                self.layers[self.points[i].layer].append(
                    self.points[i].point)
            elif self.tail_points[self.max_layer-1].dominate(self.points[i]):
                if self.max_layer == self.group_size:
                    continue
                self.max_layer += 1
                self.points[i].layer = self.max_layer
                self.tail_points.append(self.points[i])
                self.layers[self.points[i].layer] = [self.points[i].point]
            else:
                current_layer = self.binary_search_layer(
                    self.tail_points, self.points[i], 1, self.max_layer-1)
                self.points[i].layer = current_layer
                self.tail_points[current_layer-1] = self.points[i]
                self.layers[self.points[i].layer].append(
                    self.points[i].point)

    def processing_higher_dimensional_points(self):
        for i in range(1, len(self.points)):
            cant_dominate = False
            for point in self.layers[1]:
                skpoint = Skyline(point)
                if skpoint.dominate(self.points[i]):
                    cant_dominate = True
                    break
            if not cant_dominate:
                self.points[i].layer = 1
                self.layers[self.points[i].layer].append(self.points[i].point)
                continue

            for j in range(2, len(self.layers)+1):
                flag = False
                for point in self.layers[j]:
                    skpoint = Skyline(point)
                    if skpoint.dominate(self.points[i]):
                        flag = True
                        break
                if not flag:
                    self.points[i].layer = j
                    self.layers[self.points[i].layer].append(
                        self.points[i].point)
                    self.max_layer = j if self.max_layer < j else self.max_layer
                    break
        for layer_idx in list(self.layers):
            if len(self.layers[layer_idx]) == 0:
                del self.layers[layer_idx]

    def processing(self):
        if self.d <= 2:
            self.processing_two_dimensional_points()
        else:
            self.processing_higher_dimensional_points()

    def binary_search_layer(self, tail_points, point, low, high):
        if high >= low:
            current_layer = low + (high - low)//2
            if not tail_points[current_layer].dominate(point):
                if tail_points[current_layer-1].dominate(point):
                    return current_layer + 1
                elif not tail_points[current_layer-1].dominate(point):
                    return self.binary_search_layer(tail_points, point, low, current_layer-1)
            else:
                return self.binary_search_layer(tail_points, point, current_layer + 1, high)
        else:
            return -1
