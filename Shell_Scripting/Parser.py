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

            if HighLevelkey == "system_packages":
                    system_data = {
                        "system_packages": HighLevelvalue,
                    }
                    script_builder.generate(system_data)
            elif HighLevelkey == "languages":
                    for item in HighLevelvalue:
                        script_builder.generate(item)
                        
        script_builder.script_end()



