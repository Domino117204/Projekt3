import sys
from main import Graph
import time
import random

nodes = int(sys.argv[1])
rep = sys.argv[2]
action = sys.argv[3]

graph = Graph(nodes, rep)
graph.generate_acyclic_graph(30)  # Ustalona saturacja

if action == "find":
    u = random.randint(1, nodes)
    v = random.randint(1, nodes)
    t0 = time.perf_counter()
    graph.has_edge(u, v)
    t1 = time.perf_counter()
elif action == "kahn":
    t0 = time.perf_counter()
    try:
        graph.topological_sort_kahn()
    except:
        pass
    t1 = time.perf_counter()
elif action == "tarjan":
    t0 = time.perf_counter()
    try:
        graph.topological_sort_tarjan()
    except:
        pass
    t1 = time.perf_counter()
else:
    print("Unknown action")
    sys.exit(1)

print(f"TIME: {t1 - t0:.6f}")
