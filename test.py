from HackKU2025.imageBuilder import generate_dockerfile, build_docker_image
from HackKU2025.deploymentManger import push_image_to_acr, deploy_to_azure_from_acr
import uuid
import os
def test_generate_dockerfile():
    abs_file_path = os.path.realpath(__file__)
    path = os.path.dirname(abs_file_path)

    print("Step 1 === Generating Dockerfile ===")
    generate_dockerfile(path)

    dockerfile_path = os.path.join(path, "Dockerfile")

    if os.path.exists(dockerfile_path):
        print(f"Dockerfile generated succesfully at {dockerfile_path}")
    else:
        print("Dockerfile was not generated")

    unique_id = uuid.uuid4().hex[:6]
    image_tag = f"cli-runner-test:{unique_id}"

    print("Step 2 === Generating Docker image tagged '{image_tag}' ===")
    image = build_docker_image(path, image_tag)

    if image:
        print(f"Docker image built successfully! Image ID: {image.id}")
    else:
        print("Docker build failed.")

    acr_server = "clirunnerregistry.azurecr.io"
    repo_name = "cli-runner"
    acr_username = "clirunnerregistry"             
    acr_password = "1zzlku2RHy5s3X1Do82HYThS7MM6DMgeLMke33qopk+ACRANFJhc"

    print("=== STEP 3: Push to Docker Hub ===")
    image_tag = push_image_to_acr(image, acr_server, repo_name)

    if image_tag:
        print(f"Image has been published to docker hub {image_tag}")
    else:
        print("Failed when publishing image to docker hub")

    print("=== STEP 4: Deploy to Azure ===")
    deploy_to_azure_from_acr(
        image_tag,
        resource_group="HackathonRG",
        container_name="cli-runner-deploy",
        acr_server=acr_server,
        acr_username=acr_username,
        acr_password=acr_password,
        dns_label="acrclirunnerdemo",
        port=8080
    )


if __name__ == "__main__":
    test_generate_dockerfile()