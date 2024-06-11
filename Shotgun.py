import random

import VariableManager as VM

Shotgun = [] # List of loaded shells.

# L = Live, B = Blank, E = Empty
ShellTypes = ["L", "B"] # Ensures only Live ("L") or Blank ("B") shells can be loaded into the shotgun.

ShellCount = 0
LiveShells = 0
BlankShells = 0

def LoadShotgun(Balanced):
    # ShellNum = How many shells to load
    # Balanced = Whether loading shells into shotgun is truly random, or balanced (e.g. ensuring that there arent like, 7 lives 1 blank.) 
    global Shotgun
    global ShellTypes
    global ShellCount
    global LiveShells
    global BlankShells

    ShellCount = VM.ShotgunShellCount

    Shotgun = [] # Reset chamber

    for Shell in range (ShellCount):
        Shotgun.append("E")
    
    Shotgun.append("E") # The extra "E" is used as check to signify and empty chamber.

    if Balanced == False: # Random loading of shotgun.
        for Shell in range(ShellCount):
            Shotgun[Shell] = ShellTypes[random.randint(0, len(ShellTypes) - 1)]
    
    if Balanced == True: # Balanced loading of shotgun.
        if ShellCount % 2 == 0: # If ShellCount is even.
            Shotgun[0] = "L" # Allows while loop to engage (when shotgun is empty, number of Ls and Bs are technically equal.)
            
            while Shotgun.count("L") != Shotgun.count("B"): # Loop exits when number of Ls and Bs are equal.
                for Shell in range(ShellCount):
                    Shotgun[Shell] = ShellTypes[random.randint(0, len(ShellTypes) - 1)]
                #print(Shotgun)
        
        else: # If ShellCount is odd.
            LiveOrBlank = ""
            RandomChoice = random.randint(1, 2)
            
            if RandomChoice == 1:
                LiveOrBlank = "L" # 1 = Have more Lives, 2 = Have more Blanks
            else:
                LiveOrBlank = "B"

            while Shotgun.count(LiveOrBlank) != ((ShellCount // 2) + random.randint(1, 2)):
                # Loop exits when number the number of Ls is a random amount more than the number of Bs (and vice versa, depending on which letter is chosen).
                # The random number is between 1 and 2.
                for Shell in range(ShellCount):
                    Shotgun[Shell] = ShellTypes[random.randint(0, len(ShellTypes) - 1)]

    
    LiveShells = Shotgun.count("L")
    BlankShells = Shotgun.count("B")

def CheckCurrentShell(): 
    if Shotgun[0] == "L":
        return "Live"
    if Shotgun[0] == "B":
        return "Blank"
    if Shotgun[0] == "E" or Shotgun[1] == "":
        return "Empty"

def CheckNextShell(): 
    if Shotgun[1] == "L":
        return "Live"
    if Shotgun[1] == "B":
        return "Blank"
    if Shotgun[1] == "E" or Shotgun[1] == "":
        return "Empty"

#CurrentShell = CheckCurrentShell()
#NextShell = CheckNextShell()

#GenerateShotgun(8, True)
#print("Shotgun = ", Shotgun)