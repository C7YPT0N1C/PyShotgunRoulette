import LogicManager as LM
import Shotgun
#import PlayerUI
import DealerAI as DAI

# TODO: Finish commenting
# TODO: Add 2 player (use AI analysis as player move suggestions?)

######################################## GAME ROUNDS ########################################

def GameRounds(GameRound, Lives, ShellCount):
    #Shotgun.ShellCount = ShellCount
    #Shotgun.LoadShotgun(ShellCount, GameRound)
    
    LM.PlayerLives = Lives # Reset Lives
    LM.DealerLives = Lives
    print("\n####################################################################################################")
    if GameRound == 1:
        print("\n##### NEW GAME #####")
    print("##### ROUND", GameRound, "#####")

    Shotgun.LoadShotgun(ShellCount, True)
        

    CurrentShell = LM.CheckCurrentShell()

    while CurrentShell != "Empty":
        CurrentShell = LM.CheckCurrentShell()
            
        if CurrentShell != "Empty":
            if LM.PlayerLives != 0:
                if LM.DealerLives != 0:
                    LM.PlayersTurn() # Calls for Player's turn.
                else:
                    LM.GUI("PlayerDied", "Dealer") # Report that Dealer died.
                    break
            else:
                LM.GUI("PlayerDied", "Player") # Report that Player died.
                break
        else:
            LM.GUI("Shotgun", "Empty") # Report that shotgun chamber is empty.
            break

        CurrentShell = LM.CheckCurrentShell()

        if CurrentShell != "Empty":
            if LM.DealerLives != 0:
                if LM.PlayerLives != 0:
                    LM.DealersTurn() # Calls for Dealer's turn.
                else:
                    LM.GUI("PlayerDied", "Player") # Report that Player died.
                    break
            else:
                LM.GUI("PlayerDied", "Dealer") # Report that Dealer died.
                break
        else:
            LM.GUI("Shotgun", "Empty") # Report that shotgun chamber is empty.
            break

def StartGame(MaxGameRounds):
    LM.MaxGameRounds = MaxGameRounds

    if MaxGameRounds == 2:
        GameRounds(LM.GameRound, 3, 5)
        
        LM.GameRound += 1

        GameRounds(LM.GameRound, 3, 8)

    if MaxGameRounds == 3:
        GameRounds(LM.GameRound, 3, 5)
        
        LM.GameRound += 1

        GameRounds(LM.GameRound, 3, 8)

        LM.GameRound += 1

        GameRounds(LM.GameRound, 5, 16)

    if MaxGameRounds == 5:
        GameRounds(LM.GameRound, 3, 5)
        
        LM.GameRound += 1

        GameRounds(LM.GameRound, 3, 8)

        LM.GameRound += 1

        GameRounds(LM.GameRound, 5, 16)

        LM.GameRound += 1

        GameRounds(LM.GameRound, 3, 8)

        LM.GameRound += 1

        GameRounds(LM.GameRound, 5, 16)
    
    if LM.GameRound != (LM.MaxGameRounds + 1): # End game after final round is complete
        print("\n! GAME OVER. !")
        exit

######################################## MAIN RUNTIME ########################################

def Main():
    ChooseGameMode = int(input("Choose the Game Mode (1 = Player vs Dealer AI, 2 = Player 1 vs Player 2.): ")) # Choose Game Mode.
    if ChooseGameMode == 2:
        print("\n! Selecting Player 1 vs Player 2 Game Mode. !")
        LM.GameMode = 2
    
    if ChooseGameMode == 420069: # Game Debugging.
        if LM.GameDebug == 1:
            print("\n! Game Debugging Deactivated. !")
            LM.GameDebug = 0
            LM.DealerDebug = 0
            Main()

        print("\n! Game Debugging Activated. !")
        LM.GameDebug = 1

        DealerDecisionDebug = int(input("\nActivate Dealer Decision Debugging? (1 = Yes, 2 = No.): ")) # Activate Dealer Decision Debugging.
        if DealerDecisionDebug == 1:
            print("\n! Dealer Decision Debugging Activated. !")
            LM.DealerDecisionDebug = 1

        else:
            print("\n! Dealer Decision Debugging Deactivated. !")
            LM.DealerDecisionDebug = 0

        DealerAnalysisDebug = int(input("\nActivate Dealer Analysis Debugging? (1 = Yes, 2 = No.): ")) # Activate Dealer Analysis Debugging.
        if DealerAnalysisDebug == 1:
            print("\n! Dealer Analysis Debugging Activated. !")
            LM.DealerAnalysisDebug = 1

        else:
            print("\n! Dealer Analysis Debugging Deactivated. !")
            LM.DealerAnalysisDebug = 0

        Main()
    
    else:
        print("\n! Selecting Player vs Dealer AI Game Mode. !")
        LM.GameMode = 1

        ChooseAILevel = int(input("\nChoose the Dealer's AI difficulty (1 = Normal, 2 = Hard, 3 = CHEATER.): ")) # Choose the difficulty of the Dealer's AI.
        if ChooseAILevel == 2:
            print("\n! Starting game with 'Hard' Dealer AI diffiiculty. !")
        elif ChooseAILevel == 3:
            print("\n! Starting game with 'CHEATER' Dealer AI diffiiculty. !")
        else:
            print("\n! Starting game with 'Normal' Dealer AI diffiiculty. !")
            LM.AILevel = 1
    
    StartGame(5)

def DebugMain():
    print("! Setting Game Debugging Variables. !")
    LM.GameDebug = 1

    print("\n! Setting Debugging Variables. !")
    LM.DealerDecisionDebug = 1
    LM.DealerAnalysisDebug = 1

    print("\n! Setting Game Mode. !")
    LM.GameMode = 1

    print("\n! Setting Dealer AI diffiiculty. !")
    #LM.AILevel = 1 # Easy
    LM.AILevel = 2 # Hard
    #LM.AILevel = 3 # CHEATER

    StartGame(2)

#DebugMain()
Main()