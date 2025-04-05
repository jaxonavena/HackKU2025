import json
from Parser import Parser

## Add code for receiveing json file and replace this hard coded input

file = "../fixtures/start.json"

jimbo = Parser(file)

parsed_data = jimbo.parse()


# with open("setup.sh", "w") as script:
#     script.write("#!/bin/bash\n")
#     script.write("echo 'Setting up your environment...'\n")

