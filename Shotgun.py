import random

# L = Live, B = Blank, E = Empty
ShellTypes = ["L", "B"] # Ensures only Live ("L") or Blank ("B") shells can be loaded into the shotgun.
Shotgun = [] # List of loaded shells.
ShellCount = 0
LiveShells = 0
BlankShells = 0

def SetShotgun():
    global Shotgun

    #Shotgun = ["E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E"] # 16 Shells + extra "E" as check.
    Shotgun = ["E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E"] # 32 Shells + extra "E" as check.

def LoadShotgun(ShellNo, Balanced):
    # Shells = How many shells to load
    # GameRound = How to load shotgun depending on the round the game is in.
    # Balanced = Whether loading shells into shotgun is truly random, or balanced (e.g. ensuring that there arent like, 7 lives 1 blank.) 
    global ShellTypes
    global Shotgun
    global ShellCount
    global LiveShells
    global BlankShells

    ShellCount = ShellNo

    SetShotgun() # Reset chamber

    if Balanced == False: # Random loading of shotgun.
        for Shell in range(ShellCount):
            Shotgun[Shell] = ShellTypes[random.randint(0, len(ShellTypes) - 1)]
    
    if Balanced == True: # Balanced loading of shotgun.
        if ShellCount % 2 == 0: # If ShellCount is even.
            Shotgun[0] = "L" # Allows while loop to engage (when shotgun is empty, number of Ls and Bs are technically equal.)
            
            while Shotgun.count("L") != Shotgun.count("B"): # Loops exits when number of Ls and Bs are equal.
                for Shell in range(ShellCount):
                    Shotgun[Shell] = ShellTypes[random.randint(0, len(ShellTypes) - 1)]
                #print(Shotgun)
        
        else: # If ShellCount is odd.
            RandomChoice = random.randint(1, 2)
            LiveOrBlank = ""
            
            if RandomChoice == 1:
                LiveOrBlank = "L" # 1 = Have more Lives, 2 = Have more Blanks
            else:
                LiveOrBlank = "B"

            while Shotgun.count(LiveOrBlank) != ((ShellCount // 2) + 1):
                # Loops exits when number the number of Ls is 1 more than the number of Bs
                #(and vice versa, depending on which letter is chosen).
                for Shell in range(ShellCount):
                    Shotgun[Shell] = ShellTypes[random.randint(0, len(ShellTypes) - 1)]

    
    LiveShells = Shotgun.count("L")
    BlankShells = Shotgun.count("B")