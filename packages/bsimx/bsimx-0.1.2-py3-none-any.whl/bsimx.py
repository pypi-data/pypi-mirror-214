from typing import List, Self, Any
import networkx as nx
import json
import numpy as np
from flask import Flask, redirect
from flask_cors import CORS
import json


class Agent:
    @staticmethod
    def fields():
        return ["x", "y", "timestamp"]

    __id: int
    __history: List[List[Any]]
    __route: List[Any]
    __edge_progress: float
    __timestamp: int
    __speed: float

    def __init__(self, id: int, **kwargs):
        self.__id = id
        self.reset()
        for k in kwargs:
            setattr(self, k, kwargs[k])

    def push_history(self, G: nx.Graph):
        d = self.get_data(G)
        self.__history.append(d)

    def get_data(self, G: nx.Graph):
        len_r = len(self.__route)
        if len_r == 0:
            return {"x": None, "y": None, "timestamp": self.__timestamp}

        n1 = G.nodes[self.__route[0]]
        x_key = G.graph["x_key"]
        y_key = G.graph["y_key"]
        if len_r == 1:
            return {
                "x": n1[x_key],
                "y": n1[y_key],
                "timestamp": self.__timestamp,
            }
        n2 = G.nodes[self.__route[1]]
        if type(G) is nx.MultiGraph or type(G) is nx.MultiDiGraph:
            edge_datas = G.get_edge_data(self.__route[0], self.__route[1])
            d = min([edge_datas[key][G.graph["length_key"]] for key in edge_datas])
        else:
            d = G.get_edge_data(self.__route[0], self.__route[1])[G.graph["length_key"]]
        w2 = self.__edge_progress / d
        w1 = 1 - w2
        return {
            "x": n1[x_key] * w1 + n2[x_key] * w2,
            "y": n1[y_key] * w1 + n2[y_key] * w2,
            "timestamp": self.__timestamp,
        }

    def is_arrived(self):
        return len(self.__route) <= 1

    def tick(self, G: nx.Graph):
        self.__timestamp += 1
        len_r = len(self.__route)
        if len_r < 2:
            return
        n1, n2 = self.__route[:2]
        if type(G) is nx.MultiGraph or type(G) is nx.MultiDiGraph:
            edge_datas = G.get_edge_data(self.__route[0], self.__route[1])
            d = min([edge_datas[key][G.graph["length_key"]] for key in edge_datas])
        else:
            d = G.get_edge_data(self.__route[0], self.__route[1])[G.graph["length_key"]]
        self.__edge_progress += self.__speed
        if self.__edge_progress >= d:
            # on_stepped
            r = self.__edge_progress - d
            self.__route.pop(0)
            self.__edge_progress = 0.0
            self.push_history(G)
            self.on_stepped(n2, G)
            self.__edge_progress = r
            if len_r == 2:
                # on_arrived
                self.on_arrived(n2, G)

    def get_id(self):
        return self.__id

    def get_history(self):
        return json.loads(json.dumps(self.__history))

    def reset(self):
        self.__history = []
        self.__route = []
        self.__edge_progress = 0
        self.__timestamp = 0
        self.__speed = 1.0

    def teleport(self, G: nx.Graph, node: Any):
        goal = self.__route[-1] if len(self.__route) > 1 else None
        self.__edge_progress = 0.0
        self.__route = [node]
        if goal:
            self.set_goal(goal, G)
        self.push_history(G)

    def set_goal(self, G: nx.Graph, goal: Any):
        r_len = len(self.__route)
        if r_len == 0:
            return
        elif r_len == 1 or self.__edge_progress == 0.0:
            source = self.__route[0]
            path = self.search_path(G, source, goal)
            self.__route = path
            return
        n1 = self.__route[0]
        n2 = self.__route[1]
        d = G[n1][n2][G.graph["length_key"]]
        p1 = self.search_path(G, n1, goal)
        p2 = self.search_path(G, n2, goal)
        d1 = (
            np.sum([G[i][j][G.graph["length_key"]] for i, j in zip(p1, p1[1:])])
            if len(p1) > 1
            else 0.0
        ) + self.__edge_progress
        d2 = (
            np.sum([G[i][j][G.graph["length_key"]] for i, j in zip(p2, p2[1:])])
            if len(p1) > 1
            else 0.0
        ) + (d - self.__edge_progress)
        self.__route = p1 if d1 < d2 else p2
        if d1 < d2:
            self.__edge_progress = d - self.__edge_progress

    def set_speed(self, G: nx.Graph, speed: float):
        self.__speed = speed
        self.push_history(G)

    def search_path(self, G: nx.Graph, source: Any, target: Any):
        """maybe override"""
        return nx.dijkstra_path(G, source, target, weight=G.graph["length_key"])

    def on_started(self, G: nx.Graph, agents: List[Self]):  # type: ignore
        """for override"""

    def on_stepped(self, G: nx.Graph, node: int):
        """for override"""

    def on_arrived(self, G: nx.Graph, node: int):
        """for override"""


def simulate(
    agents: List[Agent], G: nx.Graph, x_key="x", y_key="y", length_key="length"
):
    g = G.copy()
    g.graph["x_key"] = x_key
    g.graph["y_key"] = y_key
    g.graph["length_key"] = length_key
    for a in agents:
        a.on_started(g, agents)

    while any([not a.is_arrived() for a in agents]):
        for a in agents:
            a.tick(g)

    data = [
        {"id": a.get_id(), "class": a.__class__.__name__, "history": a.get_history()}
        for a in agents
    ]

    for a in agents:
        a.reset()

    return data


def serializable(item: Any):
    try:
        json.dumps(item)
    except TypeError:
        return False
    return True


def preview(G: nx.Graph, simulation_result: list[dict[str, Any]] = []):
    app = Flask(__name__)
    CORS(app)

    nodes = [
        (n[0], {k: n[1][k] for k in n[1] if serializable(n[1][k])})
        for n in G.nodes(data=True)
    ]
    edges = [
        (e[0], e[1], {k: e[2][k] for k in e[2] if serializable(e[2][k])})
        for e in G.edges(data=True)
    ]

    @app.route("/")
    def home():
        return redirect("/api/bsim")

    @app.route("/api/bsim")
    def bsim_result():
        return {"trips": simulation_result, "nodes": nodes, "edges": edges}

    print(
        """
###################################################
Bsim Preview 🗺️ : https://bsimx.netlify.app/preview
###################################################"""
    )
    app.run()
