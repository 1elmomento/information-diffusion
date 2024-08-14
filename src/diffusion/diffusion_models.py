import random
import math
import numpy as np
import networkx as nx
from networkx.algorithms import approximation as approx
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("QtAgg")


class Models:
    r"""
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

    common_neighbors_influence(seeds):
        This is a simple method based on ICM with minor modifications. In this methods we use degree centrality as the node activation probability, and an custom defined index for capability of node to activate other nodes. When this index is greater than the node activation probability, then the destination node gets activated.

    run_icm_models(seeds):
        This is a function for running all the methods. Aggergating all methods in one final method of the Class.
    """

    def __init__(self, nodes, edges) -> None:
        self.nodes = nodes
        self.edges = edges
        self.GREEN = "#20bf55"
        self.GRAY = "#ced4da"
        self.graph = nx.Graph()

    def create_network(self) -> None:
        r"""
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
            node_color=self.GRAY,
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
        r"""
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

            node_colors = [
                self.GREEN if node in active else self.GRAY
                for node in self.graph.nodes()
            ]

            plt.figure(figsize=(12, 8))
            plt.title(
                f"Spread of Gossip initiating from {seeds[0]} and {seeds[1]} using ICM"
            )
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
                    f"plots/icm/degree_{seeds[0]}_{seeds[1]}.spread.png", dpi=200
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
        r"""
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
                    previous_node = active_nodes[-2]

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

    def potential_diffusion_model(self, seeds, epsilon=0.1):
        r"""
        Function the simulate information diffusion based on Activation and Spreader Potential of receiver and spreader node.

        Parameters
        ----------
        seeds: list[int]
            Initial node that is active.

        epsilon: float
            damping coefficient for controling rate of decay of spread

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
            active_nodes = list(seeds)
            new_active = set(seeds)
            eigenvector_centraltiy = nx.eigenvector_centrality(self.graph)
            closeness_centrality = nx.closeness_centrality(self.graph)
            betweenness_centraltiy = nx.betweenness_centrality(self.graph)
            degree_centrality = nx.degree_centrality(self.graph)
            clustering = nx.clustering(self.graph)

            while new_active:
                for index, spreader in enumerate(active_nodes):
                    for node in self.graph.nodes():
                        if node not in active_nodes:
                            if self.graph.has_edge(spreader, node):

                                sp = (
                                    (
                                        degree_centrality[spreader]
                                        + betweenness_centraltiy[spreader]
                                        + closeness_centrality[spreader]
                                        + eigenvector_centraltiy[spreader]
                                    )
                                    / 4
                                    * (np.exp(-epsilon * index))
                                )

                                ap = clustering[node]

                                if sp > ap:
                                    print(f"({spreader}, {node}) - [{sp}, {ap}]")
                                    new_active.add(node)
                                    active_nodes.append(node)
                                else:
                                    new_active = set()
                            else:
                                new_active = set()
                        else:
                            new_active = set()

            print(active_nodes)

            node_colors = [
                self.GREEN if node in active_nodes else self.GRAY
                for node in self.graph.nodes()
            ]

            plt.figure(figsize=(12, 8))
            plt.title(f"Spread of Gossip initiating from {seeds[0]} using ERI")
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
                    f"plots/potential/potential_diffusion_{seeds[0]}.png", dpi=200
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

    def run_icm_models(self, seeds):
        r"""
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
        # self.common_neighbors_influence(seeds=seeds)
        self.eigenvector_spread_model(seeds=seeds)

    def run_eigenvector_spread(self, seeds, epsilon):
        self.create_network()
        self.potential_diffusion_model(seeds=seeds, epsilon=epsilon)
