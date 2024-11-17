import networkx as nx
import matplotlib.pyplot as plt
import re
import base64
import io
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/validate', methods=['POST'])
def validate():
    expression = request.json.get('expression')
    is_valid, components = validate_expression_format(expression)
    
    if is_valid:
        img_path = create_syntax_tree(expression, components)
        return {"valid": True, "image_url": f"/static/{img_path}"}
    return {"valid": False, "message": "Expresión no válida"}

def validate_expression_format(expression):
    match = re.fullmatch(r'^\d+(\.\d+)?\s*[\+\-\*/]\s*\d+(\.\d+)?$', expression)
    if match:
        operator_position = re.search(r'[\+\-\*/]', expression).start()
        operand1 = expression[:operator_position].strip()
        operator = expression[operator_position]
        operand2 = expression[operator_position + 1:].strip()
        return True, (operand1, operator, operand2)
    return False, None


def create_syntax_tree(expression, components):
    G = nx.DiGraph()
    
    operand1, operator, operand2 = components
    
    G.add_nodes_from(["S", "C", operator, "N1", "N2"])
    G.add_edge("S", "C")
    G.add_edge("C", "N1")
    G.add_edge("C", operator)
    G.add_edge("C", "N2")
    
    G.add_edge("N1", "D1")
    G.add_edge("N2", "D2")
    for i, digit in enumerate(operand1):
        G.add_node(f"D1_{i}", label=digit)
        G.add_edge("D1", f"D1_{i}")
    for i, digit in enumerate(operand2):
        G.add_node(f"D2_{i}", label=digit)
        G.add_edge("D2", f"D2_{i}")
    
    pos = nx.spring_layout(G)
    node_labels = {node: G.nodes[node].get('label', node) for node in G.nodes}
    colors = ["green" if node in ["S", "C", "N1", "N2"] else "yellow" for node in G.nodes]
    
    plt.figure(figsize=(6, 6))
    nx.draw(G, pos, with_labels=True, labels=node_labels, node_color=colors, node_size=1000, font_size=10, font_color="black")
    
    img_path = 'syntax_tree.png'
    plt.savefig(f'static/{img_path}', format='png')
    plt.close()
    return img_path

if __name__ == '__main__':
    app.run(debug=True)
