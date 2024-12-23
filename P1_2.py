from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('P1_2.html')

@app.route('/find', methods=['POST'])
def find():
    numbers = request.form['numbers']
    numbers_list = list(map(int, numbers.split(',')))
    
    def closest_sums_to_zero(arr):
        min_sum = float('inf')
        pairs = []
        
        for i in range(len(arr)):
            for j in range(i + 1, len(arr)):
                current_sum = arr[i] + arr[j]
                if abs(current_sum) < abs(min_sum):
                    min_sum = current_sum
                    pairs = [(arr[i], arr[j])]
                elif abs(current_sum) == abs(min_sum):
                    pairs.append((arr[i], arr[j]))
        
        return pairs
    
    result_pairs = closest_sums_to_zero(numbers_list)
    return render_template('P1_2.html', result=result_pairs)

if __name__ == '__main__':
    app.run(debug=True, port=1002)
