import os, sys, time

class Functions:

    def __init__(self, intro: bool = True):
        if intro:
            print("|FUNCTIONS.PY| this program uses functions.py by drooler (https://drooler.tk/)")
        
    def clear(self):
        os.system("cls")
    
    def pause(self, delay: str = 0.02):
        time.sleep(delay)

    def write(self, text: str, delay: int = 0.02, newline: bool = True):
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            self.pause(delay)
        if newline:
            print()
    
    def ask(self, text: str):
        self.write(f"{text} ", newline = False)
        return input()
    
