import json
from command_gen import CommandGen

class Parser:
    def __init__(self, data):
        """
        Initialize Parser with either JSON data or file path
        Args:
            data: Either a dictionary containing dependency data or a file path
        """
        self.data = data if isinstance(data, dict) else None
        self.file = None if isinstance(data, dict) else data

    def parse(self):
        """
        Parse the dependency data and generate shell script
        Returns:
            str: Generated shell script content
        """
        if self.data is None:
            with open(self.file, "r") as f:
                self.data = json.load(f)

        script_builder = CommandGen()
        script_content = script_builder.setup()
        
        for HighLevelkey, HighLevelvalue in self.data.items():
            match HighLevelkey:
                case "system_packages":
                    system_data = {
                        "system_packages": HighLevelvalue,
                    }
                    script_content += script_builder.generate(system_data)
                case "languages":
                    for item in HighLevelvalue:
                        script_content += script_builder.generate(item)
        
        return script_content

    
