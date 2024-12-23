from flask import Flask, render_template, request
from itertools import permutations
import numpy as np

app = Flask(__name__)

def traveling_salesman(distance_matrix):
    num_nodes = len(distance_matrix)
    min_travel_cost = float('inf')
    optimal_path = []
    optimal_segments = []
    
    for node_permutation in permutations(range(num_nodes)):
        total_cost = 0
        path_segments = []
        
        for i in range(num_nodes):
            total_cost += distance_matrix[node_permutation[i]][node_permutation[(i + 1) % num_nodes]]
            path_segments.append((node_permutation[i] + 1, node_permutation[(i + 1) % num_nodes] + 1,
                                  distance_matrix[node_permutation[i]][node_permutation[(i + 1) % num_nodes]]))
        
        if total_cost < min_travel_cost:
            min_travel_cost = total_cost
            optimal_path = node_permutation
            optimal_segments = path_segments
    
    return optimal_path, min_travel_cost, optimal_segments

@app.route('/', methods=['GET', 'POST'])
def index():
    distance_input_matrix = []
    if request.method == 'POST':
        node_count = int(request.form['nodes'])
        dist_matrix = np.full((node_count, node_count), np.inf)
        
        for i in range(node_count):
            row = []
            for j in range(node_count):
                weight_key = f'weight_{i}_{j}'
                weight_value = request.form[weight_key]
                
                if weight_value == '∞':
                    dist_matrix[i][j] = 0
                else:
                    dist_matrix[i][j] = int(weight_value)
                row.append(weight_value)
            distance_input_matrix.append(row)
        
        optimal_path, min_cost, path_segments = traveling_salesman(dist_matrix)
        path_representation = ' - '.join(str(i + 1) for i in optimal_path) + f' - 1'
        segments_representation = ', '.join([f"{start} - {end} = {cost}" for start, end, cost in path_segments])
        
        result = {
            'path': path_representation,
            'cost': min_cost,
            'input_matrix': distance_input_matrix,
            'segments': segments_representation
        }
        return render_template('P12.html', output=result)
    
    return render_template('P12.html', output=None)

if __name__ == '__main__':
    app.run(debug=True, port=1012)
