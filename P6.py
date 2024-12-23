from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_matrix_chain_order(dimensions):
    n = len(dimensions) - 1
    m = [[0 for _ in range(n)] for _ in range(n)]
    s = [[0 for _ in range(n)] for _ in range(n)]

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            m[i][j] = float('inf')
            for k in range(i, j):
                q = m[i][k] + m[k + 1][j] + dimensions[i] * dimensions[k + 1] * dimensions[j + 1]
                if q < m[i][j]:
                    m[i][j] = q
                    s[i][j] = k

    return m, s

def get_optimal_parenthesization(s, i, j):
    if i == j:
        return f"A{i + 1}"
    else:
        k = s[i][j]
        left = get_optimal_parenthesization(s, i, k)
        right = get_optimal_parenthesization(s, k + 1, j)
        return f"({left} x {right})"

@app.route('/', methods=['GET', 'POST'])
def index():
    num_matrices = None
    min_operations = None
    optimal_parenthesization = None
    multiplication_table = None

    if request.method == 'POST':
    
        dimensions = list(map(int, request.form['dimensions'].replace(',', ' ').split()))
        num_matrices = len(dimensions) - 1

       
        m, s = calculate_matrix_chain_order(dimensions)
        optimal_parenthesization = get_optimal_parenthesization(s, 0, len(dimensions) - 2)
        min_operations = m[0][-1]

     
        multiplication_table = [['X' if cell == 0 else cell for cell in row] for row in m]

    return render_template('P6.html',
                           min_operations=min_operations,
                           optimal_parenthesization=optimal_parenthesization,
                           multiplication_table=multiplication_table,
                           num_matrices=num_matrices)

if __name__ == '__main__':
    app.run(debug=True, port=6001)
