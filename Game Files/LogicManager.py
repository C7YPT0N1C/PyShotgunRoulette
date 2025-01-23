import Main

import Shotgun as Shotgun
import Timer as Timer
import PlayerUI as PlayerUI
import DealerAI as DAI

import random as random
import time as time

######################################## DECLARE VARIABLES ########################################
GameDebug = 0
DealerDecisionDebug = 0
DealerAnalysisDebug = 0
ShotgunDebug = 0

GameMode = 1
GameRound = 0
RoundEnd = 0

AILevel = 1

StartingTurn = 0
CurrentTurn = 0

#WaitTime = 1.5 # Make code wait WaitTime seconds. Makes output more readable while playing.
#def Wait():
    #time.sleep(WaitTime) # Wait WaitTime seconds. Makes output more readable while playing.

PlayerLives = 3
Player2Lives = 3
DealerLives = 3

#Test = 1

######################################## GUI ########################################

### KEY ###

# ! = System Announcement
# # = Turn Announcement
# - = Action
# () = System "Thoughts"

### KEY ###

def GUI(Element, Modifier):
    global RoundEnd

    if Element == "LiveShell" and Modifier == 0:
        print("\n! It was a Live. !")
    if Element == "BlankShell" and Modifier == 0:
        print("\n! It was a Blank. !")

    if Element == "PrintLives":
        if Modifier == 0:
            if GameMode == 2: # Player 1 VS Player 2.
                print("! Player 1 has", PlayerLives, "lives remaining. !")
                print("! Player 2 has", Player2Lives, "lives remaining. !")
                    
            else: # Player 1 VS Dealer.
                print("! You have", PlayerLives, "lives remaining. !")
                print("! The Dealer has", DealerLives, "lives remaining. !")

    if Element == "PlayerDied":
        if Modifier == "Player1":
            print("\n! PLAYER 1 HAS DIED. !")
            RoundEnd = 1
        if Modifier == "Player2":
            print("\n! PLAYER 2 HAS DIED. !")
            RoundEnd = 1
        if Modifier == "Dealer":
            print("\n! THE DEALER HAS DIED. !")
            RoundEnd = 1

    if Element == "Shotgun":
        if Modifier == "Debug": # Basically cheats.
            print("\nCurrent Shell Is:", Shotgun.CheckCurrentShell())
            print("Next Shell Is:", Shotgun.CheckNextShell())

            print("Shotgun:", Shotgun.Shotgun) 

        if Modifier == "Loaded": ############################################################################################################
            print("\n! Loaded", Shotgun.LiveShells, "Live Shells into the Shotgun's Chamber. !")
            print("! Loaded", Shotgun.BlankShells, "Blank Shells into the Shotgun's Chamber. !")

        if Modifier == "Report": 
            GUI("Shotgun", "Debug") # Basically cheats.
            
            print("\n! ", Shotgun.BlankShells, "Blank Shells left. !")
            print("! ", Shotgun.LiveShells, "Live Shells left. !")
        
        if Modifier == "Empty":
            if PlayerLives == 0:
                GUI("PlayerDied", "Player1") # Report that Player 1 died.
            if Player2Lives == 0:
                GUI("PlayerDied", "Player2") # Report that Player 2 died.
            if DealerLives == 0:
                GUI("PlayerDied", "Dealer") # Report that the Dealer died.
                
            print("\n! Shotgun Chamber Empty, Skipping Turn. !")

######################################## GAME STUFF ########################################

def ShotTaken(Target):
    global GameRound
    
    global PlayerLives
    global DealerLives

    global StartingTurn
    global CurrentTurn

    CurrentShell = Shotgun.CheckCurrentShell()
    NextShell = Shotgun.CheckNextShell()

    Shotgun.ShellCount -= 1
    Shotgun.Shotgun.pop(0)

    if CurrentShell == "Blank":
        Shotgun.BlankShells -= 1
        
        if Target == "Self":
            GUI("BlankShell", 0) # Report that a blank shell was shot.
            if NextShell != "Empty":
                if CurrentTurn == "Player":
                    print("\n! Player gets another go. !")
                    Player1Turn()    
                if CurrentTurn == "Dealer":
                    print("\n! Dealer gets another go. !")
                    DealersTurn()
            else: # If next shell is empty. TODO This shit does NOT work
                GUI("Shotgun", "Empty") # Report that shotgun chamber is empty.
                if CurrentTurn == "Player":
                    print("\n! Player goes first next round. !")
                    StartingTurn = "P1"
                if CurrentTurn == "Dealer":
                    print("\n! Dealer goes first next round. !")
                    StartingTurn = "P2"
        if Target == "Enemy":
            GUI("BlankShell", 0)
        
    if CurrentShell == "Live":
        Shotgun.LiveShells -= 1
        
        if Target == "Self":
            GUI("LiveShell", 0) # Report that a live shell was shot.
            if CurrentTurn == "Player":
                print("\n! PLAYER LOST A LIFE. !")
                PlayerLives = PlayerLives - 1     
            if CurrentTurn == "Dealer":
                print("\n! DEALER LOST A LIFE. !")
                DealerLives = DealerLives - 1
        if Target == "Enemy":
            GUI("LiveShell", 0)
            if CurrentTurn == "Player":
                print("\n! DEALER LOST A LIFE. !")
                DealerLives = DealerLives - 1     
            if CurrentTurn == "Dealer":
                print("\n! PLAYER LOST A LIFE. !")
                PlayerLives = PlayerLives - 1

######################################## GAME ROUNDS #########################################
# TODO: Edit so that the game keeps loading new chambers until a player dies. When a player dies, the round should end.

def GameRounds(Round1Lives, Round2Lives, Round3Lives, ShotgunBalance):
    global GameRound
    global RoundEnd
    
    global PlayerLives
    global Player2Lives
    global DealerLives

    RoundEnd = 0 # Reset RoundEnd
    GameRound = GameRound + 1 # Increment Round Number.
    
    if GameRound == 1: # Print Round Number.
        print("\n##### NEW GAME #####")

        if AILevel == 3:
            print("\n! THE Dealer's AI difficulty IS SET TO 'CHEATER'. THE DEALER WILL NOT GUESS INCORRECTLY. !")

        print("\n##### ROUND 1 #####")
        PlayerLives = Round1Lives # Reset Lives
        Player2Lives = Round1Lives
        DealerLives = Round1Lives
    
    elif GameRound == 2:
        print("\n##### ROUND 2 #####")
        PlayerLives = Round2Lives # Reset Lives
        Player2Lives = Round2Lives
        DealerLives = Round2Lives
    
    elif GameRound == 3:
        print("\n##### ROUND 3 #####")
        PlayerLives = Round3Lives # Reset Lives
        Player2Lives = Round3Lives
        DealerLives = Round3Lives
    
    else:
        print("\n\n##### GAME OVER #####")
        Main.Main()

    ############## In-Round Sequences ##############
    def Sequence(Sequence, ShotgunBalance):
        print("\n###DEBUGGING### Round:", GameRound, "| Sequence:", Sequence)
        if Sequence == 1:
            ShellCount = random.randint(3, 5) # Randomly choose how many shells to load into the shotgun.
        if Sequence == 2:
            ShellCount = random.randint(2, 6)
        if Sequence == 3:
            ShellCount = random.randint(5, 8)
        if Sequence == 4:
            ShellCount = random.randint(8, 16)

        ####### Prerequisites #######
        DAI.ResetPredictions() # Reset Dealer's predictions.

        if ShotgunBalance == False: # Load shotgun with random shells.
            Shotgun.InitialiseShotgun(ShellCount, False)
        else:
            Shotgun.InitialiseShotgun(ShellCount, True)
        
        #Shotgun.ForceChamber(['B', 'B', 'L', 'L', 'B', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'], 5) # Force chamber for testing. See function.

        GUI("Shotgun", "Loaded") # Report that shotgun has been loaded.

        Timer.WaitTime("Reset")  # See function. Reset Dealer RunTime.
        ####### Prerequisites #######

        ####### Game Turn Loop #######
        CurrentShell = Shotgun.CheckCurrentShell() # Update current shell

        while CurrentShell != "Empty": # Only runs whilst shotgun has loaded shells.
            ###### Player 1 VS Dealer ######
            if GameMode == 1:
                ##### Player 1's Turn #####
                CurrentShell = Shotgun.CheckCurrentShell() # Update current shell for Player's turn.
                if CurrentShell != "Empty" and PlayerLives != 0 and DealerLives != 0: # Only runs whilst the chamber isnt empty, and whilst Player 1 or The Dealer isnt dead.
                    Player1Turn() # Calls for Player 1's turn.
                else:
                    if PlayerLives == 0:
                        GUI("PlayerDied", "Player1") # Report that Player died.
                    if DealerLives == 0:
                        GUI("PlayerDied", "Dealer") # Report that Dealer died.
                    break
                ##### Player 1's Turn #####

                ##### Dealer's Turn #####
                CurrentShell = Shotgun.CheckCurrentShell() # Update current shell for Dealer's turn.
                if CurrentShell != "Empty" and DealerLives != 0 and PlayerLives != 0: # Only runs whilst the chamber isnt empty, and whilst The Dealer or Player 1 isnt dead.
                    DealersTurn() # Calls for The Dealer's turn.
                else:
                    if DealerLives == 0:
                        GUI("PlayerDied", "Dealer") # Report that Dealer died.
                    if PlayerLives == 0:
                        GUI("PlayerDied", "Player1") # Report that Player died.
                    break
                ##### Dealer's Turn #####
            ###### Player 1 VS Dealer ######
            
            ###### Player 1 VS Player 2 ######
            else:
                ##### Player 1's Turn #####
                CurrentShell = Shotgun.CheckCurrentShell() # Update current shell for Player 1's turn.
                if CurrentShell != "Empty" and PlayerLives != 0 and Player2Lives != 0: # Only runs whilst the chamber isnt empty, and whilst Player 1 or Player 2 isnt dead.
                    Player1Turn() # Calls for Player 1's turn.
                else:
                    if PlayerLives == 0:
                        GUI("PlayerDied", "Player1") # Report that Player 1 died.
                    if Player2Lives == 0:
                        GUI("PlayerDied", "Player2") # Report that Player 2 died.
                    break
                ##### Player 1's Turn #####

                ##### Player 2's Turn #####
                CurrentShell = Shotgun.CheckCurrentShell() # Update current shell for Player 2's turn.
                if CurrentShell != "Empty" and Player2Lives != 0 and PlayerLives != 0: # Only runs whilst the chamber isnt empty, and whilst Player 2 or Player 1 isnt dead.
                    Player2Turn() # Calls for Player 1's turn.
                else:
                    if Player2Lives == 0:
                        GUI("PlayerDied", "Player2") # Report that Player 2 died.
                    if PlayerLives == 0:
                        GUI("PlayerDied", "Player1") # Report that Player 1 died.
                    break
                ##### Player 2's Turn #####
            ###### Player 1 VS Player 2 ######
        ####### Game Turn Loop #######
    ############## In-Round Sequences ##############
    
    while RoundEnd != 1: # Runs whilst the round hasnt ended.
        Sequence(1, ShotgunBalance)
        Sequence(2, ShotgunBalance)
        Sequence(3, ShotgunBalance)
        Sequence(4, ShotgunBalance)
    else:
        GameRounds(Round1Lives, Round2Lives, Round3Lives, ShotgunBalance) # Start new round.

######################################## PLAYER TURNS #########################################

# TODO: Recode to let the player who shot the last bullet in the event that it is a Blank to go first in the next round.
# ADD ITEMS

def Player1Turn():
    global CurrentTurn

    CurrentTurn = "Player"
    
    #print("\n###DEBUGGING### ! StartingTurn =", StartingTurn, " !")
    #print("\n###DEBUGGING### ! CurrentTurn =", CurrentTurn, " !")
    
    Timer.GameWait("Full") # See function.
    if GameDebug == 1:
        GUI("Shotgun", "Report")
    print("\n### PLAYERS' TURN:")
    GUI("PrintLives", 0)

    Timer.GameWait("Short") # See function.
    Outcome = PlayerUI.Turn(1)
    if GameDebug == 1:
        print("\n###DEBUGGING### Player Turn Outcome:", Outcome)

    if Outcome == "ShootSelf":
        print("\n- You shoot yourself. -")
        ShotTaken("Self")
    elif Outcome == "ShootDealer":
        print("\n- You shoot the Dealer. -")
        ShotTaken("Enemy")
    elif Outcome == "ChoiceFailed":
        Player1Turn()
    else:
        print("\n! Error. Defaulting to shooting The Dealer. !")
        print("\n- You shoot the Dealer. -")
        ShotTaken("Enemy")

def Player2Turn():
    global CurrentTurn

    CurrentTurn = "Player"
    
    #print("\n###DEBUGGING### ! StartingTurn =", StartingTurn, " !")
    #print("\n###DEBUGGING### ! CurrentTurn =", CurrentTurn, " !")
    
    Timer.GameWait("Full") # See function.
    if GameDebug == 1:
        GUI("Shotgun", "Report")
    print("\n### PLAYERS' TURN:")
    GUI("PrintLives", 0)

    Timer.GameWait("Short") # See function.
    Outcome = PlayerUI.Turn(2)
    if GameDebug == 1:
        print("\n###DEBUGGING### Player Turn Outcome:", Outcome)

    if Outcome == "ShootSelf":
        print("\n- You shoot yourself. -")
        ShotTaken("Self")
    elif Outcome == "ShootDealer":
        print("\n- You shoot the Dealer. -")
        ShotTaken("Enemy")
    elif Outcome == "ChoiceFailed":
        Player2Turn()
    else:
        print("\n! Error. Defaulting to shooting The Dealer. !")
        print("\n- You shoot the Dealer. -")
        ShotTaken("Enemy")

def DealersTurn():
    global CurrentTurn

    CurrentTurn = "Dealer"
    
    #print("\n###DEBUGGING### ! StartingTurn =", StartingTurn, " !")
    #print("\n###DEBUGGING### ! CurrentTurn =", CurrentTurn, " !")

    Timer.GameWait("Full") # See function.
    if GameDebug == 1:
        GUI("Shotgun", "Report")
    print("\n### DEALER'S TURN:")
    GUI("PrintLives", 0)

    Timer.GameWait("Short") # See function.
    Timer.WaitTime("Start") # See function.
    Outcome = DAI.Turn(AILevel)

    #Timer.GameWait("Full") # See function.
    if DealerDecisionDebug == 1:
        print("\n###DEBUGGING### Dealer Turn Outcome:", Outcome)

    Timer.GameWait("Short") # See function.
    
    if Outcome == "ShootSelf":
        print("\n- The Dealer shoots itself. -")
        ShotTaken("Self")
        
    if Outcome == "ShootPlayer":
        print("\n- The Dealer shoots you. -")
        ShotTaken("Enemy")