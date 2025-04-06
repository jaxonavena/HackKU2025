from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import using importlib to handle the hyphenated directory name
import importlib.util
import importlib.machinery

# Load the repo_scanner module
loader = importlib.machinery.SourceFileLoader(
    'repo_scanner',
    os.path.join(os.path.dirname(__file__), 'dependency-parser', 'repo_scanner.py')
)
spec = importlib.util.spec_from_loader('repo_scanner', loader)
repo_scanner = importlib.util.module_from_spec(spec)
loader.exec_module(repo_scanner)
scan_repo = repo_scanner.main

from Shell_Scripting.Main import main as generate_shell_script

app = Flask(__name__)
CORS(app)

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
        scan_result = scan_repo(repo_url)
        
        # Pass the JSON to shell script generator
        script_content = generate_shell_script(scan_result)
        
        return jsonify({
            "status": "success",
            "message": "Repository processed successfully",
            "dependencies": scan_result,
            "shell_script": script_content
        })
    except Exception as e:
        print(f"Error processing repository: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
