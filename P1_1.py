from flask import Flask,render_template,request

app = Flask(__name__)

def compare_ratings(a,b):
    chef1_pts = 0
    chef2_pts = 0

    for i in range(3):
        if a[i] > b[i]:
            chef1_pts+=1
        elif a[i] < b[i]:
            chef2_pts+=1
        elif a[i] == b[i]:
            chef1_pts+=1
            chef2_pts+=1

    return chef1_pts,chef2_pts

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        try:
            a = []
            b = []
            for i in range(3):
                a_value = request.form.get(f'a{i}')
                b_value = request.form.get(f'b{i}')
                
                if a_value is None or b_value is None or a_value == '' or b_value == '':
                    raise ValueError("Input cannot be empty")

                a_value = int(a_value)
                b_value = int(b_value)

                if not (0 <= a_value <= 100 and 0 <= b_value <= 100):
                    raise ValueError("Inputs must be between 0 and 100")

                a.append(a_value)
                b.append(b_value)
            
            chef1_pts, chef2_pts = compare_ratings(a, b)
            return render_template('P1_1.html', chef1_pts=chef1_pts, chef2_pts=chef2_pts)
        except ValueError as e:
            return f"Error: {str(e)}", 400

    return render_template('P1_1.html', chef1_pts=None, chef2_pts=None)

if __name__ == '__main__':
    app.run(debug=True, port=1001)