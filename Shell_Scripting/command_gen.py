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

  def setup(self):
    with open("setup.sh", "w") as script:
      script.write("#!/bin/bash\n")
      script.write("echo 'Setting up your environment...'\n")
      script.write("sudo apt-get update\n")

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
          script.write(f"sudo apt-get install -y {name}\n")
          command = CommandGen.INSTALL_COMMANDS[name]

        for pack in packs:
          command += f" {pack}"
        command += "\n"
        script.write(command)

