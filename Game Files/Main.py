import Shotgun as Shotgun
import LogicManager as LM
import Timer as Timer
import DealerAI as DAI

Debugging = 0

######################################## GAME ROUNDS ########################################

def GameRounds(GameRound, Lives, ShellCount, ShotgunBalance):
    #Shotgun.ShellCount = ShellCount
    #Shotgun.LoadShotgun(ShellCount, GameRound)
    
    if GameRound == 1:
        print("\n##### NEW GAME #####")

        if LM.AILevel == 3:
            print("\n! THE Dealer's AI difficulty IS SET TO 'CHEATER'. THE DEALER WILL NOT GUESS INCORRECTLY. !")

        print("\n##### ROUND 1 #####")
    
    #if GameRound == 2:
        #print("\n\n##### ROUND 2 #####")
    
    #if GameRound == 3:
        #print("\n\n##### ROUND 3 #####")

    else:
        print("\n\n##### ROUND", GameRound, "#####")

    if GameRound == "End":
        print("\n\n##### GAME OVER #####")
        Main()
    
    LM.PlayerLives = Lives # Reset Lives
    LM.Player2Lives = Lives
    LM.DealerLives = Lives

    Shotgun.ShellCount = ShellCount

    if ShotgunBalance == False:
        Shotgun.LoadShotgun(ShellCount, False)
    else:
        Shotgun.LoadShotgun(ShellCount, True)

    LM.GUI("Shotgun", "Loaded") # Report that shotgun has been loaded.

    Timer.WaitTime("Reset")  # See function. Reset Dealer RunTime.

    ############## Game Turn Loop ##############
    CurrentShell = Shotgun.CheckCurrentShell() # Update current shell

    while CurrentShell != "Empty": # Only runs whilst shotgun has loaded shells.
        CurrentShell = Shotgun.CheckCurrentShell() # Update current shell

        if LM.GameMode == 1: # Player 1 VS Dealer.
            ###### Player 1's Turn ######
            if LM.PlayerLives != 0 and LM.DealerLives != 0 and CurrentShell != "Empty": # Only runs whilst Player 1 or The Dealer isnt dead, and whilst the shotgun has loaded shells.
                LM.PlayersTurn() # Calls for Player 1's turn.
            else:
                if LM.PlayerLives == 0:
                    LM.GUI("PlayerDied", "Player1") # Report that Player died.
                if LM.DealerLives == 0:
                    LM.GUI("PlayerDied", "Dealer") # Report that Dealer died.
                if CurrentShell == "Empty":
                    LM.GUI("Shotgun", "Empty") # Report that shotgun chamber is empty.
                break
            ###### Player 1's Turn ######

            ###### Dealer's Turn ######
            if LM.PlayerLives != 0 and LM.DealerLives != 0 and CurrentShell != "Empty": # Only runs whilst Player 1 or The Dealer isnt dead, and whilst the shotgun has loaded shells.
                LM.DealersTurn() # Calls for Player 1's turn.
            else:
                if LM.PlayerLives == 0:
                    LM.GUI("PlayerDied", "Player1") # Report that Player died.
                if LM.DealerLives == 0:
                    LM.GUI("PlayerDied", "Dealer") # Report that Dealer died.
                if CurrentShell == "Empty":
                    LM.GUI("Shotgun", "Empty") # Report that shotgun chamber is empty.
                break
            ###### Dealer's Turn ######
        
        else: # Player 1 VS Player 2.
            ###### Player 1's Turn ######
            if LM.PlayerLives != 0 and LM.Player2Lives != 0 and CurrentShell != "Empty": # Only runs whilst Player 1 or Player 2 isnt dead, and whilst the shotgun has loaded shells.
                LM.PlayersTurn(1) # Calls for Player 1's turn.
            else:
                if LM.PlayerLives == 0:
                    LM.GUI("PlayerDied", "Player1") # Report that Player died.
                if LM.Player2Lives == 0:
                    LM.GUI("PlayerDied", "Player2") # Report that Dealer died.
                if CurrentShell == "Empty":
                    LM.GUI("Shotgun", "Empty") # Report that shotgun chamber is empty.
                break
            ###### Player 1's Turn ######

            ###### Player 2's Turn ######
            if LM.PlayerLives != 0 and LM.Player2Lives != 0 and CurrentShell != "Empty": # Only runs whilst Player 1 or Player 2 isnt dead, and whilst the shotgun has loaded shells.
                LM.PlayersTurn(2) # Calls for Player 1's turn.
            else:
                if LM.PlayerLives == 0:
                    LM.GUI("PlayerDied", "Player1") # Report that Player died.
                if LM.Player2Lives == 0:
                    LM.GUI("PlayerDied", "Player2") # Report that Dealer died.
                if CurrentShell == "Empty":
                    LM.GUI("Shotgun", "Empty") # Report that shotgun chamber is empty.
                break
            ###### Player 2's Turn ######

        ############## Game Turn Loop ##############

def StartGame(ShotgunBalance): # Define Game Rounds Here.
    GameRounds(LM.GameRound, 2, 5, ShotgunBalance)
        
    LM.GameRound += 1
    #GameRounds(LM.GameRound, 2, 5, ShotgunBalance)
    GameRounds(LM.GameRound, 5, 16, ShotgunBalance)

    LM.GameRound += 1
    #GameRounds(LM.GameRound, 2, 5, ShotgunBalance)
    GameRounds(LM.GameRound, 7, 32, ShotgunBalance)

    LM.GameRound = "End"
    GameRounds(LM.GameRound, 0, 0, ShotgunBalance)

######################################## MAIN RUNTIME ########################################

def Options():
    global Debugging

    print("\nDebugging:", Debugging)
    Debugging = input("Do you want to activate Debugging? (0 = No, 1 = Yes): ") # Enable Debugging.
    if Debugging == "1":
        print("! Activating Debugging. !")
        
        print("\nGame Debugging:", LM.GameDebug)
        GameDebug = input("Do you want to enable Game Debugging? (1 = No, 2 = Yes): ") # Enable Game Debugging.
        if GameDebug == "2":
            print("! Enabling Game Debugging. !")
            LM.GameDebug = 1
        else:
            print("! Disabling Game Debugging. !")
            LM.GameDebug = 0
        
        print("\nDealer Decision Debugging:", LM.DealerDecisionDebug)
        DealerDecisionDebug = input("Do you want to enable Dealer Decision Debugging? (1 = No, 2 = Yes): ") # Enable Dealer Decision Debugging.
        if DealerDecisionDebug == "2":
            print("! Enabling Dealer Decision Debugging. !")
            LM.DealerDecisionDebug = 1
        else:
            print("! Disabling Dealer Decision Debugging. !")
            LM.DealerDecisionDebug = 0

        print("\nDealer Analysis Debugging:", LM.DealerAnalysisDebug)
        DealerAnalysisDebug = input("Do you want to enable Dealer Analysis Debugging? (1 = No, 2 = Yes): ") # Enable Dealer Analysis Debugging.
        if DealerAnalysisDebug == "2":
            print("! Enabling Dealer Analysis Debugging. !")
            LM.DealerAnalysisDebug = 1
        else:
            print("! Disabling Dealer Analysis Debugging. !")
            LM.DealerAnalysisDebug = 0

        print("\nShotgun Debugging:", LM.ShotgunDebug)
        ShotgunDebug = input("Do you want to enable Shotgun Debugging? (1 = No, 2 = Yes): ") # Enable Shotgun Debugging.
        if ShotgunDebug == "2":
            print("! Enabling Shotgun Debugging. !")
            LM.ShotgunDebug = 1
        else:
            print("! Disabling Shotgun Debuggingging. !")
            LM.ShotgunDebug = 0
        
        print("\n! Returning to Main Menu. !")

    else:
        print("! Deactivating Debugging. !")
    
    Main()

def Main():
    GameMenu = input("\nMain Menu! (1 = Play Game, 2 = Options): ") # Choose game mode.
    if GameMenu == "1":
        print("\n! Starting Game. !")
        
        ChooseGameMode = input("\nChoose the Game Mode (1 = Player vs Dealer AI, 2 = Player 1 vs Player 2): ") # Choose game mode.
        if ChooseGameMode == "2":
            print("\n! Selecting Player 1 vs Player 2 Game Mode. !")
            LM.GameMode = 2
        else:
            print("\n! Selecting Player vs Dealer AI Game Mode. !")
            LM.GameMode = 1

            ChooseAILevel = input("\nChoose The Dealer's AI difficulty (1 = Easy, 2 = Normal, 3 =  CHEATER): ") # Choose the difficulty of the Dealer's AI.
            if ChooseAILevel == "2":
                print("\n! Starting game with 'Normal' Dealer AI diffiiculty. !")
                LM.AILevel = 2
            elif ChooseAILevel == "3":
                print("\n! Starting game with 'CHEATER' Dealer AI diffiiculty. !")
                LM.AILevel = 3
            else:
                print("\n! Starting game with 'Easy' Dealer AI diffiiculty. !")
                LM.AILevel = 1
            
        ChooseShotgunBalance = input("\nDo you want the Shotgun to be balanced? (1 = No, 2 = Yes): ") # Choose whether  loading the shotgun is balanced or not.
        if ChooseShotgunBalance == "1":
            print("\n! Starting game with an unbalanced Shotgun. !")
            StartGame(False)
        else:
            print("\n! Starting game with an balanced Shotgun. !")
            StartGame(True)

    else:
        print("\n! Entering Option Menu. !")
        Options()