import json
from command_gen import CommandGen

class Parser:
  def __init__(self, file):
    self.file = file
    self.data = []

  def parse(self):
    with open(self.file, "r") as f:
      data = json.load(f)

    script_builder = CommandGen()
    for HighLevelkey, HighLevelvalue in data.items():
        match HighLevelkey:
          case "system_packages":
            ## system packages 
            system_Data = {
                      "system_packages": HighLevelvalue,
                      "type": "system"
            }
            script_builder.setup(system_Data)
            script_builder.generate()
          case "languages":
            ## for lang and version passing 
            for item in HighLevelvalue:
              script_builder.setup(item)
              script_builder.generate()
          
    
