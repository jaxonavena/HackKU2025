import os
import docker

def generate_dockerfile(shell_scripting_path: str):
    dockerfile_path = os.path.join(shell_scripting_path, "Dockerfile")

    with open(dockerfile_path,"w") as f:
        f.write("FROM python:3.10-slim\n")
        f.write("WORKDIR /app\n")
        f.write("COPY repo/ /app/\n")
        f.write("COPY install_deps.sh /app/install_deps.sh\n")
        f.write("RUN chmod +x /app/install_deps.sh && /app/install_deps.sh\n")
        f.write("EXPOSE 8080\n") 
        f.write("""CMD ["ttyd", "--writable", "-p", "8080", "bash"]\n""")
    
    print(f"Dockerfile created at: {dockerfile_path}")

def build_docker_image(path, image_tag):
    print(f"Path received is {path}")
    client = docker.from_env()
    print(f"Building docker image '{image_tag}' from: {path}")

    image, logs = client.images.build(path=path, tag=image_tag, rm=True, nocache=True)
    return image