import json

class Parser:
  def __init__(self, file):
    self.file = file
    self.data = []

  def parse(self):
    with open(self.file, "r") as f:
      data = json.load(f)

    command = data["test"]
    print(command)
    # for dep in dependencies:
    #   print(dep)