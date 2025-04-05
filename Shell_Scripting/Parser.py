import json
from command_gen import command_gen

class Parser:
  def __init__(self, file):
    self.file = file
    self.data = []

  def parse(self):
    with open(self.file, "r") as f:
      data = json.load(f)


    for HighLevelkey, HighLevelvalue in data.items():
        print(f"\n=== {HighLevelkey.upper()} ===")
        match HighLevelkey:
          case "system_packages":
                        ## system packages 

            # print(f"- {item}")
            command_gen.generate(HighLevelvalue, system=True)

          case "languages":

            ## if the entry is a list, meaning only have 
            if isinstance(HighLevelvalue, list):
                for item in HighLevelvalue:
                    if isinstance(item, dict):
                        for sub_key, sub_value in item.items():
                            print(f"{sub_key}: {sub_value}")
                            if sub_key == "packages":
                              
                              
                            command_gen.generate(HighLevelvalue.items())
                    else:
                      ## system packages 
                      if HighLevelkey == "system_packages":
                        print(f"- {item}")
                        command_gen.generate(item, system=True)
            case


        # elif isinstance(HighLevelvalue, dict):
        #     for sub_key, sub_value in HighLevelvalue.items():
        #         print(f"{sub_key}: {sub_value}")
        #         ## create the command 
        #         command_gen(HighLevelvalue.items())


        else:
            print(f"{value}")
            
    command = data["test"]
    print(command)
    
