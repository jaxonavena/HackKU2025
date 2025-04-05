import json
import Parser from Parser

## Add code for receiveing json file and replace this hard coded input
file = pass
# with open("{file}}.json", "r") as dependencies_file:
#     deps = json.load(dependencies_file)
parsed_data = Parser.parse(file)


with open("setup.sh", "w") as script:
    script.write("#!/bin/bash\n")
    script.write("echo 'Setting up your environment...'\n")


    ## pip

    ## npm

