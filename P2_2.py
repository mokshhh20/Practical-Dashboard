from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('P2_2.html')

@app.route('/submit', methods=['POST'])
def submit():
    num_list = list(map(int, request.form['months'].split(',')))
    
    iter_counts = []
    recur_counts = []
    rabbit_pairs = []

    for num in num_list:
        iter_count = 0
        a, b = 0, 1
        for i in range(num + 1):
            iter_count += 1
            if i == 0:
                pairs = 0
            elif i == 1:
                pairs = 1
            else:
                pairs = a + b
                a = b
                b = pairs
        iter_counts.append(iter_count)
        rabbit_pairs.append(pairs)

        def fibonacci_recursive(n, count=0):
            count += 1
            if n == 0:
                return 0, count
            elif n == 1:
                return 1, count
            else:
                fib_1, count = fibonacci_recursive(n-1, count)
                fib_2, count = fibonacci_recursive(n-2, count)
                return fib_1 + fib_2, count

        _, recur_count = fibonacci_recursive(num)
        recur_counts.append(recur_count)

    plt.figure()
    plt.plot(num_list, iter_counts, label='Iteration Method', marker='o')
    plt.plot(num_list, recur_counts, label='Recursive Method', marker='x')
    plt.xlabel('Months')
    plt.ylabel('Operation Count')
    plt.title('Iteration vs Recursive Method Complexity')
    plt.legend()

  
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    graph_url = base64.b64encode(buf.getvalue()).decode('utf8')

    results = {
        'months': num_list,
        'iter_counts': iter_counts,
        'recur_counts': recur_counts,
        'rabbit_pairs': rabbit_pairs
    }

    return render_template('P2_2.html', results=results, graph_url=graph_url)

if __name__ == '__main__':
    app.run(debug=True, port=2002)
