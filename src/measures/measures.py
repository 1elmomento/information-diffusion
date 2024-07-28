import random
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("QtAgg")


class Measures:
    def __init__(self) -> None:
        self.nodes = list(range(1, 35))
        self.edges = [
            (12, 5),
            (12, 27),
            (12, 9),
            (12, 33),
            (12, 1),
            (12, 18),
            (12, 21),
            (12, 14),
            (12, 30),
            (12, 3),
            (12, 22),
            (12, 7),
            (12, 25),
            (12, 34),
            (12, 2),
            (12, 19),
            (12, 11),
            (12, 29),
            (12, 6),
            (12, 15),
            (12, 20),
            (12, 4),
            (12, 13),
            (12, 32),
            (12, 8),
            (23, 28),
            (12, 10),
            (5, 27),
            (5, 9),
            (5, 33),
            (5, 1),
            (5, 21),
            (5, 14),
            (5, 30),
            (5, 3),
            (5, 22),
            (5, 7),
            (5, 25),
            (5, 34),
            (5, 29),
            (5, 6),
            (5, 15),
            (5, 4),
            (5, 13),
            (5, 31),
            (5, 24),
            (5, 17),
            (5, 26),
            (27, 9),
            (27, 33),
            (27, 1),
            (27, 34),
            (27, 29),
            (27, 6),
            (27, 4),
            (27, 13),
            (27, 23),
            (9, 33),
            (9, 1),
            (9, 30),
            (9, 34),
            (9, 6),
            (9, 4),
            (9, 24),
            (9, 23),
            (33, 1),
            (33, 34),
            (33, 6),
            (33, 23),
            (1, 30),
            (1, 3),
            (1, 34),
            (1, 29),
            (1, 6),
            (1, 4),
            (1, 24),
            (21, 14),
            (21, 25),
            (21, 29),
            (21, 13),
            (14, 29),
            (14, 25),
            (14, 13),
            (30, 34),
            (30, 6),
            (30, 4),
            (30, 31),
            (30, 17),
            (3, 34),
            (3, 29),
            (3, 6),
            (3, 31),
            (3, 17),
            (25, 29),
            (25, 28),
            (25, 10),
            (25, 16),
            (34, 6),
            (34, 15),
            (34, 4),
            (34, 31),
            (34, 17),
            (19, 11),
            (29, 6),
            (29, 15),
            (29, 20),
            (29, 13),
            (29, 28),
            (29, 26),
            (6, 15),
            (6, 4),
            (6, 31),
            (6, 24),
            (6, 17),
            (4, 31),
            (4, 17),
            (32, 8),
            (16, 28),
            (28, 31),
        ]
        self.graph = nx.Graph()

    def create_network(self) -> None:
        self.graph.add_nodes_from(self.nodes)
        self.graph.add_edges_from(self.edges)

        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(self.graph, k=0.8, iterations=200)
        nx.draw(
            self.graph,
            pos=pos,
            with_labels=True,
            font_size=10,
            node_size=700,
            edge_color="gray",
            node_color="#93BFCF",
        )
        plt.savefig("plots/network.png", dpi=400)
        plt.close("all")

    def independent_cascade_model(self, seed_set, prob):
        active = set(seed_set)
        new_active = set(seed_set)

        while new_active:
            current_new_active = set()
            for node in new_active:
                for neighbor in self.graph.neighbors(node):
                    if neighbor not in active and neighbor not in current_new_active:
                        if random.random() < prob:
                            current_new_active.add(neighbor)
            new_active = current_new_active
            active.update(new_active)

        return active

    def run(self, seed_set, prob):
        self.create_network()
        spread = self.independent_cascade_model(seed_set=seed_set, prob=prob)
        return spread
