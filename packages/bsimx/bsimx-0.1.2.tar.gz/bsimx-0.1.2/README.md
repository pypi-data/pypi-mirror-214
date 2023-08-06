# bsimx

The agent-based modeling tool with [deck.gl](https://deck.gl/), [networkx](https://networkx.org/) and [osmnx](https://osmnx.readthedocs.io/en/stable/)..

## Getting Started

```py
import networkx as nx
import osmnx as ox
from bsimx import preview, Agent, simulate

# networkx graph from open street map.
G = ox.graph_from_place("Takamatsu Hayashi", network_type="drive")

# simple walker model
class SimpleWalker(Agent):
    start: int # start node id
    goal: int # goal node id

    # the action of this model on simulation started
    def on_started(self, G: nx.Graph, *_):
        # move to `start` immediately
        self.teleport(G, self.start)
        # set goal node
        # continue to move to `goal` with Dijkstra algorithm
        self.set_goal(G, self.goal)
        # moving speed: 1.0 ms
        self.set_speed(G, 1.0)

# give parameters to model
instances = [SimpleWalker(id=1, start=1042117440, goal=1042116599)]

# simulation
trips = simulate(instances, G)

# preview on web map
preview(G, trips)
```
