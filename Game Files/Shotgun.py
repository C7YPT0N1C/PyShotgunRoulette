import LogicManager as LM

import random

Shotgun = [] # List of loaded shells.

ShotgunDebug = LM.ShotgunDebug # Enable Debugging.
#ShotgunDebug = 1

# L = Live, B = Blank, E = Empty
ShellTypes = ["L", "B"] # Ensures only Live ("L") or Blank ("B") shells can be loaded into the shotgun.

ShellCount = 0
BlankShells = 0
LiveShells = 0

################################################################################

######## HOW THE SHOTGUN WORKS ########
# TODO

def CheckCurrentShell(): 
    if Shotgun[0] == "L":
        return "Live"
    elif Shotgun[0] == "B":
        return "Blank"
    elif Shotgun[0] == "E" or Shotgun[1] == "":
        return "Empty"
    else:
        return "Empty"

def CheckNextShell(): 
    if Shotgun[1] == "L":
        return "Live"
    elif Shotgun[1] == "B":
        return "Blank"
    elif Shotgun[1] == "E" or Shotgun[1] == "":
        return "Empty"
    else:
        return "Empty"

def LoadShotgun(ShellNo, Balanced):
    # Shells = How many shells to load
    # GameRound = How to load shotgun depending on the round the game is in.
    # Balanced = Whether loading shells into shotgun is truly random, or balanced (e.g. ensuring that there arent like, 7 lives 1 blank.) 
    global Shotgun
    global ShellTypes
    global ShellCount
    global LiveShells
    global BlankShells

    #ShellCount = ShellCount

    Shotgun = [] # Reset chamber

    for Shell in range (ShellCount):
        Shotgun.append("E")
    
    Shotgun.append("E") # The extra "E" is used as check to signify and empty chamber.
    if ShotgunDebug == 1:
        print("\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print("\n! SHOTGUN DEBUGGING: !")
        #print("\n")

    ShellCount = ShellNo

    Shotgun = ["E"] * 17 # Reset chamber

    if Balanced == False: # Random loading of shotgun.
        for Shell in range(ShellCount):
            Shotgun[Shell] = ShellTypes[random.randint(0, len(ShellTypes) - 1)]
            
            if ShotgunDebug == 1:
                print("Shotgun = ", Shotgun)
    
    if Balanced == True: # Balanced loading of shotgun.
        LiveOrBlank = ""
        RandomChoice = random.randint(1, 2)

        if RandomChoice == 1:
            LiveOrBlank = "L" # 1 = Have more Lives
        else:
            LiveOrBlank = "B" # 2 = Have more Blanks
        
        if ShellCount % 2 == 0: # If ShellCount is even.
            Shotgun[0] = LiveOrBlank # Allows while loop to engage (when shotgun is empty, number of Ls and Bs are technically equal.)
            
            while Shotgun.count("L") != Shotgun.count("B"): # Loop exits when number of Ls and Bs are equal.
                for Shell in range(ShellCount):
                    Shotgun[Shell] = ShellTypes[random.randint(0, len(ShellTypes) - 1)]

                    if ShotgunDebug == 1:
                        print("Shotgun = ", Shotgun)
        
        else: # If ShellCount is odd.
            #while Shotgun.count(LiveOrBlank) != ((ShellCount // 2) + random.randint(1, 2)):
            while Shotgun.count(LiveOrBlank) != ((ShellCount // 2) + 1):
                # Loops exits when number the number of the value of "LiveOrBlank" (Ls or Bs) is 1 more than the number of the other value of "LiveOrBlank"
                for Shell in range(ShellCount):
                    Shotgun[Shell] = ShellTypes[random.randint(0, len(ShellTypes) - 1)]

                    if ShotgunDebug == 1:
                        print("Shotgun = ", Shotgun)

    
    LiveShells = Shotgun.count("L")
    BlankShells = Shotgun.count("B")

################################################################################

PredictedChamber = ["E"] * 17 # Resets chamber to "E" for all 17 positions

######## HOW CHAMBER PREDICTION WORKS ########
# TODO: Comment.

def PredictShotgun():
    global PredictedChamber

    #BlankShells = 2 # Debugging
    #LiveShells = 0 # Debugging
    ShellCount = BlankShells + LiveShells

    Count = ShellCount + 1

    # Reset chambers
    PredictedChamber = ["E"] * Count # Resets chamber to "E" for Count + 1 positions
    GeneratedChambers = {i: ["E"] * Count for i in range(1, 8)} # Creates chambers 1-7, all shells reset to "E"

    if ShotgunDebug == 1:
        print("\n! REGENERATING SHOTGUN CHAMBER PREDICTION !")

    for Generation in range(1, 8):
        GeneratingChamber = ["E"] * Count # Reset chamber

        if ShotgunDebug == 1:
            print("\nGENERATION", Generation)

        if BlankShells != 0 and LiveShells != 0: # If there are both blanks and lives in the shotgun.
            while GeneratingChamber.count("B") != BlankShells and GeneratingChamber.count("L") != LiveShells:
                for Shell in range(ShellCount):
                    GeneratingChamber[Shell] = ShellTypes[random.randint(0, len(ShellTypes) - 1)]
        else: # If there are only blanks or only lives in the shotgun.
            for Shell in range(ShellCount):
                    GeneratingChamber[Shell] = ShellTypes[random.randint(0, len(ShellTypes) - 1)]

        GeneratedChambers[Generation] = GeneratingChamber  # Store chamber in dictionary

        if ShotgunDebug == 1:
            print("------------Shotgun = ", Shotgun)
            print(f"Generated Chamber {Generation} = {GeneratedChambers[Generation]}")

    # Count blanks and lives across all chambers
    for Shell in range(ShellCount):
        BlankCount = sum(1 for chamber in GeneratedChambers.values() if chamber[Shell] == "B")
        LiveCount = sum(1 for chamber in GeneratedChambers.values() if chamber[Shell] == "L")

        if BlankCount > LiveCount:
            PredictedChamber[Shell] = "B"
        elif LiveCount > BlankCount:
            PredictedChamber[Shell] = "L"
    
    if ShotgunDebug == 1:
        print("\n----------")
        print("Shotgun = ", Shotgun)
        print("Predicted Chamber = ", PredictedChamber)
        print("\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

################################################################################

def InitialiseShotgun(ShellNo, Balanced):
    LoadShotgun(ShellNo, Balanced)
    PredictShotgun()

def ForceChamber(Chamber, ShellNo): # Force chamber to specific shells. (For testing purposes.)
    global Shotgun
    global ShellCount
    global BlankShells
    global LiveShells

    Shotgun = Chamber
    ShellCount = ShellNo
    LiveShells = Chamber.count("L")
    BlankShells = Chamber.count("B")

################################################################################

def ShotgunTest(Mode, ShellNo, Balanced): # Check how likely a certain order of shells is to be generated.
    global ShotgunDebug

    global ShellCount
    global LiveShells
    global BlankShells

    ShotgunDebug = 0

    TestChamber = ["L", "L", "L", "L", "L", "L", "L", "L", "E", "E", "E", "E", "E", "E", "E", "E", "E"]

    LiveShells = TestChamber.count("L")
    BlankShells = TestChamber.count("B")
    ShellCount = LiveShells + BlankShells
    
    Count = 0

    if Mode == "LoadShotgun":
        LoadShotgun(ShellNo, Balanced)
        print("Shotgun = ", Shotgun)
        print("Live Shells =", LiveShells)
        print("Blank Shells =", BlankShells)
    
    if Mode == "Shotgun":
        while Shotgun != TestChamber:
            LoadShotgun(ShellNo, Balanced)
            print("\nCount", Count + 1, ": Shotgun = ", Shotgun)
            if Shotgun != TestChamber:
                Count = Count + 1
                Chance = 100/Count
                print("Chances: 1 /", Count, "(", Chance, "%)")
    
    if Mode == "Prediction":
        while PredictedChamber != TestChamber:
            PredictShotgun()
            print("\nCount", Count + 1, ": Predicted Chamber = ", PredictedChamber)
            if PredictedChamber != TestChamber:
                Count = Count + 1
                Chance = 100/Count
                print("Chances: 1 /", Count, "(", Chance, "%)")

    Count = Count + 1
    Chance = 100/Count

    print("Chances: 1 /", Count, "(", Chance, "%)")
    print("\nCalculated Chances: 1 /", Count, "(", Chance, "%)")

#ShotgunTest("LoadShotgun", 8, True)
#ShotgunTest("Shotgun", 8, True)
#ShotgunTest("Prediction", 8, True)
