from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import base64
import io
import time

app = Flask(__name__)

def min_coins(value, coins=[1, 4, 6]):
    dp = [float('inf')] * (value + 1)
    dp[0] = 0
    coin_count = [[0, 0, 0] for _ in range(value + 1)] 

    for i in range(1, value + 1):
        for j, coin in enumerate(coins):
            if i - coin >= 0 and dp[i - coin] + 1 < dp[i]:
                dp[i] = dp[i - coin] + 1
                coin_count[i] = coin_count[i - coin][:]  
                coin_count[i][j] += 1  

    return dp[value], coin_count[value]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        values_str = request.form.get("values")
        values = list(map(int, values_str.split(',')))
        results = []
        times = []

        for value in values:
            start_time = time.time()  
            min_count, coins_used = min_coins(value)
            elapsed_time = time.time() - start_time  
            results.append({"value": value, "coins_used": coins_used, "total_coins": min_count})
            times.append(elapsed_time)

        
        fig, ax = plt.subplots()
        ax.plot(values, times, marker='o', color='b', label='Time Taken (s)')
        ax.set_xlabel('Value (Rs)')
        ax.set_ylabel('Time (seconds)')
        ax.set_title('Time vs Value Analysis')
        ax.legend()

        
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()

        return render_template("P5.html", results=results, plot_url=plot_url)

    return render_template("P5.html", results=None)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
