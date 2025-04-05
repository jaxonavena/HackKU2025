import json

class Parser:
  def __init__(self, payload):
    data = []

  def parse(self):
    with open('fixtures/deps.json') as f:
      data = json.load(f)

    dependencies = data["dependencies"]

    for dep in dependencies:
      print(dep)