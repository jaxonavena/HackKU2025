class CommandGen:
  INSTALL_COMMANDS = {
    "python": "-m pip install",
    "node": "npm install",
    "ruby": "gem install",
    "java": "mvn install",
    "c": "sudo apt-get install",
    "cpp": "sudo apt-get install",
    "rust": "cargo install",
    "go": "go get"
  }

  FULLNAMES = {
    "python": "python",
    "node": "nodejs npm",
    "ruby": "ruby",
    "java": "java",
    "c": "gcc g++",
    "cpp": "gcc g++",
    "rust": "rust",
    "go": "golang"
  }
    
  def setup(self):
    with open("./DockerBuilder/setup.sh", "w") as script:
      script.write("#!/bin/bash\n")
      script.write("echo 'Setting up your environment...'\n")
      script.write("sudo apt-get update\n")
      script.write("apt-get install -y cmake g++ pkg-config libjson-c-dev libwebsockets-dev git make\n")
      script.write("git clone https://github.com/tsl0922/ttyd.git /tmp/ttyd\n")
      script.write("cd /tmp/ttyd\n")
      script.write("mkdir build && cd build\n")
      script.write("cmake ..\n")
      script.write("make && make install\n")

  def generate(self, dep):
    system_packages = dep.get("system_packages")
    name = dep.get("name")
    version = dep.get("version")
    packs = dep.get("packages")

    with open("./DockerBuilder/setup.sh", "a") as script:
      if system_packages:
        for item in system_packages:
          script.write(f"sudo apt-get install -y {item}\n")

      elif name and version:
        if name == "python":
          interp = f"{name}{version} "
          script.write(f"sudo apt-get install -y {interp}\n")
          command = f"{interp}{CommandGen.INSTALL_COMMANDS[name]}"
        else:
          script.write(f"sudo apt-get install -y {CommandGen.FULLNAMES[name]}\n")
          command = CommandGen.INSTALL_COMMANDS[name]

        for pack in packs:
          command += f" {pack}"
        command += "\n"
        script.write(command)

# FROM python:3.10-slim
# WORKDIR /app
# COPY repo/ /app/
# COPY setup.sh /app/setup.sh
# RUN chmod +x /app/setup.sh && /app/setup.sh
# EXPOSE 8080
# CMD ["ttyd", "--writable", "-p", "8080", "bash"]

