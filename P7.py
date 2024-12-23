from flask import Flask, render_template, request

app = Flask(__name__)

def solve_knapsack(max_capacity, num_items, profits, weights):
   
    dp_table = [[0 for _ in range(max_capacity + 1)] for _ in range(num_items + 1)]

    for item in range(1, num_items + 1):
        for capacity in range(1, max_capacity + 1):
            if weights[item - 1] <= capacity:
                dp_table[item][capacity] = max(
                    profits[item - 1] + dp_table[item - 1][capacity - weights[item - 1]],
                    dp_table[item - 1][capacity]
                )
            else:
                dp_table[item][capacity] = dp_table[item - 1][capacity]

   
    selected_items = [0] * num_items
    remaining_capacity = max_capacity
    for item in range(num_items, 0, -1):
        if dp_table[item][remaining_capacity] != dp_table[item - 1][remaining_capacity]:
            selected_items[item - 1] = 1
            remaining_capacity -= weights[item - 1]

    return dp_table, selected_items

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
    
        max_capacity = int(request.form["capacity"])
        num_items = int(request.form["items"])
        profits = list(map(int, request.form["profits"].split(',')))
        weights = list(map(int, request.form["weights"].split(',')))

        dp_table, selected_items = solve_knapsack(max_capacity, num_items, profits, weights)

        return render_template(
            "P7.html",
            dp_table=dp_table,
            selected_items=selected_items,
            num_items=num_items,
            max_capacity=max_capacity,
            show_table=True
        )

    return render_template("P7.html", show_table=False)

if __name__ == "__main__":
    app.run(debug=True, port=7001)
