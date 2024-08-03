# Friendship Network and Information diffusion

This project is a subsequent of another project in which I analyzed my friends network using Social Network Analysis and Graph theory. I've read a paper about spread of gossip in society and I decided to model the spread of the gossip and in general information diffusion in my network of friends.

### About this projcet

For modeling information diffusion in my network, first I use a simple version of a model called **Independent Cascade Model (ICM)**. In this implementaion there were two numbers being compared. One is a random number between 0 and 1, and the other is the probability of a node getting activated. 

## Information Diffusion 

Information Diffusion in social networks referes to process by which information spreads from one node to anther nodes within the network. Studying information difussion and identifying the processes of it, is important because it can help us to understand how nodes are interacting with each other. This can be useful in the fields such marketing, public health, and social sciences.

### Independent Cascade Model

This models is a simple probabalistic model used to simulate the spread of **influence** through the network. This method was introduced by Kemple et al. in 2003. It is specially useful in fields like epidemiology, viral marketing, and social netowrks. 

How ICM works:
1. *Initial Activation*: The process of modeling starts with a set of nodes that are initially activated. Activation here means two or more nodes are engaged in spreading the information. Since I am studying spread of gossip on my network, I will use gossip instead of information from now on. For example in my modeling in the `src` folder, I defined nodes 12 and 5 to be initially activated. 

2. *Activation Process*: When a node $i$ becomes active, it has a single oppurtunity to activate all its inactive neighbors. For instance, if active node $i$ had two inactive neighbors $j$, $k$, it will attempt to activate those two nodes. Meaning, it will try to spread the gossip to these two nodes. In some models the categorize the nodes in three classes of Initiator, Ignorant, and Infected. The Ignorant nodes are inactive and do not participate in spreading the gossip, which means they are not influenced by the influnce of their active neighbors. Here the probability of activation makes sense, because not all the nodes have the same role in social networks.

3. *Sequential Attempts*: If node $i$ successfully activates node $j$ and node $k$, each of these new activated (or infected) nodes will try to activate their own neighbors. It is important to note, regardless of the result of activation one node only can attempt once to activate other nodes.

4. *Termination*: The process continues until no further activations are possible, meaning all potential activations have been exhausted.

We denote the probability of node $j$ getting activated by node $i$ as $p(i, j)$. This probability is often defined as a weight associated with the edge connecting $i$ to $j$. I think this is not a good choice, because there are other comprehensive and sophisticated measures for influence that can be used as the probability of a node getting activated. One measure that can be used in this regard is called **Eigenvector Centrality** and it is usefull for assessing a node's influence on its neighbors.

In the `src/measures/measures.py`, I defined a function for ICM. In this algorithm I compare a random number between 0 and 1 with the probablity of a node getting activated. In a general network where the nodes are not friends, randomness can capture the random nature of spreading of the gossip in the social network. Gossip spreading in real life is not deterministic, and a person can choose to spread the gossip based on various factors that can be modeled probabilistically. 

In my case, where I study my friendship network, nodes have a preference for spreading the gossip and have favorate nodes as destination nodes. This means they will spread the gossip to nodes they feel close to. This is why I try to model the spread of the gossip in the network without comparing a random number with node activation probability.

### The Network:
![Friendship Netowrk](src/plots//network.png)

## Results of implementing simple version of ICM:

First I used degree centrality of the nodes as the probabiltiy of a node getting activated by the node who is already active. Let's have a look at a graph of activated nodes. In this run nodes that are initially active, were nodes 12 and 18. I chose this nodes because the destination node (18) has only one connection to to node 12 and does not have any connections to other nodes of the network. It is very unlikely that node 18 could spread the gossip as shown in this chart. The randomness does not model this case well:

**Consideration**: The network is undirected and the algorithm assumes node 12 will spread the gossip to other nodes than 18 as well. This is not what I assume, and I will change the code in a way, in which nodes can only activate one node.

![Activated Nodes](src/plots//icm/degree_12_18.spread.png)

# Common Neighbors Influence Model:
I defined a simple model that is based on Independent Cascade Model (ICM). In this model, I used degree centrality as node activation probability, as before. Instead of a random number, I defined an index called **common neighbors influence index** which denoted as `cn_index` in the code. We calculate this index as follows:

$$\text{CN Index} = \frac{\text{Number of common neighbors of node i and j}}{\text{Total number of neighbors of node j}}$$

This index takes into the account that the nodes sharing the most common neighbors are likely close to each other and, therefore they will chose themselves as destination nodes for gossip.

The result of implementing this model on my network is depicted in the left graph below. The graph on the right shows the spreading of the gossip for same initial active nodes, but uses the simple version of the ICM. As you can see, in the left graph, fewer nodes got activated and nodes are mostly belongs to community of the second initial active node. I think this model can simulate the spread of the gossip more realistically than the previous method.

<figure style="text-align: center;">
  <figcaption>Spread of gossip from 12 to 5, using the model I defined.</figcaption>
  <img src="src/plots/cnim/spread_from_12_5.png" alt="Activated Nodes" style="max-width: 100%; height: auto;">
</figure>


<figure style="text-align: center;">
  <figcaption>Spread of gossip from 12 to 5, using the simple version of ICM.</figcaption>
  <img src="src/plots/icm/degree_12_5.spread.png" alt="Activated Nodes" style="max-width: 100%; height: auto;">
</figure>
  
