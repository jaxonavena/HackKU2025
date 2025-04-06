from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sys
import os
import uuid
import traceback
from imageBuilder import generate_dockerfile, build_docker_image
from deploymentManger import push_image_to_acr, deploy_to_azure_from_acr
from Shell_Scripting.Main import script_gen

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
        repo_scanner.main(repo_url)
        # script_gen()

        # === STEP 2: Generate Dockerfile
        abs_file_path = os.path.realpath(__file__)
        path = os.path.dirname(abs_file_path)
        print("Step 1 === Generating Dockerfile ===")
        generate_dockerfile(path)

        dockerfile_path = os.path.join(path, "HackKU2025")
        # === STEP 3: Build Docker image
        unique_id = uuid.uuid4().hex[:6]
        image_tag = f"cli-runner-test:{unique_id}"
        image = build_docker_image(path, image_tag)
        print("Finished")
        # # === STEP 4: Push to ACR
        # acr_server = "clirunnerregistry.azurecr.io"
        # acr_username = "clirunnerregistry"
        # acr_password = "1zzlku2RHy5s3X1Do82HYThS7MM6DMgeLMke33qopk+ACRANFJhc"  # Consider using os.environ for secrets

        # full_image_tag = push_image_to_acr(image, acr_server, "cli-runner")

        # # === STEP 5: Deploy to Azure
        # container_name = f"cli-runner-deploy-{unique_id}"
        # dns_label = f"clirunnerdemo{unique_id}"
        # deploy_to_azure_from_acr(
        #     full_image_tag,
        #     resource_group="HackathonRG",
        #     container_name=container_name,
        #     acr_server=acr_server,
        #     acr_username=acr_username,
        #     acr_password=acr_password,
        #     dns_label=dns_label,
        #     port=8080
        # )

        # # === STEP 6: Wait a few seconds and return the public IP
        # public_ip = f"http://{dns_label}.eastus.azurecontainer.io:8080"

        # # === STEP 7: Return the generated shell script and terminal URL
        # with open(os.path.join(path, "install_deps.sh")) as f:
        #     shell_script = f.read()

        # return jsonify({
        #     "status": "success",
        #     "shell_script": shell_script,
        #     "dependencies": {},  # Add dependency JSON here if needed
        #     "ttyd_url": public_ip
        # })
        return jsonify({"status": "success"})

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001, extra_files=extra_files, use_reloader=False)
