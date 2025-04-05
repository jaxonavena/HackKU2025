import json
from Parser import Parser
import os


## Add code for receiveing json file and replace this hard coded input
def main():
    file = "../examples/big-deps.json"

    jimbo = Parser(file)

    jimbo.parse()

def clean_up():
    file_path = "setup.sh"

    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Deleted {file_path}")
    else:
        print(f"{file_path} not found.")


if __name__ == "__main__":
    main()