import json
import os
import sys

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from Parser import Parser

## Add code for receiveing json file and replace this hard coded input
def script_gen():
    file = "../dependency-parser/target.json"
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
    # main()
    script_gen()