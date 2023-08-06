from functions import Functions

functions = Functions(False)

class User:

    def __init__(self, projectname: str, commands: list, intro: bool = True, clearonstart: bool = True):
        if clearonstart:
            functions.clear()
        if intro:
            print("|USER.PY| this program uses user.py by drooler (https://drooler.tk/)")
        functions.write(f"Welcome to {projectname}")
        username = functions.ask("Create a username:")
        functions.clear()
        self.username = username
        self.commands = commands
        self.level = 0
        self.money = 0

    def update_stats(self, level: int = 0, money: int = 0):
        self.level += level
        self.money += money
    
    def command(self):
        functions.clear()
        functions.write(f"Commands: {' '.join(self.commands)}")
        answer = input("> ")
        functions.clear()
        if answer.lower() in self.commands:
            return answer.lower()
        else:
            functions.write(f'"{answer}" is not a valid command')
            return
        
    def __str__(self):
        return f"{self.username}\n{'-' * (len(self.username) + 1)}\nLevel: {self.level}\nMoney: {self.money}"