import networkx as nx
import pickle
from pprint import pprint


class DependencyPathDistanceGetter:
    def __init__(self):
        with open(
            "D:\Kuliah/TA/data/spacy_dependency_parsing_result.pickle", "rb"
        ) as inp:
            self.edges_list = pickle.load(inp)

        print("Dependency Path Distance Getter instantiated...")

    def get_distance_value(self, source, source_idx, target, target_idx, sentence_idx):
        """
        Parameters: source token, source token index, target token, target token index, sentence index
        """

        graph = nx.Graph(self.edges_list[sentence_idx])

        source += "-" + str(source_idx)
        target += "-" + str(target_idx)

        try:
            return nx.shortest_path_length(graph, source=source, target=target)
        except nx.exception.NetworkXNoPath:
            return 1
        except nx.exception.NodeNotFound:
            return 1


if __name__ == "__main__":
    getter = DependencyPathDistanceGetter()

    # print(getter.get_distance_value("amazing", 3, "service", 4, 100))
    pprint(getter.edges_list[241])
