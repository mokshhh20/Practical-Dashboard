from flask import Flask, render_template, request
import heapq

app = Flask(__name__)

class HuffmanNode:
    def __init__(self, symbol, frequency):
        self.symbol = symbol
        self.frequency = frequency
        self.left_child = None
        self.right_child = None

    def __lt__(self, other):
        if self.frequency == other.frequency:
            return (self.symbol or '') < (other.symbol or '')
        return self.frequency < other.frequency

def build_huffman_tree(frequency_table):
    min_heap = [HuffmanNode(symbol, freq) for symbol, freq in frequency_table.items()]
    heapq.heapify(min_heap)
    
    while len(min_heap) > 1:
        left_node = heapq.heappop(min_heap)
        right_node = heapq.heappop(min_heap)
        
        merged_node = HuffmanNode(None, left_node.frequency + right_node.frequency)
        merged_node.left_child = left_node
        merged_node.right_child = right_node
        
        heapq.heappush(min_heap, merged_node)
    
    return min_heap[0]

def generate_codes(node, current_code="", code_dict={}):
    if node is None:
        return
    
    if node.symbol is not None:
        code_dict[node.symbol] = current_code
    else:
        generate_codes(node.left_child, current_code + "0", code_dict)
        generate_codes(node.right_child, current_code + "1", code_dict)
    
    return code_dict

def encode_text(input_text, code_dict):
    return ''.join(code_dict.get(char, '') for char in input_text)

def decode_binary(binary_data, root_node):
    decoded_text = []
    current_node = root_node
    
    for bit in binary_data:
        current_node = current_node.left_child if bit == '0' else current_node.right_child
        
        if current_node.symbol is not None:
            decoded_text.append(current_node.symbol)
            current_node = root_node
    
    return ''.join(decoded_text)

frequency_table = {'A': 0.5, 'B': 0.35, 'C': 0.5, 'D': 0.1, 'E': 0.4, '-': 0.2}

root_node = build_huffman_tree(frequency_table)
code_dict = generate_codes(root_node)

@app.route("/", methods=["GET", "POST"])
def index():
    result_text = ""
    input_text = ""
    
    if request.method == "POST":
        input_text = request.form.get("input_text")
        operation = request.form.get("operation")
        
        if operation == "encode":
            result_text = encode_text(input_text, code_dict)
        elif operation == "decode":
            result_text = decode_binary(input_text, root_node)
    
    return render_template("index.html", result=result_text, input_text=input_text)

if __name__ == "__main__":
    app.run(debug=True, port=1010)
