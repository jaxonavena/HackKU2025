from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/run', methods=['POST'])
def run():
    data = request.get_json()
    repo_url = data.get('repo_url', '')
    print(f"Received repo URL: {repo_url}")
    
    # 1) Clone the repo
    # 2) Build Docker image
    # 3) etc.

    return jsonify({"message": "Repo URL received", "repo_url": repo_url})

if __name__ == '__main__':
    app.run(debug=True)
