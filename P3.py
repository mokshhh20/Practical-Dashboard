from flask import Flask, render_template, request
import time
import matplotlib.pyplot as plt
import io
import base64
import random

app = Flask(__name__)

def bubble_sort(arr):
    n = len(arr)
    start_time = time.time()
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    end_time = time.time()
    return end_time - start_time

def insertion_sort(arr):
    n = len(arr)
    start_time = time.time()
    for i in range(1, n):
        key = arr[i]
        j = i-1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
    end_time = time.time()
    return end_time - start_time

def selection_sort(arr):
    n = len(arr)
    start_time = time.time()
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    end_time = time.time()
    return end_time - start_time

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.form['data']
        arr = list(map(int, data.split(',')))

        time_bubble = bubble_sort(arr.copy())
        time_insertion = insertion_sort(arr.copy())
        time_selection = selection_sort(arr.copy())

        complexities = {
            'Bubble Sort': {'Best': 'O(n)', 'Average': 'O(n^2)', 'Worst': 'O(n^2)'},
            'Insertion Sort': {'Best': 'O(n)', 'Average': 'O(n^2)', 'Worst': 'O(n^2)'},
            'Selection Sort': {'Best': 'O(n^2)', 'Average': 'O(n^2)', 'Worst': 'O(n^2)'}
        }

        list_sizes = [10, 50, 100, 500, 1000]
        bubble_times = []
        insertion_times = []
        selection_times = []

        for n in list_sizes:
            test_arr = [random.randint(1, 1000) for _ in range(n)]
            bubble_times.append(bubble_sort(test_arr.copy()))
            insertion_times.append(insertion_sort(test_arr.copy()))
            selection_times.append(selection_sort(test_arr.copy()))

        plt.figure(figsize=(10, 6))
        plt.plot(list_sizes, bubble_times, label='Bubble Sort', marker='o', color='green')
        plt.plot(list_sizes, insertion_times, label='Insertion Sort', marker='o', color='blue')
        plt.plot(list_sizes, selection_times, label='Selection Sort', marker='o', color='red')

        plt.xlabel('List Size (n)')
        plt.ylabel('Time Taken (seconds)')
        plt.title('Sorting Algorithm Time Complexity Comparison')
        plt.legend()

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        graph_url = base64.b64encode(img.getvalue()).decode()

        return render_template('P3.html', complexities=complexities, graph_url=graph_url)

    return render_template('P3.html')

if __name__ == '__main__':
    app.run(debug=True, port=3001)
