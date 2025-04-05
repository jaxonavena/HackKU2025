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
    script_builder.setup()
    for HighLevelkey, HighLevelvalue in data.items():
        match HighLevelkey:
          case "system_packages":
            ## system packages 
            system_Data = {
                      "system_packages": HighLevelvalue,
            }
            script_builder.generate(system_Data)
          case "languages":
            ## for lang and version passing 
            for item in HighLevelvalue:
              
              script_builder.generate(item)
          
    
