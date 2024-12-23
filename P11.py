from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('P11.html')

@app.route('/calculate_shortest_path', methods=['POST'])
def calculate_shortest_path():
    num_cities = int(request.form['num_cities'])
    cities = request.form.getlist('city_names')
    source_city = request.form['source_city']

    distances = request.form.getlist('distances')
    distance_matrix = []
    index = 0
    for i in range(num_cities):
        row = []
        for j in range(num_cities):
            value = distances[index]
            row.append(float('inf') if value == "∞" or value == "" else int(value))  
            index += 1
        distance_matrix.append(row)

    source_index = cities.index(source_city)

    shortest_paths = dijkstra(distance_matrix, source_index)

    results = [(cities[i], shortest_paths[i]) for i in range(num_cities)]

    display_matrix = [[("∞" if cell == float('inf') else cell) for cell in row] for row in distance_matrix]
    display_results = [(city, ("∞" if dist == float('inf') else dist)) for city, dist in results]

    return render_template(
        'results.html',
        cities=cities,
        matrix=display_matrix,
        source=source_city,
        results=display_results
    )

def dijkstra(graph, src):
    n = len(graph)
    dist = [float('inf')] * n
    dist[src] = 0
    visited = [False] * n

    for _ in range(n):
        u = min_distance(dist, visited)
        visited[u] = True

        for v in range(n):
            if graph[u][v] != float('inf') and not visited[v] and dist[u] + graph[u][v] < dist[v]:
                dist[v] = dist[u] + graph[u][v]

    return dist

def min_distance(dist, visited):
    min_val = float('inf')
    min_index = -1
    for v in range(len(dist)):
        if dist[v] < min_val and not visited[v]:
            min_val = dist[v]
            min_index = v
    return min_index

if __name__ == '__main__':
    app.run(debug=True, port=1011)
