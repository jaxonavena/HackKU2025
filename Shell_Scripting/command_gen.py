class CommandGen:
  INSTALL_COMMANDS = {
    "python": "-m pip install",
    "node": "npm install",
    "ruby": "gem install",
    "java": "mvn install"
  }

  def setup(self):
    with open("setup.sh", "w") as script:
      script.write("#!/bin/bash\n")
      script.write("echo 'Setting up your environment...'\n")
      script.write("sudo apt-get update\n")

  def generate(self, dep):
    with open("setup.sh", "a") as script:
      if dep.get("system_packages"):
        for item in dep:
          script.write(f"sudo apt-get install -y {item}\n")

      elif dep.get("name") and dep.get("version"):
        interp = f"{dep.get("name")}{dep.get("version")}"
        script.write(f"sudo apt-get install -y {interp}\n")

        packs = dep.get("packages")
        command = f"{interp} {CommandGen.INSTALL_COMMANDS[dep.get("name")]}"

        for pack in packs:
          command += f" {pack}"
        command += "\n"
        print(command)
        script.write(command)

