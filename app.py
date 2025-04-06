from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sys
import os
import traceback

from DockerBuilder.imageBuilder import generate_dockerfile, build_docker_image
from DockerBuilder.deploymentManger import push_image_to_acr, deploy_to_azure_from_acr
import uuid
import time
app = Flask(__name__)
CORS(app)  # This must also come after app is defined

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run():
    data = request.get_json()
    repo_url = data.get('repo_url', '')
    print(f"Received repo URL: {repo_url}")

    try:
        # 1. Analyze and generate install_deps.sh
        scan_repo(repo_url)
        script_gen()

        # 2. Generate Dockerfile
        path = os.path.dirname(os.path.abspath(__file__)) + "/DockerBuilder"
        generate_dockerfile(path)

        # 3. Build Docker image
        unique_id = uuid.uuid4().hex[:6]
        image_tag = f"cli-runner:{unique_id}"
        image = build_docker_image(path, image_tag)

        # 4. Push to ACR
        acr_server = "clirunnerregistry.azurecr.io"
        acr_username = "clirunnerregistry"
        acr_password = "1zzlku2RHy5s3X1Do82HYThS7MM6DMgeLMke33qopk+ACRANFJhc"  # Replace or use env variable

        full_image_tag = push_image_to_acr(image, acr_server, "cli-runner")

        # 5. Deploy to Azure
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

        # 6. Wait for Azure to assign the public IP (or add a polling function)
        public_ip = f"http://{dns_label}.eastus.azurecontainer.io:8080"
        time.sleep(10)  # Allow a bit of time for provisioning

        # 7. Read the shell script
        with open(os.path.join(path, "install_deps.sh")) as f:
            shell_script = f.read()

        return jsonify({
            "status": "success",
            "shell_script": shell_script,
            "dependencies": {},  # Optional: return parsed deps here
            "ttyd_url": public_ip
        })

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)