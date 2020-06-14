#!/usr/bin/python3
import random
import networkx as nx
import matplotlib.pyplot as plt
import argparse
from statistics import mean
import math


def intensity_matrix_generator(n):
    return [[random.randint(0, 15) if j != i else 0 for j in range(n)] for i in range(n)]
    # return [[10 if j != i else 0 for j in range(n)] for i in range(n)]


class MyGraph:
    def __init__(self, N, edges, vertex, is_c=False):
        self.N = N
        self.edges = []
        self.edgeDict = {}
        for edge in edges:
            self.add_edge(edge)
        self.vertex = vertex
        self.g = sum([sum(x) for x in N])
        self.pos = None
        if not is_c:
            self.generate_a(first_time=True, quick=True)
            self.generate_c()
        self.generate_pos()

    def generate_pos(self):
        G = nx.Graph()
        for node in self.vertex:
            G.add_node(node)
        self.pos = nx.spring_layout(G)

    def print(self):
        G = nx.Graph()
        for node in self.vertex:
            G.add_node(node)
        labels = {}
        black = []
        red = []
        for edge in filter(lambda e: e.works, edges):
            if edge.a / (edge.c / edge.m) > 0.90 or edge.c <= edge.m or int(edge.a)+1 ==int(edge.c / edge.m):
                red.append((edge.start, edge.end))
            else:
                black.append((edge.start, edge.end))
            labels[(edge.start, edge.end)] = str(int(edge.a)) + " z " + str(int(edge.c / edge.m))

        nx.draw_networkx_nodes(G, self.pos, self.vertex, node_color="black")
        nx.draw_networkx_edges(G, self.pos, node_color='red', edgelist=black, edge_color="black")
        nx.draw_networkx_edges(G, self.pos, node_color='red', edgelist=red, edge_color="red")

        nx.draw_networkx_edge_labels(G, self.pos, edge_labels=labels, font_size=6)
        nx.draw_networkx_labels(G, self.pos, font_color="white")
        plt.axis('off')
        plt.show()

    def find_path(self, start, end, value=0, first_time=False):
        G = nx.Graph()
        for node in self.vertex:
            G.add_node(node)
        for edge in [x for x in self.edges if first_time or (x.works and x.c / x.m > x.a + value)]:
            G.add_edge(edge.start, edge.end)
        return nx.dijkstra_path(G, start, end)

    def generate_a(self, quick=False, first_time=False):
        for x in self.edges:
            if first_time:
                x.works = True
            else:
                x.works_fun()
            x.a = 0
        for i in range(len(self.N)):
            for j in range(len(self.N)):
                if i != j:
                    value = self.N[i][j]
                    if quick:
                        l = self.find_path(self.vertex[i], self.vertex[j], value=value, first_time=first_time)
                        for k in range(1, len(l)):
                            a = self.find_edge(l[k - 1], l[k])
                            self.edges[a].a += value
                    else:
                        while value != 0:
                            l = self.find_path(self.vertex[i], self.vertex[j], value=1, first_time=first_time)
                            chosen = [self.find_edge(l[k - 1], l[k]) for k in range(1, len(l))]
                            chosen_c = min(
                                list(map(lambda z: (self.edges[z].c / self.edges[z].m) - self.edges[z].a, chosen)))
                            if value < chosen_c:
                                s = value
                            else:
                                s = int(chosen_c - 1)
                            for e in chosen:
                                self.edges[e].a += s
                            value -= s

    def find_edge(self, start, end):
        x = self.edgeDict.get((start, end))
        if x is None:
            raise Exception("Can\'t find edge")
        else:
            return x

    def generate_c(self):
        avg4 = int(4 * mean([x.a for x in self.edges]))
        for edge in self.edges:
            edge.c = avg4 * edge.m

    def calculate_t(self):
        return (1 / self.g) * sum(e.a / (e.c / e.m - e.a) for e in self.edges)

    def statics(self, t_max, n):
        c = 0
        t_c = 0.0
        for h in range(n):
            try:
                self.generate_a()
                t = self.calculate_t()
                if t < t_max:
                    c += 1
                    t_c += t
                else:
                    pass
                    # graph.print()
            except nx.exception.NetworkXNoPath:
                pass
        return t_c / n, c / n * 100

    def add_edge(self, edge):
        i = len(self.edges)
        self.edges.append(edge)
        self.edgeDict[(edge.start, edge.end)] = i
        self.edgeDict[(edge.end, edge.start)] = i


class Edge:
    def __init__(self, start, end, c=0, m=1, p=1.0):
        self.start = start
        self.end = end
        self.a = 0
        self.c = c
        self.m = m
        self.p = p
        self.works = True

    def works_fun(self, x=0):
        self.works = random.random() <= self.p


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--graph", help="choose predefined graph ( 1 or 2), or type filename with graph")
    parser.add_argument("-e", "--exercise", choices=["1", "2", "3", "4", "5"], help="choose exercise")
    parser.add_argument("-t", "--t_max", help="type t_max")
    parser.add_argument("-p", "--probability", help="choose probability from [0...1]")
    parser.add_argument("-ac", "--auto_c", action="store_true", help="automatically add c(e) (for graph from file)")
    parser.add_argument("-m", "--package", help="type package size (int)")

    args = parser.parse_args()
    is_c = False
    try:
        probability = float(args.probability)
        override_p = True
    except:
        override_p = False
        probability = 0.95
    try:
        t_max = float(args.t_max)
    except:
        t_max = 1
    try:
        m = int(args.package)
        override_m= True
    except:
        m = 1
        override_m= False

    if args.graph == "1":
        edges = [Edge("a", "b", p=probability,m=m), Edge("b", "c", p=probability,m=m), Edge("c", "d", p=probability,m=m),
                 Edge("d", "e", p=probability,m=m), Edge("e", "f", p=probability,m=m), Edge("f", "g", p=probability,m=m),
                 Edge("g", "h", p=probability,m=m), Edge("h", "i", p=probability,m=m), Edge("i", "j", p=probability,m=m),
                 Edge("j", "a", p=probability,m=m), Edge("a", "k", p=probability,m=m), Edge("b", "m", p=probability,m=m),
                 Edge("d", "n", p=probability,m=m), Edge("e", "p", p=probability,m=m), Edge("g", "r", p=probability,m=m),
                 Edge("i", "s", p=probability,m=m), Edge("k", "l", p=probability,m=m), Edge("l", "m", p=probability,m=m),
                 Edge("m", "n", p=probability,m=m), Edge("n", "o", p=probability,m=m), Edge("o", "p", p=probability,m=m),
                 Edge("p", "q", p=probability,m=m), Edge("q", "r", p=probability,m=m), Edge("r", "s", p=probability,m=m),
                 Edge("s", "t", p=probability,m=m), Edge("t", "k", p=probability,m=m), Edge("l", "q", p=probability,m=m),
                 Edge("m", "s", p=probability,m=m), Edge("t", "o", p=probability,m=m)]
        vertex = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t"]
        N = intensity_matrix_generator(20)
    elif args.graph is not None and args.graph != "2":
        try:
            with open(args.graph, "r") as f:
                a = f.readline().split()
                vertex = f.readline().split()
                edges = []
                while True:
                    line = f.readline()
                    if not line:
                        break
                    s = line.split()
                    if not override_p:
                        pr = float(s[2])
                    else:
                        pr = probability
                    if not override_m:
                        mr = int(s[3])
                    else:
                        mr = m
                    edges.append(Edge(s[0], s[1], p=pr, m=mr, c=int(s[4])))
                N = []
                c = 0
                for i in vertex:
                    r = []
                    for j in vertex:
                        if i == j:
                            r.append(0)
                        else:
                            r.append(int(a[c]))
                        c += 1
                    N.append(r)
                is_c = True
        except FileNotFoundError:
            print("File does not exist")
            exit(0)
    else:
        edges = [Edge("a", "b", p=probability,m=m), Edge("c", "b", p=probability,m=m), Edge("c", "d", p=probability,m=m),
                 Edge("d", "b", p=probability,m=m), Edge("c", "e", p=probability,m=m)]
        vertex = ["a", "b", "c", "d", "e"]
        N = intensity_matrix_generator(5)

    if args.auto_c:
        is_c = False

    graph = MyGraph(N, edges, vertex, is_c=is_c)

    if args.exercise == "2":
        t, p = graph.statics(t_max, 10000)
        print("Network reliability", "t=", t, p, "%")

    elif args.exercise == "3":
        increase = 1.10
        r = 1
        print("Every iteration, N is multiplied by 1.10")
        i = 0
        while r != 0:
            t, r = graph.statics(t_max, 10000)
            print(i, "t=", t, r, "%")
            graph.N = [[math.ceil(y * increase) for y in x] for x in graph.N]
            i += 1

    elif args.exercise == "4":
        increase = 1.10
        r = 1
        print("Every iteration, c(e) is multiplayed by 1.10")
        i = 0
        while r < 100:
            t, r = graph.statics(t_max, 10000)
            print(i, "t=", t, r, "%")
            for edge in graph.edges:
                edge.c = int(math.ceil(edge.c * increase))
            i += 1

    elif args.exercise == "5":
        avg = int(mean([x.a * x.m for x in graph.edges]))
        m = graph.edges[0].m
        p = graph.edges[0].p
        print("Every iteration, new edge is added to the graph")
        c = 0
        new_edges = []
        graph.print()
        t, s = graph.statics(t_max, 10000)
        print(c, "t=", t, s, "%")
        for i in range(len(graph.vertex)):
            for j in range(len(graph.vertex)):
                if i < j and graph.edgeDict.get((graph.vertex[i], graph.vertex[j])) is None:
                    new_edges.append(Edge(graph.vertex[i], graph.vertex[j], c=avg, m=m, p=p))
        while new_edges:
            c += 1
            e = new_edges.pop(random.randint(0, len(new_edges) - 1))
            print(e.start, e.end)
            graph.add_edge(e)
            t, s = graph.statics(t_max, 10000)
            print(c, "t=", t, s, "%")

    else:
        try:
            graph.generate_a(quick=False)
            print("t=", graph.calculate_t())
        except nx.exception.NetworkXNoPath as e:
            print(e.args[0])
        graph.print()
