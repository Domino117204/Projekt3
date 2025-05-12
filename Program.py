import sys
from collections import deque, defaultdict
import random
import math

class Graph:
    def __init__(self, nodes, representation="list"):
        self.nodes = nodes
        self.representation = representation
        self.matrix = [[0] * nodes for _ in range(nodes)]
        self.adj_list = [[] for _ in range(nodes)]
        self.table = []

    def add_edge(self, u, v):
        u -= 1
        v -= 1
        self.matrix[u][v] = 1
        self.adj_list[u].append(v + 1)
        if self.representation == "table":
            self.table.append((u + 1, v + 1))


    def print_graph(self):
        if self.representation == "matrix":
            print("   |", " ".join(f"{i+1:>2}" for i in range(self.nodes)))
            print("---+" + "---" * self.nodes)
            for i in range(self.nodes):
                row = " ".join(str(self.matrix[i][j]) for j in range(self.nodes))
                print(f"{i+1:>2} | {row}")
        elif self.representation == "list":
            for i in range(self.nodes):
                print(f"{i+1}: {' '.join(map(str, self.adj_list[i]))}")
        elif self.representation == "table":
            print("From -> To")
            for u, v in self.table:
                print(f" {u} -> {v}")

        else:
            print("Nieznana reprezentacja")

    def has_edge(self, u, v):
        u -= 1
        v -= 1
        return self.matrix[u][v] == 1

    def bfs(self, start):
        start -= 1
        visited = [False] * self.nodes
        queue = deque([start])
        visited[start] = True
        result = []

        while queue:
            current = queue.popleft()
            result.append(current + 1)
            for neighbor in self._neighbors(current):
                if not visited[neighbor - 1]:
                    visited[neighbor - 1] = True
                    queue.append(neighbor - 1)
        print("inline:", " ".join(map(str, result)))

    def dfs(self, start):
        start -= 1
        visited = [False] * self.nodes
        result = []

        def dfs_visit(node):
            visited[node] = True
            result.append(node + 1)
            for neighbor in self._neighbors(node):
                if not visited[neighbor - 1]:
                    dfs_visit(neighbor - 1)

        dfs_visit(start)
        print("inline:", " ".join(map(str, result)))

    def _neighbors(self, node):
        if self.representation == "matrix":
            return [i + 1 for i in range(self.nodes) if self.matrix[node][i] == 1]
        elif self.representation == "list":
            return self.adj_list[node]
        elif self.representation == "table":
            return [v for (u, v) in self.table if u == node + 1]
        return []
    
    def topological_sort_kahn(self):
        from collections import defaultdict, deque

        graph_dict = {i + 1: self.adj_list[i] for i in range(self.nodes)}
        in_degree = defaultdict(int)

        for u in graph_dict:
            for v in graph_dict[u]:
                in_degree[v] += 1

        S = deque([u for u in graph_dict if in_degree[u] == 0])
        L = []

        while S:
            n = S.popleft()
            L.append(n)
            for m in graph_dict[n]:
                in_degree[m] -= 1
                if in_degree[m] == 0:
                    S.append(m)

        if len(L) < len(graph_dict):
            raise ValueError("Graf zawiera przynajmniej jeden cykl.")
        return L

    def topological_sort_tarjan(self):
        visited_temp = set()   # tymczasowe oznaczenia
        visited_perm = set()   # trwałe oznaczenia
        result = []

        def visit(node):
            if node in visited_perm:
                return
            if node in visited_temp:
                raise ValueError("Graf zawiera cykl — sortowanie niemożliwe.")

            visited_temp.add(node)

            for neighbor in self._neighbors(node - 1):
                visit(neighbor)

            visited_temp.remove(node)
            visited_perm.add(node)
            result.append(node)

        for node in range(1, self.nodes + 1):
            if node not in visited_perm:
                visit(node)

        result.reverse()  # kolejność odwrotna do kolejności odwiedzin
        return result


    def generate_acyclic_graph(self, saturation):
        for i in range(1, self.nodes):
            for j in range(i + 1, self.nodes + 1):
                if random.random() < (saturation / 100):
                    self.add_edge(i, j)

    def export_to_tex(self, filename):
        edges = []
        for u in range(self.nodes):
            for v in self._neighbors(u):
                edges.append((u + 1, v))

        with open(filename, "w") as f:
            f.write("\\documentclass{article}\n")
            f.write("\\usepackage{tikz}\n")
            f.write("\\begin{document}\n")
            f.write("\\begin{tikzpicture}[->,node distance=2cm]\n")
            f.write("\\tikzstyle{every node}=[circle,draw]\n")

            node_positions = {}
            angle_step = 360 / self.nodes
            radius = 3

            for i in range(self.nodes):
                angle = i * angle_step
                x = radius * math.cos(math.radians(angle))
                y = radius * math.sin(math.radians(angle))
                node_positions[i + 1] = (x, y)
                f.write(f"\\node ({i + 1}) at ({x},{y}) {{{i + 1}}};\n")

            for u, v in edges:
                if u in node_positions and v in node_positions:
                    f.write(f"\\draw[->] ({u}) -- ({v});\n")

            f.write("\\end{tikzpicture}\n")
            f.write("\\end{document}\n")

        print(f"Graph exported to {filename}")

def main():
    if len(sys.argv) < 2:
        print("Użycie: ./program --generate lub ./program --user-provided")
        return

    if sys.argv[1] == "--generate":
        print("Dostępne reprezentacje grafu: matrix, list, table")
        rep = input("type> ").strip().lower()

        while rep not in ("matrix", "list", "table"):
            rep = input("Niepoprawna reprezentacja. Wpisz: matrix, list lub table> ").strip().lower()

        while True:
            try:
                nodes = int(input("nodes> "))
                if nodes <= 0:
                    raise ValueError
                break
            except ValueError:
                print("Błąd: Podaj dodatnią liczbę całkowitą dla liczby wierzchołków.")

        while True:
            try:
                saturation = int(input("saturation (0-100)> "))
                if not (0 <= saturation <= 100):
                    raise ValueError
                break
            except ValueError:
                print("Błąd: Wprowadź liczbę całkowitą w zakresie 0-100.")

        graph = Graph(nodes, rep)
        graph.generate_acyclic_graph(saturation)
        print("Graf wygenerowany!")

    elif sys.argv[1] == "--user-provided":
        print("Dostępne reprezentacje grafu: matrix, list, table")
        rep = input("type> ").strip().lower()

        while rep not in ("matrix", "list", "table"):
            rep = input("Niepoprawna reprezentacja. Wpisz: matrix, list lub table> ").strip().lower()

        while True:
            try:
                nodes = int(input("nodes> "))
                if nodes <= 0:
                    raise ValueError
                break
            except ValueError:
                print("Błąd: Podaj dodatnią liczbę całkowitą dla liczby wierzchołków.")

        graph = Graph(nodes, rep)

        for i in range(1, nodes + 1):
            while True:
                try:
                    line = input(f"{i}> ").strip()
                    if not line:
                        break
                    for v in map(int, line.split()):
                        if 1 <= v <= nodes:
                            graph.add_edge(i, v)
                        else:
                            print(f"Uwaga: Wierzchołek {v} nie istnieje (zakres 1–{nodes}) i został pominięty.")
                    break
                except ValueError:
                    print("Błąd: Wprowadź numery wierzchołków oddzielone spacjami.")
    else:
        print("Nieznana opcja. Użyj --generate lub --user-provided.")
        return

    while True:
        action = input("action> ").strip().lower()
        if action == "print":
            graph.print_graph()
        elif action == "find":
            try:
                u = int(input("from> "))
                v = int(input("to> "))
                if 1 <= u <= graph.nodes and 1 <= v <= graph.nodes:
                    if graph.has_edge(u, v):
                        print(f"True: edge ({u},{v}) exists in the Graph!")
                    else:
                        print(f"False: edge ({u},{v}) does not exist in the Graph!")
                else:
                    print(f"Błąd: Wierzchołki muszą być w zakresie 1–{graph.nodes}.")
            except ValueError:
                print("Błąd: Wprowadź poprawne liczby całkowite.")
        elif action == "export":
            filename = input("filename> ").strip()
            graph.export_to_tex(filename)
        elif action == "bfs":
            try:
                start = int(input("start> ") or "1")
                if 1 <= start <= graph.nodes:
                    graph.bfs(start)
                else:
                    print(f"Błąd: Numer wierzchołka musi być w zakresie 1–{graph.nodes}.")
            except ValueError:
                print("Błąd: Wprowadź poprawny numer wierzchołka.")
        elif action == "dfs":
            try:
                start = int(input("start> ") or "1")
                if 1 <= start <= graph.nodes:
                    graph.dfs(start)
                else:
                    print(f"Błąd: Numer wierzchołka musi być w zakresie 1–{graph.nodes}.")
            except ValueError:
                print("Błąd: Wprowadź poprawny numer wierzchołka.")
        elif action == "kahn":
            try:
                order = graph.topological_sort_kahn()
                print("Graf posortowany topologicznie algorytmem Kahna:", " ".join(map(str, order)))
            except ValueError as e:
                print("Błąd:", e)
        elif action == "tarjan":
            try:
                order = graph.topological_sort_tarjan()
                print("Graf posortowany topologicznie algorytmem Tarjana:", " ".join(map(str, order)))
            except ValueError as e:
                print("Błąd:", e)

        elif action in ("exit", "quit"):
            break
        elif action == "help":
            print("""
Dostępne akcje:
  Print                 - Wypisz graf w wybranej reprezentacji (matrix, list, table)
  Find                  - Sprawdź, czy istnieje krawędź (od x y)
  BFS                   - Breadth-first search (Przeszukiwanie wszerz)
  DFS                   - Depth-first search (Przeszukiwanie w głąb)
  Kahn                  - Sortowanie topologiczne algorytmem Kahna
  Export                - Eksportuj graf do pliku LaTeX (.tex) jako drzewo (TikZ)
  Help                  - Wyświetl to menu pomocy
  Exit / Quit           - Zakończ program
""")
        else:
            print("Nieznana akcja")

if __name__ == "__main__":
    main()