import LogicManager as LM

import Shotgun
#import PlayerUI
import DealerAI as DAI

######################################## GAME ROUNDS ########################################

def GameRounds(GameRound, Lives, ShellCount, ShotgunBalance):
    #Shotgun.ShellCount = ShellCount
    #Shotgun.LoadShotgun(ShellCount, GameRound)
    
    if GameRound == 1:
        print("\n##### NEW GAME #####")
        print("\n##### ROUND 1 #####")
    
    if GameRound == 2:
        print("\n\n##### ROUND 2 #####")
    
    if GameRound == 3:
        print("\n\n##### ROUND 3 #####")

    if GameRound == "End":
        print("\n\n##### GAME OVER #####")
    
    LM.PlayerLives = Lives # Reset Lives
    LM.Player2Lives = Lives
    LM.DealerLives = Lives

    if ShotgunBalance == False:
        Shotgun.LoadShotgun(ShellCount, False)
    else:
        Shotgun.LoadShotgun(ShellCount, True)
    

    ############## Game Turn Loop ##############

    CurrentShell = LM.CheckCurrentShell() # Update current shell.

    ###### Player 1's Turn ######
    while CurrentShell != "Empty": # Only runs whilst shotgun has loaded shells.
        if LM.PlayerLives != 0: # Only runs whilst Player 1 isnt dead.
            if CurrentShell != "Empty": # Only runs whilst shotgun has loaded shells.
                
                if LM.GameMode == 2: # Player 1 VS Player 2.
                    if LM.Player2Lives != 0: # Only runs whilst Player 2 isnt dead.
                        LM.PlayerTurn(1) # Calls for Player 1's turn.
                    else:
                        LM.GUI("PlayerDied", "Player2") # Report that Player 2 died.
                        break # Exit loop
                
                else: # Player 1 VS AI.
                    if LM.DealerLives != 0: # Only runs whilst The Dealer isnt dead.
                        LM.PlayerTurn(1) # Calls for Player 1's turn.
                    else:
                        LM.GUI("PlayerDied", "Dealer") # Report that Dealer died.
                        break # Exit loop
            else:
                LM.GUI("Shotgun", "Empty") # Report that shotgun chamber is empty.
                break
        else:
            LM.GUI("PlayerDied", "Player1") # Report that Player died.
            break
        ###### Player 1's Turn ######

        ###### Player 2's Turn ######
        if LM.GameMode == 2: # Player 1 VS Player 2.
            if LM.Player2Lives != 0: # Only runs whilst Player 2 isnt dead.
                if CurrentShell != "Empty":
                    if LM.PlayerLives != 0: # Only runs whilst Player 1 isnt dead.
                        LM.PlayerTurn(2) # Calls for Player 2's turn.
                    else:
                        LM.GUI("PlayerDied", "Player1") # Report that Player 1 died.
                        break
                else:
                    LM.GUI("Shotgun", "Empty") # Report that shotgun chamber is empty.
                    break
            else:
                LM.GUI("PlayerDied", "Player2") # Report that Player 2 died.
                break
        ###### Player 2's Turn ######
        
        ###### The Dealer's Turn ######
        else: # Player 1 VS AI.
            if LM.DealerLives != 0:
                if CurrentShell != "Empty":
                    if LM.PlayerLives != 0:
                        LM.DealersTurn() # Calls for Dealer's turn.
                    else:
                        LM.GUI("PlayerDied", "Player1") # Report that Player died.
                        break
                else:
                    LM.GUI("Shotgun", "Empty") # Report that shotgun chamber is empty.
                    break
            else:
                LM.GUI("PlayerDied", "Dealer") # Report that Dealer died.
                break
        ###### The Dealer's Turn ######

        ############## Game Turn Loop ##############

def StartGame(ShotgunBalance):
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

def Main():
    ChooseGameMode = int(input("Choose the Game Mode (1 = Player vs Dealer AI, 2 = Player 1 vs Player 2): ")) # Choose game mode.
    if ChooseGameMode == 2:
        print("\n! Selecting Player 1 vs Player 2 Game Mode. !")
        LM.GameMode = 2
    else:
        print("\n! Selecting Player vs Dealer AI Game Mode. !")
        LM.GameMode = 1

        ChooseAILevel = int(input("\nChoose the Dealer's AI difficulty (1 = Normal, 2 = Hard (Work In Progress) ): ")) # Choose the difficulty of the Dealer's AI.
        if ChooseAILevel == 2:
            print("\n! Starting game with 'Hard' Dealer AI diffiiculty. !")
            LM.AILevel = 2
        else:
            print("\n! Starting game with 'Normal' Dealer AI diffiiculty. !")
            LM.AILevel = 1
    
    ChooseShotgunBalance = int(input("\nDo you want the shotgun to be balanced or not? (1 = No, 2 = Yes): ")) # Choose whether the shotgun is loading balanced or not.
    if ChooseShotgunBalance == 1:
        print("\n! Starting game with a unbalanced shotgun. !")
        StartGame(False)
    else:
        print("\n! Starting game with an balanced shotgun. !")
        StartGame(True)

Main()