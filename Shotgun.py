import random

ShotgunDebug = 0 # Enable Debugging.

# L = Live, B = Blank, E = Empty
ShellTypes = ["L", "B"] # Ensures only Live ("L") or Blank ("B") shells can be loaded into the shotgun.
Shotgun = ["E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E"]

ShellCount = 0
LiveShells = 0
BlankShells = 0

################################################################################

######## HOW CHAMBER PREDICTION WORKS ########
# TODO

PredictedChamber = ["E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E"]

def PredictShotgun(ShellCount, Balanced):
    # TODO: Comment.
    # TODO: Edit so that it takes into account how many live and blank shells are remaining.
    global PredictedChamber

    ShellCount = ShellCount

    PredictedChamber = ["E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E"] # Reset chamber

    GeneratedChamber1 = ["E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E"] # Reset chamber
    GeneratedChamber2 = ["E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E"]
    GeneratedChamber3 = ["E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E"]
    GeneratedChamber4 = ["E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E"]
    GeneratedChamber5 = ["E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E"]
    GeneratedChamber6 = ["E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E"]
    GeneratedChamber7 = ["E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E"]

    if ShotgunDebug == 1:
        print("\n! GENERATING SHOTGUN CHAMBER PREDICTION !")
    
    for Generation in range (1, 8):
        GeneratingChamber = ["E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E"] # Reset chamber

        if ShotgunDebug == 1:
            print("\nGENERATION", Generation)
            
        if Balanced == False: # Random loading of shotgun.
            for Shell in range(ShellCount):
                GeneratingChamber[Shell] = ShellTypes[random.randint(0, len(ShellTypes) - 1)]
    
        if Balanced == True: # Balanced loading of shotgun.
            if ShellCount % 2 == 0: # If ShellCount is even.
                GeneratingChamber[0] = "L" # Allows while loop to engage (when shotgun is empty, number of Ls and Bs are technically equal.)
            
                while GeneratingChamber.count("L") != GeneratingChamber.count("B"): # Loops exits when number of Ls and Bs are equal.
                    for Shell in range(ShellCount):
                        GeneratingChamber[Shell] = ShellTypes[random.randint(0, len(ShellTypes) - 1)]
        
            else: # If ShellCount is odd.
                RandomChoice = random.randint(1, 2)
                LiveOrBlank = ""
            
                if RandomChoice == 1:
                    LiveOrBlank = "L" # 1 = Have more Lives, 2 = Have more Blanks
                else:
                    LiveOrBlank = "B"

                while GeneratingChamber.count(LiveOrBlank) != ((ShellCount // 2) + 1):
                    # Loops exits when number the number of Ls is 1 more than the number of Bs
                    # (and vice versa, depending on which letter is chosen).
                    for Shell in range(ShellCount):
                        GeneratingChamber[Shell] = ShellTypes[random.randint(0, len(ShellTypes) - 1)]
                        
            #if ShotgunDebug == 1:
                #print("------------Shotgun = ", Shotgun)

        ########################################
        
        if ShotgunDebug == 1:
            print("------------Shotgun = ", Shotgun)

        if Generation == 1:
            GeneratedChamber1 = GeneratingChamber
            if ShotgunDebug == 1:
                print("Generated Chamber 1 = ", GeneratedChamber1)
        if Generation == 2:
            GeneratedChamber2 = GeneratingChamber
            if ShotgunDebug == 1:
                print("Generated Chamber 2 = ", GeneratedChamber2)
        if Generation == 3:
            GeneratedChamber3 = GeneratingChamber
            if ShotgunDebug == 1:
                print("Generated Chamber 3 = ", GeneratedChamber3)
        if Generation == 4:
            GeneratedChamber4 = GeneratingChamber
            if ShotgunDebug == 1:
                print("Generated Chamber 4 = ", GeneratedChamber4)
        if Generation == 5:
            GeneratedChamber5 = GeneratingChamber
            if ShotgunDebug == 1:
                print("Generated Chamber 5 = ", GeneratedChamber5)
        if Generation == 6:
            GeneratedChamber6 = GeneratingChamber
            if ShotgunDebug == 1:
                print("Generated Chamber 6 = ", GeneratedChamber6)
        if Generation == 7:
            GeneratedChamber7 = GeneratingChamber
            if ShotgunDebug == 1:
                print("Generated Chamber 7 = ", GeneratedChamber7)

    ########################################

    for Shell in range (0, ShellCount):
        BlankCount = 0
        
        if GeneratedChamber1[Shell] == "B":
            BlankCount = BlankCount + 1
        if GeneratedChamber2[Shell] == "B":
            BlankCount = BlankCount + 1
        if GeneratedChamber3[Shell] == "B":
            BlankCount = BlankCount + 1
        if GeneratedChamber4[Shell] == "B":
            BlankCount = BlankCount + 1
        if GeneratedChamber5[Shell] == "B":
            BlankCount = BlankCount + 1
        if GeneratedChamber6[Shell] == "B":
            BlankCount = BlankCount + 1
        if GeneratedChamber7[Shell] == "B":
            BlankCount = BlankCount + 1
        
        LiveCount = 0
        
        if GeneratedChamber1[Shell] == "L":
            LiveCount = LiveCount + 1
        if GeneratedChamber2[Shell] == "L":
            LiveCount = LiveCount + 1
        if GeneratedChamber3[Shell] == "L":
            LiveCount = LiveCount + 1
        if GeneratedChamber4[Shell] == "L":
            LiveCount = LiveCount + 1
        if GeneratedChamber5[Shell] == "L":
            LiveCount = LiveCount + 1
        if GeneratedChamber6[Shell] == "L":
            LiveCount = LiveCount + 1
        if GeneratedChamber7[Shell] == "L":
            LiveCount = LiveCount + 1
        
        if BlankCount > LiveCount:
            PredictedChamber[Shell] = "B"
            
        if LiveCount > BlankCount:
            PredictedChamber[Shell] = "L"

    if ShotgunDebug == 1:
        print("\n\n----------Shotgun = ", Shotgun)
        print("Predicted Chamber = ", PredictedChamber)
        print("\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

################################################################################

######## HOW THE SHOTGUN WORKS ########
# TODO

def LoadShotgun(ShellNo, Balanced):
    # Shells = How many shells to load
    # GameRound = How to load shotgun depending on the round the game is in.
    # Balanced = Whether loading shells into shotgun is truly random, or balanced (e.g. ensuring that there arent like, 7 lives 1 blank.) 
    global ShellTypes
    global Shotgun
    global ShellCount
    global LiveShells
    global BlankShells

    if ShotgunDebug == 1:
        print("\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print("\n! SHOTGUN DEBUGGING: !")
        #print("\n")

    ShellCount = ShellNo

    Shotgun = ["E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E"] # Reset chamber

    if Balanced == False: # Random loading of shotgun.
        for Shell in range(ShellCount):
            Shotgun[Shell] = ShellTypes[random.randint(0, len(ShellTypes) - 1)]
            
            if ShotgunDebug == 1:
                print("Shotgun = ", Shotgun)
    
    if Balanced == True: # Balanced loading of shotgun.
        if ShellCount % 2 == 0: # If ShellCount is even.
            Shotgun[0] = "L" # Allows while loop to engage (when shotgun is empty, number of Ls and Bs are technically equal.)
            
            while Shotgun.count("L") != Shotgun.count("B"): # Loops exits when number of Ls and Bs are equal.
                for Shell in range(ShellCount):
                    Shotgun[Shell] = ShellTypes[random.randint(0, len(ShellTypes) - 1)]

                    if ShotgunDebug == 1:
                        print("Shotgun = ", Shotgun)
        
        else: # If ShellCount is odd.
            RandomChoice = random.randint(1, 2)
            LiveOrBlank = ""
            
            if RandomChoice == 1:
                LiveOrBlank = "L" # 1 = Have more Lives, 2 = Have more Blanks
            else:
                LiveOrBlank = "B"

            while Shotgun.count(LiveOrBlank) != ((ShellCount // 2) + 1):
                # Loops exits when number the number of Ls is 1 more than the number of Bs
                # (and vice versa, depending on which letter is chosen).
                for Shell in range(ShellCount):
                    Shotgun[Shell] = ShellTypes[random.randint(0, len(ShellTypes) - 1)]

                    if ShotgunDebug == 1:
                        print("Shotgun = ", Shotgun)

    
    LiveShells = Shotgun.count("L")
    BlankShells = Shotgun.count("B")
    
    PredictShotgun(ShellCount, True)

################################################################################

def ShotgunRandomnessTest(ShellNo, Balanced): # Check how likely a certain order of shells is to be generated.
    TestShotgun = ["L", "L", "L", "L", "L", "L", "L", "L", "E", "E", "E", "E", "E", "E", "E", "E", "E"]
    Count = 0
    
    while Shotgun != TestShotgun:
        LoadShotgun(ShellNo, Balanced)
        print("\nCount", Count + 1, ": Shotgun = ", Shotgun)
        if Shotgun != TestShotgun:
            Count = Count + 1
            Chance = 100/Count #####
            print("Chances: 1 /", Count, "(", Chance, "%)") #####
    
    Count = Count + 1
    Chance = 100/Count

    print("Chances: 1 /", Count, "(", Chance, "%)")
    print("\nCalculated Chances: 1 /", Count, "(", Chance, "%)")

def LoadShotgunTest(ShellNo, Balanced):
    LoadShotgun(ShellNo, Balanced)
    print("Shotgun = ", Shotgun)
    print("LiveShells =", LiveShells)

#ShotgunRandomnessTest(8, True)
#LoadShotgunTest(8, True)