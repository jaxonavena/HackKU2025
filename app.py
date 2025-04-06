from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sys
import os
import traceback
import uuid
import time
import importlib.util
import importlib.machinery

from DockerBuilder.imageBuilder import generate_dockerfile, build_docker_image
from DockerBuilder.deploymentManger import push_image_to_acr, deploy_to_azure_from_acr
from Shell_Scripting.Main import script_gen

# Load the repo_scanner module
loader = importlib.machinery.SourceFileLoader(
    'repo_scanner',
    os.path.join(os.path.dirname(__file__), 'dependency-parser', 'repo_scanner.py')
)
spec = importlib.util.spec_from_loader('repo_scanner', loader)
repo_scanner = importlib.util.module_from_spec(spec)
loader.exec_module(repo_scanner)

# Flask app setup
app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run():
    data = request.get_json(force=True)
    repo_url = data.get('repo_url', '')
    print(f"📦 Received repo URL: {repo_url}")

    try:
        # === STEP 1: Analyze and generate install_deps.sh
        repo_scanner.main(repo_url)
        script_gen()

        # === STEP 2: Generate Dockerfile
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "DockerBuilder")
        generate_dockerfile(path)

        # === STEP 3: Build Docker image
        unique_id = uuid.uuid4().hex[:6]
        image_tag = f"cli-runner:{unique_id}"
        image = build_docker_image(path, image_tag)

        # === STEP 4: Push to ACR
        acr_server = "clirunnerregistry.azurecr.io"
        acr_username = "clirunnerregistry"
        acr_password = "1zzlku2RHy5s3X1Do82HYThS7MM6DMgeLMke33qopk+ACRANFJhc"  # Consider using os.environ for secrets

        full_image_tag = push_image_to_acr(image, acr_server, "cli-runner")

        # === STEP 5: Deploy to Azure
        container_name = f"cli-runner-deploy-{unique_id}"
        dns_label = f"clirunnerdemo{unique_id}"
        deploy_to_azure_from_acr(
            full_image_tag,
            resource_group="HackathonRG",
            container_name=container_name,
            acr_server=acr_server,
            acr_username=acr_username,
            acr_password=acr_password,
            dns_label=dns_label,
            port=8080
        )

        # === STEP 6: Wait a few seconds and return the public IP
        public_ip = f"http://{dns_label}.eastus.azurecontainer.io:8080"
        time.sleep(10)

        # === STEP 7: Return the generated shell script and terminal URL
        with open(os.path.join(path, "install_deps.sh")) as f:
            shell_script = f.read()

        return jsonify({
            "status": "success",
            "shell_script": shell_script,
            "dependencies": {},  # Add dependency JSON here if needed
            "ttyd_url": public_ip
        })

    except Exception as e:
        print("❌ ERROR during deploy:", traceback.format_exc())
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)