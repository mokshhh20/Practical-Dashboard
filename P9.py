from flask import Flask, render_template, request

app = Flask(__name__)

def fractional_knapsack(profits, weights, capacity):
    ratio = [(profits[i] / weights[i], i) for i in range(len(profits))]
    ratio.sort(reverse=True, key=lambda x: x[0])

    total_profit = 0
    selected_items = [0] * len(profits) 
    ratios = [profits[i] / weights[i] for i in range(len(profits))] 

    for r, i in ratio:
        if weights[i] <= capacity:
            selected_items[i] = 1
            total_profit += profits[i]
            capacity -= weights[i]
        else:
            fraction = capacity / weights[i]
            selected_items[i] = fraction
            total_profit += profits[i] * fraction
            break 

    return selected_items, total_profit, ratios

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            profits = list(map(float, request.form.get('profits').split(',')))
            weights = list(map(float, request.form.get('weights').split(',')))
            capacity = float(request.form.get('capacity'))
            
            selected_items, total_profit, ratios = fractional_knapsack(profits, weights, capacity)

            return render_template('P9.html', selected_items=selected_items, total_profit=total_profit, profits=profits, weights=weights, ratios=ratios, capacity=capacity)
        except:
            return "Please provide valid inputs."

    return render_template('P9.html', selected_items=None)

if __name__ == '__main__':
    app.run(debug=True, port=9001)
