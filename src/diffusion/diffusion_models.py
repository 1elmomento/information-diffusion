import random
import numpy as np
import networkx as nx
from networkx.algorithms import approximation as approx
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("QtAgg")


class Models:
    """
    Class of Models of Informatin Diffusion

    This class contains models for information diffusion in the social network.

    Attributes
    ----------
    nodes : list[int]
        This is the list of numbered nodes of the network indication individuals.

    edges: list[tuple[int, int]]
        This is the list of all edges or connections between nodes of the network.

    graph: nx.Graph
        This is the Graph object created by the `networkx` package.

    active_nodes: set
        This is the set of nodes that are active in the process of information diffusion

    Methods
    -------
    create_network():
        Using defined nodes and edges in the parameters, this function creates a network and stores the file in `plots` folder.

    degree_centrality_icm(seeds):
        This methods models the spread of information in the network and uses standard definition of the ICM and stores the infected and uninfected nodes in `plots/icm` folder.

    """

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
        self.GREEN = "#20bf55"
        self.GRAY = "#ced4da"
        self.graph = nx.Graph()
        self.active_nodes = None

    def create_network(self) -> None:
        """
        Visualizes the graph by adding nodes and edges, and saves the visualization to a file.

        This function adds nodes and edges to the graph, generates a layout for the graph visualization, and then draws the graph using Matplotlib. The generated plot is saved as a PNG file.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises:
        OSError
            If there is an issue saving the plot to the specified file path.
        Exception:
            For any other unexpected errors that may occur during the process.

        """
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

        try:
            plt.savefig("plots/network.png", dpi=400)
        except OSError as ex:
            print(f"File Save Error: {ex}")
        except Exception as ex:
            print(f"Unexpected Error: {ex}")
        finally:
            plt.close("all")

    def degree_centrality_icm(self, seeds):
        """
        Models the spread of the gossip using independent cascade model.

        This function uses independent cascade model for analyzing the spread of the gossip in the network. It uses degree centrality as the probability of a node getting activated by its active neighbors.

        Parameters
        ----------
        seeds: list[int]
            The initiator nodes. These nodes are active at first and spread the gossip in the network

        Returns
        -------
        None

        Raises
        ------
        OSError
            If there is an issue saving the plot to the specified file path.
        ValueError:
            If seeds are not valid nodes in the network
        nx.NetworkXError:
            If there is an error related to graph operations
        Exception:
            For any other unexpected errors that may occur during the process.
        """

        try:
            active = set(seeds)
            new_active = set(seeds)

            degree_centralities = nx.degree_centrality(self.graph)

            while new_active:
                current_new_active = set()
                for node in new_active:
                    for neighbor in self.graph.neighbors(node):
                        if (
                            neighbor not in active
                            and neighbor not in current_new_active
                        ):
                            r = random.random()
                            p = degree_centralities[node]
                            if r < p:
                                current_new_active.add(neighbor)
                new_active = current_new_active
                active.update(new_active)

            self.active_nodes = active

            node_colors = [
                "red" if node in active else "skyblue" for node in self.graph.nodes()
            ]

            plt.figure(figsize=(12, 8))
            plt.title(f"Spread of Gossip initiating from {seeds[0]} and {seeds[1]}")
            pos = nx.spring_layout(self.graph, k=0.5, iterations=200)
            nx.draw(
                self.graph,
                pos,
                with_labels=True,
                node_size=600,
                node_color=node_colors,
                font_size=10,
                font_color="black",
                edge_color="gray",
            )

            try:
                plt.savefig(
                    f"plots/icm/degree_{seeds[0]}_{seeds[1]}.spread.png", dpi=400
                )
                print("Plot of ICM based on degree centrality is saved at plots/icm")
            except OSError as ex:
                print(f"File Save Error: {ex}")
            except Exception as ex:
                print(f"Unexpected Error: {ex}")
            finally:
                plt.close("all")

        except ValueError as ex:
            print(f"Value Error: {ex}")
        except nx.NetworkXError as ex:
            print(f"Graph Error: {ex}")
        except Exception as ex:
            print(f"Unexpceted Error: {ex}")

    def common_neighbors_influence(self, seeds):
        """
        Function that models the spread of information in network based on degree centrality and common neighbors influence

        Similar to ICM, this function models the spread of information in the network. Here as probability of a node getting activated I am using degree centrality. When common neighbor influence index for destination node is greater than this probability, the the node gets activated. The results gets saved at `plots/cnim/` folder.

        Parameters
        ----------
        seeds: list[int]
            Initial pair of nodes that are activated.

        Returns
        -------
        None

        Raises
        ------
        OSError
            If there is an issue saving the plot to the specified file path.
        ValueError:
            If seeds are not valid nodes in the network
        nx.NetworkXError:
            If there is an error related to graph operations
        Exception:
            For any other unexpected errors that may occur during the process.
        """
        try:
            # Checking whether seeds are connected
            if self.graph.has_edge(seeds[0], seeds[1]):
                active_nodes = list(seeds)
                centralities = nx.degree_centrality(self.graph)
                new_active = set(seeds)
                while new_active:
                    current_node = active_nodes[-1]
                    previous_node = active_nodes[0]

                    common_neighbors = set(
                        nx.common_neighbors(self.graph, previous_node, current_node)
                    )

                    neighbors = set(nx.neighbors(self.graph, current_node))

                    cn_index = len(common_neighbors) / len(neighbors)

                    neighbors_centralities = {
                        k: centralities[k] for k in neighbors if k in centralities
                    }

                    # Removing nodes that are already active from centrality of neighbors' list.
                    for key in active_nodes:
                        if key in neighbors_centralities.keys():
                            del neighbors_centralities[key]

                    most_influenced = max(
                        neighbors_centralities.items(),
                        key=lambda x: x[1],
                        default=(None, 0),
                    )

                    if most_influenced[0]:
                        if cn_index > most_influenced[1]:
                            active_nodes.append(most_influenced[0])
                            new_active.add(most_influenced[0])
                        else:
                            new_active = set()

                    else:
                        new_active = set()

                node_colors = [
                    self.GREEN if node in active_nodes else self.GRAY
                    for node in self.graph.nodes()
                ]

                plt.figure(figsize=(12, 8))
                plt.title(f"Spread of Gossip initiating from {seeds[0]} and {seeds[1]}")
                pos = nx.spring_layout(self.graph, k=0.5, iterations=200)
                nx.draw(
                    self.graph,
                    pos,
                    with_labels=True,
                    node_size=600,
                    node_color=node_colors,
                    font_size=10,
                    font_color="black",
                    edge_color=self.GRAY,
                )

                try:
                    plt.savefig(
                        f"plots/cnim/spread_from_{seeds[0]}_{seeds[1]}.png",
                        dpi=200,
                    )
                    plt.close("all")
                except OSError as ex:
                    print(f"Error saving file: {ex}")
                except Exception as ex:
                    print(f"Unexpected error: {ex}")
                finally:
                    plt.close("all")

        except ValueError as ex:
            print(f"Value Error: {ex}")
        except nx.NetworkXError as ex:
            print(f"Graph Error: {ex}")
        except Exception as ex:
            print(f"Unexpceted Error: {ex}")

    def run_icm_models(self, seeds):
        """
        Executes the network creation and the degree centrality-based Independent Cascade Model (ICM) simulation.

        This method first creates the network and then runs the simulation of the spread of gossip
        based on degree centrality, using the provided seed nodes.

        Parameters
        ----------
        seeds : list
            A list of nodes from which the gossip spread simulation will initiate.
        """
        self.create_network()
        # self.degree_centrality_icm(seeds=seeds)
        self.common_neighbors_influence(seeds=seeds)
