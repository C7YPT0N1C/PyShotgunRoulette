import Shotgun as Shotgun
import Timer as Timer
import PlayerUI as PlayerUI
import DealerAI as DAI

import time as time

######################################## DECLARE VARIABLES ########################################
GameDebug = 0
DealerDecisionDebug = 0
DealerAnalysisDebug = 0
ShotgunDebug = 0

GameMode = 1
MaxGameRounds = 3
GameRound = 1

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
    if Element == "LiveShell" and Modifier == 0:
        print("\n! It was a Live. !")
    if Element == "BlankShell" and Modifier == 0:
        print("\n! It was a Blank. !")

    if Element == "PlayerDied" and Modifier == "Player1":
        print("\n! PLAYER 1 HAS DIED. !")
    if Element == "PlayerDied" and Modifier == "Player2":
        print("\n! PLAYER 2 HAS DIED. !")   
    if Element == "PlayerDied" and Modifier == "Dealer":
        print("\n! THE DEALER HAS DIED. !")

    if Element == "Shotgun":
        if Modifier == "Debug": # Basically cheats.
            print("\n", Shotgun.Shotgun) 
            
            print("Current Shell Is:", Shotgun.CheckCurrentShell())
            print("Next Shell Is:", Shotgun.CheckNextShell())

        if Modifier == "Loaded": ############################################################################################################
            print("\n! Loaded", Shotgun.BlankShells, "Blank Shells into the Shotgun's Chamber. !")
            print("! Loaded", Shotgun.LiveShells, "Live Shells into the Shotgun's Chamber. !")

        if Modifier == "Report": 
            if GameDebug == 2: # Runs if debugging is enabled.
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
    global PlayerLives
    global DealerLives

    global StartingTurn
    global CurrentTurn

    CurrentShell = Shotgun.CheckCurrentShell()
    NextShell = Shotgun.CheckNextShell()

    Shotgun.ShellCount -= 1
    Shotgun.Shotgun.pop(0)

    if Target == "Self":
        if CurrentShell == "Blank":
            GUI("BlankShell", 0)
            Shotgun.BlankShells -= 1

            #print("ShellCount = ", Shotgun.ShellCount) 
            if NextShell != "Empty":
                if CurrentTurn == "Player":
                    print("\n! Player gets another go. !")
                    PlayersTurn()
                    
                if CurrentTurn == "Dealer":
                    print("\n! Dealer gets another go. !")
                    DealersTurn()
            #else:
            #    GUI("Shotgun", "Empty")

            #if CurrentShell == "Blank" and NextShell == "Empty": # This shit does NOT work
            #    if CurrentTurn == "Player":
            #        print("\n! Player goes first next round. !")
            #        StartingTurn = "Player"
            #        
            #    if CurrentTurn == "Dealer":
            #        print("\n! Dealer goes first next round. !")
            #        StartingTurn = "Dealer"
    
    if Target == "Enemy":
        if CurrentShell == "Blank":
            GUI("BlankShell", 0)
            Shotgun.BlankShells -= 1
    
    if Target == "Self" or Target == "Enemy":
        if CurrentShell == "Live":
            GUI("LiveShell", 0)

            Shotgun.LiveShells -= 1

    if Target == "Self":
        if CurrentShell == "Live":
            if CurrentTurn == "Player":
                print("\n! PLAYER LOST A LIFE. !")
                PlayerLives = PlayerLives - 1
                
            if CurrentTurn == "Dealer":
                print("\n! DEALER LOST A LIFE. !")
                DealerLives = DealerLives - 1

    if Target == "Enemy":
        if CurrentShell == "Live":
            if CurrentTurn == "Player":
                print("\n! DEALER LOST A LIFE. !")
                DealerLives = DealerLives - 1
                
            if CurrentTurn == "Dealer":
                print("\n! PLAYER LOST A LIFE. !")
                PlayerLives = PlayerLives - 1

######################################## PLAYER TURNS #########################################

# TODO: Recode to let the player who shot the last bullet in the event that it is a Blank to go first in the next round.
# TODO: ADD ITEMS

def PrintLives():
    if GameMode == 2: # Player 1 VS Player 2.
        print("! Player 1 has", PlayerLives, "lives remaining. !")
        print("! Player 2 has", Player2Lives, "lives remaining. !")
            
    else: # Player 1 VS Dealer.
        print("! You have", PlayerLives, "lives remaining. !")
        print("! The Dealer has", DealerLives, "lives remaining. !")

def PlayersTurn():
    global CurrentTurn

    CurrentTurn = "Player"
    
    #print("\n###DEBUGGING### ! StartingTurn =", StartingTurn, " !")
    #print("\n###DEBUGGING### ! CurrentTurn =", CurrentTurn, " !")
    
    Timer.GameWait("Full") # See function.
    if GameDebug == 1:
        GUI("Shotgun", "Report")
    print("\n### PLAYERS' TURN:")
    PrintLives()

    Timer.GameWait("Short") # See function.
    Outcome = PlayerUI.Turn()
    if GameDebug == 1:
        print("\n###DEBUGGING### Player Turn Outcome:", Outcome)

    if Outcome == "ShootSelf":
        print("\n- You shoot yourself. -")
        ShotTaken("Self")
    elif Outcome == "ShootDealer":
        print("\n- You shoot the Dealer. -")
        ShotTaken("Enemy")
    elif Outcome == "ChoiceFailed":
        PlayersTurn()
    else:
        print("\n! Error. Defaulting to shooting The Dealer. !")
        print("\n- You shoot the Dealer. -")
        ShotTaken("Enemy")

    Shotgun.PredictedChamber.pop(0) # Update Dealer AI's Shotgun Prediction Algorithm

def DealersTurn():
    global CurrentTurn

    CurrentTurn = "Dealer"
    
    #print("\n###DEBUGGING### ! StartingTurn =", StartingTurn, " !")
    #print("\n###DEBUGGING### ! CurrentTurn =", CurrentTurn, " !")

    Timer.GameWait("Full") # See function.
    if GameDebug == 1:
        GUI("Shotgun", "Report")
    print("\n### DEALER'S TURN:")
    PrintLives()

    Timer.GameWait("Short") # See function.
    Timer.WaitTime("Start") # See function.
    Outcome = DAI.Turn(AILevel)

    #Timer.GameWait("Full") # See function.
    if DealerDecisionDebug == 1:
        print("\n###DEBUGGING### Dealer Turn Outcome:", Outcome)
    
    if Outcome == "ShootSelf":
        print("\n- The Dealer shoots itself. -")
        ShotTaken("Self")
        
    if Outcome == "ShootPlayer":
        print("\n- The Dealer shoots you. -")
        ShotTaken("Enemy")

    Shotgun.PredictedChamber.pop(0) # Update Dealer AI's Shotgun Prediction Algorithm