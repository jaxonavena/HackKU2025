

class command_gen:

    def __init__(self, dep, system=False, lang=False, req=False):
        if lang: 
            self.name = dep.get("name")
            self.version = dep.get("version")
            self.system = False
        elif system:
            self.dep = dep
            self.system = True
        elif req:
            self.req = True
            self.dep = dep
        
        


    def generate(self):
        with open("setup.sh", "w") as script:
            script.write("#!/bin/bash\n")
            script.write("echo 'Setting up your environment...'\n")

            ## probably a system package idk use apt get maybe 
            if self.system:
                for item in self.dep:
                    script.write(f"apt-get install -y {item}")
            elif self.lang:  
                pass
            elif self.req:
                pass


            