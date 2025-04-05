import json
from Parser import Parser
import os


## Add code for receiveing json file and replace this hard coded input

file = "../fixtures/start.json"

jimbo = Parser(file)

parsed_data = jimbo.parse()


# with open("setup.sh", "w") as script:
#     script.write("#!/bin/bash\n")
#     script.write("echo 'Setting up your environment...'\n")


def clean_up():
    file_path = "setup.sh"

    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Deleted {file_path}")
    else:
        print(f"{file_path} not found.")


# if __name__ == "__main__":