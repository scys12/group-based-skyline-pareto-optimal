from skyline import Skyline


class DirectedSkylineGraph:
    def __init__(self, layers, max_layer):
        self.graph = {}
        self.layers = layers
        self.max_layer = max_layer
        self.current_point_index = 0

        for i in range(len(self.layers[1])):
            key = tuple(self.layers[1][i])
            self.graph[key] = self.initialize_graph_value(1, self.current_point_index)
            self.current_point_index += 1

    def initialize_graph_value(self, layer_index, point_index):
        return {
            "layer_index": layer_index,
            "point_index": point_index,
            "parents": [],
            "children": [],
        }

    def processing(self):
        for i in range(2, self.max_layer + 1):
            for j in range(len(self.layers[i])):
                dsg = self.initialize_graph_value(i, self.current_point_index)
                self.current_point_index += 1
                for k in range(i - 1, 0, -1):
                    for l in range(len(self.layers[k])):
                        sp1 = Skyline(self.layers[k][l])
                        sp2 = Skyline(self.layers[i][j])
                        if sp1.dominate(sp2):
                            dsg["parents"].append(self.layers[k][l])
                            key = tuple(self.layers[k][l])
                            self.graph[key]["children"].append(self.layers[i][j])
                key = tuple(self.layers[i][j])
                self.graph[key] = dsg
