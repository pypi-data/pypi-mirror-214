import main
class MyCli(main.CMD):
    def __init__(self,commands):
        super().__init__()
        commands.update({"print":self.prin,"hello_world":self.hello_world,})
        print(commands)
    def prin(self,arg):
        print(arg[0])
    def hello_world(self):
        print("Hello World")
MyCli(main.commands).cmdloop()