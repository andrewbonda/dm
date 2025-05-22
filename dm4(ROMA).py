import matplotlib.pyplot as plt
import networkx as nx
import random

def graph_create(graph_type, graph_size):
    if graph_type == 1:  # Простой граф
        print("Матрица смежности для простого графа:")
        adjacency_matrix = [[random.randint(0, 1) for _ in range(graph_size)] for _ in range(graph_size)]
        for i in range(graph_size):
            adjacency_matrix[i][i] = 0
    elif graph_type == 2:  # Полный граф
        print("Матрица смежности для полного графа:")
        adjacency_matrix = [[1 for _ in range(graph_size)] for _ in range(graph_size)]
        for i in range(graph_size):
            adjacency_matrix[i][i] = 0
    elif graph_type == 3:  # Граф с петлями
        print("Матрица смежности для графа с петлями:")
        adjacency_matrix = [[random.randint(0, 1) for _ in range(graph_size)] for _ in range(graph_size)]
    return adjacency_matrix

def graph_print(adjacency_matrix):
    for row in adjacency_matrix:
        print(' '.join(map(str, row)))

def graph_vis(weight_matrix, distances):
    G = nx.DiGraph()
    num_nodes = len(weight_matrix)
    
    valid_distances = [d for d in distances if d != float('inf')]
    node_colors = []
    
    if not valid_distances:
        node_colors = ['gray'] * num_nodes
    else:
        max_d = max(valid_distances)
        if max_d == 0:
            node_colors = ['red' if d == 0 else 'gray' for d in distances]
        else:
            for d in distances:
                if d == float('inf'):
                    node_colors.append('gray')
                else:
                    ratio = d / max_d
                    r = int(255 * ratio)
                    g = int(255 * (1 - ratio))
                    b = 0
                    color = f'#{r:02x}{g:02x}{b:02x}'
                    node_colors.append(color)
    
    for i in range(num_nodes):
        for j in range(num_nodes):
            if weight_matrix[i][j] != 0:
                G.add_edge(i, j, weight=weight_matrix[i][j])
    
    pos = nx.spring_layout(G)
    edges = G.edges()
    
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=1500)
    labels = {(i, j): G[i][j]['weight'] for i, j in edges}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_color='green')
    plt.show()

def generate_weight_matrix(adjacency_matrix):
    n = len(adjacency_matrix)
    weight_matrix = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if adjacency_matrix[i][j] > 0:
                weight_matrix[i][j] = random.randint(1, 20)
            else:
                weight_matrix[i][j] = 0
    return weight_matrix

def dijkstra(graph, start):
    n = len(graph)
    distances = [float('inf')] * n
    distances[start] = 0
    visited = [False] * n
    
    for _ in range(n):
        min_distance = float('inf')
        min_node = -1
        for node in range(n):
            if not visited[node] and distances[node] < min_distance:
                min_distance = distances[node]
                min_node = node
        
        if min_node == -1:
            break
        visited[min_node] = True
        
        for neighbor in range(n):
            if graph[min_node][neighbor] != 0:
                new_distance = distances[min_node] + graph[min_node][neighbor]
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
    
    return distances

def calculate_chromatic_number(adjacency_matrix):
    # Проверка на наличие петель
    for i in range(len(adjacency_matrix)):
        if adjacency_matrix[i][i] != 0:
            return float('inf')  # Граф с петлями некрасим
    
    n = len(adjacency_matrix)
    colors = [0] * n
    color_count = 0
    
    # Сортируем вершины по убыванию степени
    vertices = sorted(range(n), key=lambda v: sum(adjacency_matrix[v]), reverse=True)
    
    for u in vertices:
        used_colors = set()
        # Проверяем все соседние вершины
        for v in range(n):
            if adjacency_matrix[u][v] != 0 or adjacency_matrix[v][u] != 0:
                if colors[v] != 0:
                    used_colors.add(colors[v])
        # Назначаем минимальный возможный цвет
        color = 1
        while color in used_colors:
            color += 1
        colors[u] = color
        if color > color_count:
            color_count = color
    
    return color_count

print("1 - простой граф\n2 - полный граф\n3 - граф с петлями")
graph_type = int(input("Введите номер: "))
graph_size = int(input("Введите размерность матрицы: "))
adjacency_matrix = graph_create(graph_type, graph_size)
weight_matrix = generate_weight_matrix(adjacency_matrix)
graph_print(adjacency_matrix)

start_node = int(input("Введите номер начальной вершины: "))
shortest_distances = dijkstra(weight_matrix, start_node)

print("\nКратчайшие расстояния:")
for node in range(len(shortest_distances)):
    distance = shortest_distances[node]
    if distance == float('inf'):
        print(f"От {start_node} до {node}: ∞")
    else:
        print(f"От {start_node} до {node}: {distance}")

chromatic_number = calculate_chromatic_number(adjacency_matrix)
if chromatic_number == float('inf'):
    print("\nХроматическое число графа: ∞ (граф содержит петли)")
else:
    print(f"\nХроматическое число графа: {chromatic_number}")

graph_vis(weight_matrix, shortest_distances)