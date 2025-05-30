import random
import matplotlib.pyplot as plt
import networkx as nx
from math import inf


def create_smej_matrix(choice, n):
    smej_matrix = []
    for i in range(n):
        row = [0 for _ in range(n)]
        smej_matrix.append(row)

    if choice == 1:
        for i in range(n):
            for j in range(i + 1, n):
                if random.randint(0, 1) == 1:
                    smej_matrix[i][j] = 1
                    smej_matrix[j][i] = 1

    elif choice == 2:
        for i in range(n):
            for j in range(i + 1, n):
                if random.randint(0, 1) == 1:
                    smej_matrix[i][j] = 1
                    smej_matrix[j][i] = 1
            if random.randint(0, 1) == 1:
                smej_matrix[i][i] = 1

    elif choice == 3:
        for i in range(n):
            for j in range(i, n):
                if random.randint(0, 1) == 1:
                    smej_matrix[i][j] = 1
                    smej_matrix[j][i] = 1

    elif choice == 4:
        for i in range(n):
            for j in range(i + 1, n):
                smej_matrix[i][j] = 1
                smej_matrix[j][i] = 1

    return smej_matrix


def create_incidence_matrix(smej_matrix):
    n = len(smej_matrix)
    edge_list = []

    for i in range(n):
        for j in range(i, n):
            if smej_matrix[i][j] == 1:
                edge_list.append((i, j))

    edge_count = len(edge_list)
    incidence_matrix = [[0 for _ in range(edge_count)] for _ in range(n)]
    col_names = []

    for inc, (u, v) in enumerate(edge_list):
        if u == v:
            incidence_matrix[u][inc] = 2
        else:
            incidence_matrix[u][inc] = 1
            incidence_matrix[v][inc] = 1
        col_names.append(f"({u},{v})")

    return incidence_matrix, col_names


def show_graph(smej_matrix):
    G = nx.Graph()
    n = len(smej_matrix)

    for i in range(n):
        G.add_node(i)

    for i in range(n):
        for j in range(i, n):
            if smej_matrix[i][j] == 1:
                G.add_edge(i, j)

    nx.draw(G, with_labels=True, node_color='red', node_size=500)
    plt.title("Граф по матрице смежности")
    plt.show()


def print_matrix_with_headers(matrix, col_names, row_prefix="V"):
    print("      ", end="")
    for name in col_names:
        print(f"{name:>6}", end=" ")
    print()
    for idx, row in enumerate(matrix):
        print(f"{row_prefix}{idx:<3} ", end=" ")
        for val in row:
            print(f"{val:>6}", end=" ")
        print()


def matrix_multiply(a, b):
    n = len(a)
    result = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += a[i][k] * b[k][j]
    return result


def matrix_power(matrix, power):
    result = matrix
    for _ in range(power - 1):
        result = matrix_multiply(result, matrix)
    return result


def metric_matrix(adj_matrix):
    n = len(adj_matrix)
    dist = [[0 if i == j else (1 if adj_matrix[i][j] else inf)
             for j in range(n)] for i in range(n)]

    changed = True  
    iterations = 0  
    max_iterations = n  

    while changed and iterations < max_iterations:
        changed = False
        
        new_dist = [[dist[i][j] for j in range(n)] for i in range(n)]

        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        new_dist[i][j] = dist[i][k] + dist[k][j]
                        changed = True  

        dist = new_dist
        iterations += 1
    return dist

def graph_characteristics(metric_matr):
    n = len(metric_matr)
    max_distances = [max(row) if max(row) != inf else inf for row in metric_matr]
    has_isolated = any(d == inf for d in max_distances)
    if has_isolated:
        radius = inf
        diameter = inf
    else:
        radius = min(max_distances)
        diameter = max(max_distances)
    central_vertices = [i for i, d in enumerate(max_distances) if d == radius]
    peripheral_vertices = [i for i, d in enumerate(max_distances) if d == diameter]
    return {
        'radius': radius,
        'diameter': diameter,
        'central_vertices': central_vertices,
        'peripheral_vertices': peripheral_vertices
    }


def print_metric_matrix(metric_matr):
    n = len(metric_matr)
    print("\nМатрица метрик (расстояний):")
    print("     ", end="")
    for i in range(n):
        print(f"{'V' + str(i):>6}", end=" ")
    print()
    for i in range(n):
        print(f"{'V' + str(i):<5}", end=" ")
        for j in range(n):
            if metric_matr[i][j] == inf:
                print(f"{'∞':>6}", end=" ")
            else:
                print(f"{metric_matr[i][j]:>6}", end=" ")
        print()


print("Выберите тип графа:\n1. Простой\n2. С петлями\n3. С кратными рёбрами\n4. Полный")
choice = int(input("Ваш выбор (1-4): "))
n = int(input("Число вершин: "))

adjacency_matrix = create_smej_matrix(choice, n)

print("\nМатрица смежности:")
col_headers = [f"V{i}" for i in range(n)]
print("     ", "  ".join(f"{h:>3}" for h in col_headers))
for idx, row in enumerate(adjacency_matrix):
    print(f"V{idx:<2} ", "  ".join(f"{val:>3}" for val in row))

incidence_matrix, edge_col_names = create_incidence_matrix(adjacency_matrix)

print("\nМатрица инцидентности:")
print_matrix_with_headers(incidence_matrix, edge_col_names)

metric_matr = metric_matrix(adjacency_matrix)
print_metric_matrix(metric_matr)

chars = graph_characteristics(metric_matr)
print("\nХарактеристики графа:")
print(f"Радиус: {chars['radius']}")
print(f"Диаметр: {chars['diameter']}")
print(f"Центральные вершины: {chars['central_vertices']}")
print(f"Периферийные вершины: {chars['peripheral_vertices']}")

print("\nМатрица смежности в квадрате (количество путей длины 2):")
adj_squared = matrix_power(adjacency_matrix, 2)
print("     ", "  ".join(f"{h:>3}" for h in col_headers))
for idx, row in enumerate(adj_squared):
    print(f"V{idx:<2} ", "  ".join(f"{val:>3}" for val in row))

show_graph(adjacency_matrix)
