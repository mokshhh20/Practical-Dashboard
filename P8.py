from flask import Flask, render_template, request

app = Flask(__name__)

def lcs(string1, string2):
    m = len(string1)
    n = len(string2)
    
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if string1[i - 1] == string2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    lcs_str = []
    i, j = m, n
    while i > 0 and j > 0:
        if string1[i - 1] == string2[j - 1]:
            lcs_str.append(string1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    lcs_str.reverse()

    return dp, ''.join(lcs_str)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        string1 = request.form['string1'].split(',')
        string2 = request.form['string2'].split(',')
        
        dp_table, lcs_result = lcs(string1, string2)
        
        indexed_dp_table = [(i, row) for i, row in enumerate(dp_table)]
        
        return render_template('P8.html', dp_table=indexed_dp_table, string1=string1, string2=string2, lcs_result=lcs_result)
    
    return render_template('P8.html')

if __name__ == '__main__':
    app.run(debug=True, port=8001)
