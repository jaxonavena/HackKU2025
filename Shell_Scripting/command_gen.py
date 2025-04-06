class CommandGen:
  INSTALL_COMMANDS = {
    "python": "-m pip install",
    "node": "npm install",
    "ruby": "gem install",
    "java": "mvn install",
    "rust": "cargo install",
    "go": "go get",
    "cpp": "apt-get install"
  }

  def setup(self):
    """Initialize the shell script with setup commands"""
    return "#!/bin/bash\n" + \
           "echo 'Setting up your environment...'\n" + \
           "sudo apt-get update\n"

  def generate(self, dep):
    """Generate installation commands for dependencies"""
    script_content = ""
    
    if dep.get("system_packages"):
      for item in dep["system_packages"]:
        script_content += f"sudo apt-get install -y {item}\n"
    
    elif dep.get("name") and dep.get("version"):
      interp = f"{dep.get('name')}{dep.get('version')}"
      script_content += f"sudo apt-get install -y {interp}\n"
      
      if dep.get("packages"):
        command = f"{interp} {self.INSTALL_COMMANDS[dep.get('name')]}"
        for pack in dep["packages"]:
          command += f" {pack}"
        command += "\n"
        script_content += command
    
    return script_content

