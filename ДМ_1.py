import random
import matplotlib.pyplot as plt
import networkx as nx


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
            incidence_matrix[u][inc] = 2  # Петля
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


# Основной код
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

show_graph(adjacency_matrix)
