from flask import Flask, request, jsonify
import os
import subprocess

app = Flask(__name__)

# Define your GraphRAG root folder
RAG_ROOT = './ragtest'

# Route to handle text indexing
@app.route('/index', methods=['POST'])
def index_text():
    data = request.json
    text_content = data.get('text')

    if not text_content:
        return jsonify({"error": "No text provided"}), 400

    # Save the input text to the appropriate file
    os.makedirs(f'{RAG_ROOT}/input', exist_ok=True)
    with open(f'{RAG_ROOT}/input/input_text.txt', 'w') as f:
        f.write(text_content)

    # Run the GraphRAG indexing process
    try:
        subprocess.run(['python', '-m', 'graphrag.index', '--root', RAG_ROOT], check=True)
        return jsonify({"message": "Text indexed successfully"}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"error": str(e)}), 500

# Route to handle text querying
@app.route('/query', methods=['POST'])
def query_text():
    data = request.json
    query = data.get('query')
    method = data.get('method', 'global')  # Default to global method

    if not query:
        return jsonify({"error": "No query provided"}), 400

    try:
        # Run the GraphRAG query process
        result = subprocess.run(
            ['python', '-m', 'graphrag.query', '--root', RAG_ROOT, '--method', method, query],
            capture_output=True, text=True, check=True
        )
        return jsonify({"result": result.stdout}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)