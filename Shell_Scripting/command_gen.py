class CommandGen:
    INSTALL_COMMANDS = {
      "python": "-m pip install",
      "node": "npm install",
      "ruby": "gem install",
      "java": "mvn install"
    }

    def setup(self, dep):
      self.dep = dep
      self.type = self.dep["type"]
      self.interp = None

    def generate(self):
      with open("setup.sh", "w") as script:
        script.write("#!/bin/bash\n")
        script.write("echo 'Setting up your environment...'\n")

        script.write("sudo apt-get update\n")

        if self.dep["system_packages"]:
          for item in self.dep:
            script.write(f"sudo apt-get install -y {item}\n")

        elif self.dep["name"] and self.dep["version"]:
          self.interp = f"{self.dep["name"]}{self.dep["version"]}"
          script.write(f"sudo apt-get install -y {self.interp}")
          packs = self.dep["packages"]
          command = f"{self.interp} {CommandGen.INSTALL_COMMANDS[self.dep["name"]]}"

          # requests==2.25.1 flask==2.0.1
          for pack in packs:
            command += f" {pack}"
          command += "\n"
          script.write(command)

