from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sys
import os
import traceback

# Import using importlib to handle the hyphenated directory name
import importlib.util
import importlib.machinery

# Get the path to the parent directory (your_project/)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from Shell_Scripting.Main import script_gen

# # Add the current directory to Python path
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load the repo_scanner module
loader = importlib.machinery.SourceFileLoader(
    'repo_scanner',
    os.path.join(os.path.dirname(__file__), 'dependency-parser', 'repo_scanner.py')
)
spec = importlib.util.spec_from_loader('repo_scanner', loader)
repo_scanner = importlib.util.module_from_spec(spec)
loader.exec_module(repo_scanner)
scan_repo = repo_scanner.main

app = Flask(__name__)
CORS(app)

# Configure Flask to ignore the repo directory for reloading
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
extra_files = []
for root, dirs, files in os.walk("."):
    if "dependency-parser/repo" in root:
        continue
    for filename in files:
        extra_files.append(os.path.join(root, filename))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run():
    data = request.get_json()
    repo_url = data.get('repo_url', '')
    print(f"Received repo URL: {repo_url}")

    try:
        # Run repo scanner to get dependencies JSON
        scan_repo(repo_url)
        script_gen()
        return jsonify({"status": "success"})

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001, extra_files=extra_files)
