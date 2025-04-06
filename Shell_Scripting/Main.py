import json
import os
import sys

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from Parser import Parser

## Add code for receiveing json file and replace this hard coded input
def script_gen():
    file = "../examples/big-deps.json"

    jimbo = Parser(file)
    jimbo.parse()

# def main(json_data=None):
#     """
#     Process dependencies and generate shell script.
#     Args:
#         json_data: Dictionary containing dependency data. If None, reads from default file.
#     Returns:
#         str: Generated shell script content
#     """
#     if json_data is None:
#         # Fallback to file if no JSON data provided
#         file = "../examples/dependency.json"
#         with open(file, 'r') as f:
#             json_data = json.load(f)

#     parser = Parser(json_data)
#     script_content = parser.parse()
    
#     # Write to file and return content
#     with open("setup.sh", "w") as f:
#         f.write(script_content)
    
#     return script_content

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