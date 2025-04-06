import subprocess
import time
def push_image_to_dockerhub(image, dockerhub_user, repo_name):
    tag = f"{dockerhub_user}/{repo_name}:latest"
    
    print(f"Tagging image as: {tag}")
    image.tag(tag)

    print(f"Pushing image to Docker Hub: {tag}")
    result = subprocess.run(["docker", "push", tag], capture_output=True, text=True)

    if result.returncode == 0:
        print("Docker image pushed successfully.")
        time.sleep(60)
        return tag
    else:
        print("Docker push failed.")
        print(result.stderr)
        return None

def push_image_to_acr(image, acr_login_server, repo_name):
    acr_image_tag = f"{acr_login_server}/{repo_name}:latest"
    
    print(f"🔁 Tagging image as: {acr_image_tag}")
    image.tag(acr_image_tag)

    print(f"📤 Pushing image to ACR: {acr_image_tag}")
    result = subprocess.run(["docker", "push", acr_image_tag], capture_output=True, text=True)

    if result.returncode == 0:
        print("✅ Image pushed to ACR successfully.")
        return acr_image_tag
    else:
        print("❌ Failed to push image to ACR:")
        print(result.stderr)
        return None

def deploy_to_azure(image_tag, resource_group, container_name, dns_label=None, port=None, location="eastus"):

    print("🔄 Ensuring Microsoft.ContainerInstance is registered...")
    subprocess.run([
        "az", "provider", "register",
        "--namespace", "Microsoft.ContainerInstance"
    ], check=True)

    print("Creating Azure resource group")
    subprocess.run([
        "az", "group", "create",
        "--name", resource_group,
        "--location", location
    ], check=True)

    print("🚀 Deploying container to Azure...")

    cmd = [
        "az", "container", "create",
        "--resource-group", resource_group,
        "--name", container_name,
        "--image", image_tag,
        "--cpu", "1",
        "--memory", "1",
        "--restart-policy", "Never",
        "--os-type", "Linux"
    ]

    if port:
        cmd += ["--ports", str(port), "--ip-address", "Public"]

    if dns_label:
        cmd += ["--dns-name-label", dns_label]

    subprocess.run(cmd, check=True)
    print("Azure container created.")

def deploy_to_azure_from_acr(image_tag, resource_group, container_name, acr_server, acr_username, acr_password, dns_label, port, location="eastus"):
    print("🔄 Ensuring Microsoft.ContainerInstance is registered...")
    subprocess.run(["az", "provider", "register", "--namespace", "Microsoft.ContainerInstance"], check=True)

    print("🛠 Creating Azure resource group...")
    subprocess.run(["az", "group", "create", "--name", resource_group, "--location", location], check=True)

    print("🚀 Deploying container to Azure from ACR...")

    cmd = [
        "az", "container", "create",
        "--resource-group", resource_group,
        "--name", container_name,
        "--image", image_tag,
        "--registry-login-server", acr_server,
        "--registry-username", acr_username,
        "--registry-password", acr_password,
        "--cpu", "1",
        "--memory", "1",
        "--restart-policy", "Never",
        "--os-type", "Linux",
    ]

    if port:
        cmd += ["--ports", "8080", "--ip-address", "Public"]

    if dns_label:
        cmd += ["--dns-name-label", dns_label]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print("✅ Container deployed successfully!")
    else:
        print("❌ Deployment failed:")
        print(result.stderr)
