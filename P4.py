from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

def sequential_search(arr, target):
    steps = 0
    for i in range(len(arr)):
        steps += 1
        if arr[i] == target:
            return steps
    return steps


def divide_conquer_search(arr, target):
    steps = 0
    start = 0
    end = len(arr) - 1
    while start <= end:
        steps += 1
        mid = (start + end) // 2
        if arr[mid] == target:
            return steps
        elif arr[mid] < target:
            start = mid + 1
        else:
            end = mid - 1
    return steps

@app.route('/')
def home():
    return render_template('P4.html', results={})

@app.route('/submit', methods=['POST'])
def submit():
    elements = list(map(int, request.form['elements'].split(',')))
    seq_search_steps = []
    div_search_steps = []

    for elem in elements:
        elem_list = list(range(1, elem + 1)) 
        seq_search_steps.append(sequential_search(elem_list.copy(), elem))
        div_search_steps.append(divide_conquer_search(elem_list.copy(), elem))

    
    plt.figure()
    plt.plot(elements, seq_search_steps, label='Sequential Search')
    plt.plot(elements, div_search_steps, label='Divide and Conquer Search')
    plt.xlabel('Number of Elements')
    plt.ylabel('Steps Count')
    plt.title('Search Efficiency Comparison')
    plt.legend()

  
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    graph_url = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    
    employees = [
        {'employeeID': 'X001', 'name': 'John Doe', 'age': 48, 'salary': 85000, 'position': 'Sales Director', 'mobile_number': '8123456789', 'email': 'john.doe@example.com', 'department': 'Sales', 'address': '45 King St, New York'},
        {'employeeID': 'X002', 'name': 'Emily White', 'age': 30, 'salary': 70000, 'position': 'UI/UX Designer', 'mobile_number': '9234567890', 'email': 'emily.white@example.com', 'department': 'Design', 'address': '22 Maple Ave, Boston'},
        {'employeeID': 'X003', 'name': 'Ryan Smith', 'age': 42, 'salary': 92000, 'position': 'Backend Developer', 'mobile_number': '6345678901', 'email': 'ryan.smith@example.com', 'department': 'Development', 'address': '789 Elm St, San Francisco'},
        {'employeeID': 'X004', 'name': 'Sophia Brown', 'age': 37, 'salary': 78000, 'position': 'HR Specialist', 'mobile_number': '7456789012', 'email': 'sophia.brown@example.com', 'department': 'Human Resources', 'address': '456 Oak St, Seattle'},
        {'employeeID': 'X005', 'name': 'David Green', 'age': 51, 'salary': 97000, 'position': 'Network Engineer', 'mobile_number': '8567890123', 'email': 'david.green@example.com', 'department': 'IT', 'address': '987 Birch St, Austin'},
    ]

    
    def highest_paid_position(employees):
        return max(employees, key=lambda e: e['salary'])['position']

    def lowest_paid_employee(employees):
        return min(employees, key=lambda e: e['salary'])['name']

    def youngest_employee_contact(employees):
        return min(employees, key=lambda e: e['age'])['mobile_number']

    def oldest_employee_salary(employees):
        return max(employees, key=lambda e: e['age'])['salary']

    
    results = {
        'elements': elements,
        'seq_search_steps': seq_search_steps,
        'div_search_steps': div_search_steps,
        'employees': employees,
        'highest_paid_position': highest_paid_position(employees),
        'lowest_paid_employee': lowest_paid_employee(employees),
        'youngest_employee_contact': youngest_employee_contact(employees),
        'oldest_employee_salary': oldest_employee_salary(employees)
    }

    return render_template('P4.html', results=results, graph_url=graph_url)

if __name__ == '__main__':
    app.run(debug=True, port=4001)
