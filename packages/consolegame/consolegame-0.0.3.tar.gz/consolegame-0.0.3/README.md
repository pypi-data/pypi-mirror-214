# CONSOLE GAME

## For more info and the documentation visit https://console-game.drooler.tk/
&nbsp;
### How do I start:
1. Install the module, do this by running the following in cmd or shell: ```pip install console-game```.
2. Import the module, do this by adding the following at the top of your your python file ```import console-game```.
3. Initialize the user in the module do this by adding the following in the code after the import syntax: ```user = consolegame.User(<projectname>, <commands>)```, replace the <> with the items described between them. There are also additional arguments called: ```intro``` and ```clearonstart```, these are set to ```True``` by default.
4. Initialize functions in the module do this by adding the following in the code after the import syntax: ```functions = consolegame.Functions()```. There is also an additional argument called: ```intro```, this is set to ```True``` by default.
5. Now create a gameloop, below there is a template on how this works.
### Template:
```
import consolegame

projectname = "Template Project"
commands = ["example"]

user = consolegame.User(projectname, commands)
functions = consolegame.Functions()

while True:
    command = user.command()
    if command == "example":
        functions.write("example command successful")
        input()
    else:
        functions.write("command is not available")
```
