import random
import matplotlib.pyplot as plt
import networkx as nx

def create_smej_matrix(choice, n):
    smej_matrix = [[0]*n for _ in range(n)]

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


# Ручная реализация combinations
def combinations(lst, r):
    n = len(lst)
    if r > n:
        return []
    indices = list(range(r))
    yield [lst[i] for i in indices]
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield [lst[i] for i in indices]


def find_max_empty_subgraphs(adj_matrix):
    """Поиск ВСЕХ максимальных пустых подграфов (независимых множеств)."""
    n = len(adj_matrix)
    vertices = list(range(n))
    max_size = 0
    max_empty_subgraphs = []

    for size in range(n, 0, -1):
        for candidate in combinations(vertices, size):
            is_independent = True
            # Проверяем все пары в кандидате
            cand_list = list(candidate)
            for i in range(len(cand_list)):
                for j in range(i + 1, len(cand_list)):
                    u = cand_list[i]
                    v = cand_list[j]
                    if adj_matrix[u][v] == 1:
                        is_independent = False
                        break
                if not is_independent:
                    break
            if is_independent:
                if size > max_size:
                    max_size = size
                    max_empty_subgraphs = [list(candidate)]
                elif size == max_size:
                    max_empty_subgraphs.append(list(candidate))
        if max_empty_subgraphs:
            return max_empty_subgraphs
    return max_empty_subgraphs


def find_max_complete_subgraphs(adj_matrix):
    """Поиск ВСЕХ максимальных полных подграфов (клик)."""
    n = len(adj_matrix)
    vertices = list(range(n))
    max_size = 0
    max_complete_subgraphs = []

    for size in range(n, 0, -1):
        for candidate in combinations(vertices, size):
            is_clique = True
            cand_list = list(candidate)
            for i in range(len(cand_list)):
                for j in range(i + 1, len(cand_list)):
                    u = cand_list[i]
                    v = cand_list[j]
                    if adj_matrix[u][v] == 0:
                        is_clique = False
                        break
                if not is_clique:
                    break
            if is_clique:
                if size > max_size:
                    max_size = size
                    max_complete_subgraphs = [list(candidate)]
                elif size == max_size:
                    max_complete_subgraphs.append(list(candidate))
        if max_complete_subgraphs:
            return max_complete_subgraphs
    return max_complete_subgraphs


def color_graph(adj_matrix):
    """Ручная раскраска графа жадным методом."""
    n = len(adj_matrix)
    colors = [-1] * n

    for u in range(n):
        used_colors = set()
        for v in range(n):
            if adj_matrix[u][v] == 1 and colors[v] != -1:
                used_colors.add(colors[v])
        color = 0
        while color in used_colors:
            color += 1
        colors[u] = color

    coloring = {i: colors[i] for i in range(n)}
    chromatic_number = max(colors) + 1
    return coloring, chromatic_number


def draw_colored_graph(adj_matrix, coloring):
    """Отрисовка графа с раскраской."""
    G = nx.Graph()
    n = len(adj_matrix)
    for i in range(n):
        G.add_node(i)
    for i in range(n):
        for j in range(i + 1, n):
            if adj_matrix[i][j] == 1:
                G.add_edge(i, j)

    colors = [coloring[node] for node in G.nodes()]
    nx.draw(G, with_labels=True, node_color=colors, cmap=plt.cm.tab10, node_size=500)
    plt.title("Раскрашенный граф")
    plt.show()


print("Выберите тип графа:\n1. Простой\n2. С петлями\n3. С кратными рёбрами\n4. Полный")
choice = int(input("Ваш выбор (1-4): "))
n = int(input("Число вершин: "))

adjacency_matrix = create_smej_matrix(choice, n)

print("\nМатрица смежности:")
col_headers = [f"V{i}" for i in range(n)]
print("     ", "  ".join(f"{h:>3}" for h in col_headers))
for idx, row in enumerate(adjacency_matrix):
    print(f"V{idx:<2} ", "  ".join(f"{val:>3}" for val in row))

# Раскраска графа
coloring, chromatic_number = color_graph(adjacency_matrix)
print(f"\nРаскраска графа: {coloring}")
print(f"Хроматическое число: {chromatic_number}")

# Поиск максимальных пустых подграфов
max_empty_subgraphs = find_max_empty_subgraphs(adjacency_matrix)
print("\nВсе максимальные пустые подграфы (независимые множества):")
for i, subgraph in enumerate(max_empty_subgraphs, 1):
    print(f"{i}. {subgraph}")

# Поиск максимальных полных подграфов
max_complete_subgraphs = find_max_complete_subgraphs(adjacency_matrix)
print("\nВсе максимальные полные подграфы (клики):")
for i, subgraph in enumerate(max_complete_subgraphs, 1):
    print(f"{i}. {subgraph}")

# Отрисовка графа
draw_colored_graph(adjacency_matrix, coloring)
