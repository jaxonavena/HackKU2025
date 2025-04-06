class CommandGen:
  INSTALL_COMMANDS = {
    "python": "-m pip install",
    "node": "npm install",
    "ruby": "gem install",
    "java": "mvn install",
#     "rust": "cargo install",
#     "go": "go get",
#     "cpp": "apt-get install"
#   }

#   def setup(self):
#     """Initialize the shell script with setup commands"""
#     return "#!/bin/bash\n" + \
#            "echo 'Setting up your environment...'\n" + \
#            "sudo apt-get update\n"

#   def generate(self, dep):
#     """Generate installation commands for dependencies"""
#     script_content = ""
    
#     if dep.get("system_packages"):
#       for item in dep["system_packages"]:
#         script_content += f"sudo apt-get install -y {item}\n"
    
#     elif dep.get("name") and dep.get("version"):
#       interp = f"{dep.get('name')}{dep.get('version')}"
#       script_content += f"sudo apt-get install -y {interp}\n"
      
#       if dep.get("packages"):
#         command = f"{interp} {self.INSTALL_COMMANDS[dep.get('name')]}"
#         for pack in dep["packages"]:
#           command += f" {pack}"
#         command += "\n"
#         script_content += command
    
#     return script_content
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
    with open("setup.sh", "w") as script:
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

    with open("setup.sh", "a") as script:
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

