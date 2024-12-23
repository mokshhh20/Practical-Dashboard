from flask import Flask, render_template
import matplotlib.pyplot as plt
import io
import base64
import time
import sys

app = Flask(__name__)

sys.setrecursionlimit(1500)

def calc_sum_using_loop(N):
    total = 0
    for num in range(1, N + 1):
        total += num
    return total

def sum_using_equation(N):
    return (N * (N + 1)) // 2

def recursion_sum(N):
    if N <= 1:
        return N
    else:
        return N + recursion_sum(N - 1)

def measure_time(func, N):
    start_time = time.time()
    try:
        func(N)
    except RecursionError:
        return None  
    end_time = time.time()
    return end_time - start_time

@app.route('/')
def index():
    N_values = [100, 500, 300, 800, 1500, 2000, 2500] 

    loop_times = [measure_time(calc_sum_using_loop, N) for N in N_values]
    equation_times = [measure_time(sum_using_equation, N) for N in N_values]
    recursion_times = [measure_time(recursion_sum, N) for N in N_values]

    plt.figure(figsize=(14, 7))
    plt.plot(N_values, loop_times, label='Loop', marker='o', color='r', linestyle='-')
    plt.plot(N_values, equation_times, label='Equation', marker='o', color='b', linestyle='-')
    plt.plot(N_values, recursion_times, label='Recursion', marker='o', color='g', linestyle='-')
    plt.xlabel('Input Size (N)')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Execution Time Comparison: Sum Calculation Methods')
    plt.legend()
    plt.grid(True)

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template('P2_1.html', plot_url=plot_url,
                           numbers=N_values,
                           loop_times=loop_times,
                           equation_times=equation_times,
                           recursion_times=recursion_times)

if __name__ == '__main__':
    app.run(debug=True, port=2001)
