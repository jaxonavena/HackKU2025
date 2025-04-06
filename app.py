from flask import Flask, request, jsonify
from flask_cors import CORS
from Shell_Scripting.Main import script_gen 

app = Flask(__name__)
CORS(app)

@app.route('/run', methods=['POST'])
def run():
    data = request.get_json()
    repo_url = data.get('repo_url', '')
    print(f"Received repo URL: {repo_url}")
    
    script_gen()
    pathToScript = "Shell_Scripting/setup.sh"

    return jsonify({"message": "Repo URL received", "repo_url": repo_url})

if __name__ == '__main__':
    app.run(debug=True)
