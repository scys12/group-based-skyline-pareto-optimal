from skyline import Skyline


class SkylineLayer:
    def __init__(self, points):
        self.points = []
        for p in points:
            self.points.append(Skyline(p))
        self.points[0].layer = 1
        self.tail_points = [self.points[0]]
        self.layers = {
            1: [self.points[0].point]
        }
        self.max_layer = 1

    def processing(self):

        for i in range(1, len(self.points)):
            if not self.tail_points[0].dominate(self.points[i]):
                self.points[i].layer = 1
                self.tail_points[0] = self.points[i]
                self.layers[self.points[i].layer].append(
                    self.points[i].point)
            elif self.tail_points[self.max_layer-1].dominate(self.points[i]):
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
