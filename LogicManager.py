import time

import Shotgun
import PlayerUI
import DealerAI as DAI

######################################## DECLARE VARIABLES ########################################

GameMode = 1

MaxGameRounds = 3
GameRound = 1

AILevel = 1

CurrentTurn = 0

PlayerLives = 3
DealerLives = 3

WaitTime = 2

GameDebug = 0

DealerDecisionDebug = 0
DealerAnalysisDebug = 0

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
        print("! It was a Live. !")
    if Element == "BlankShell" and Modifier == 0:
        print("! It was a Blank. !")

    if Element == "PlayerDied" and Modifier == "Player":
        print("\n! PLAYER HAS DIED. !")
    if Element == "PlayerDied" and Modifier == "Dealer":
        print("\n! DEALER HAS DIED. !")

    if Element == "Shotgun":
        if Modifier == "Debug": # Basically cheats.
            print("\n! Chamber = ", Shotgun.Shotgun, "!")
            print("! Current Shell Is:", CheckCurrentShell(), "!")
            print("! Next Shell Is:", CheckNextShell(), "!") 

        if Modifier == "Report": 
            print("\n! --------------------------------------------------------- !")
            if GameDebug == 1:
                GUI("Shotgun", "Debug") #################################################################################### Basically cheats.

            print("\n! There are", Shotgun.LiveShells, "Live Shells left. !")
            print("! There are", Shotgun.BlankShells, "Blank Shells left. !")
        
        if Modifier == "Empty":
            print("\n! Chamber Empty, Skipping Next Turn. !")

######################################## GAME STUFF ########################################

def CheckCurrentShell(): 
    if Shotgun.Shotgun[0] == "L":
        return "Live"
    if Shotgun.Shotgun[0] == "B":
        return "Blank"
    if Shotgun.Shotgun[0] == "E" or Shotgun.Shotgun[1] == "":
        return "Empty"

def CheckNextShell(): 
    if Shotgun.Shotgun[1] == "L":
        return "Live"
    if Shotgun.Shotgun[1] == "B":
        return "Blank"
    if Shotgun.Shotgun[1] == "E" or Shotgun.Shotgun[1] == "":
        return "Empty"

def ShotTaken(Target):
    global PlayerLives
    global DealerLives

    CurrentShell = CheckCurrentShell()
    NextShell = CheckNextShell()

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
    print("! You have", PlayerLives, "lives remaining. !")
    print("! The Dealer has", DealerLives, "lives remaining. !")

def PlayersTurn():
    global CurrentTurn

    CurrentTurn = "Player"
    
    time.sleep(WaitTime) # Wait WaitTime seconds.
    GUI("Shotgun", "Report")
    print("\n### PLAYERS' TURN:")
    PrintLives()

    time.sleep(WaitTime/2) # Wait WaitTime seconds.
    Outcome = PlayerUI.Turn()
    if GameDebug == 1:
        print("\nPlayer Turn Outcome is:", Outcome)

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

    time.sleep(WaitTime) # Wait WaitTime seconds.
    GUI("Shotgun", "Report")
    print("\n### DEALER'S TURN:")
    PrintLives()

    time.sleep(WaitTime) # Wait WaitTime seconds.
    Outcome = DAI.Turn(AILevel)
    if DealerDecisionDebug == 1:
        print("\nDealer Turn Outcome is:", Outcome)
    
    if Outcome == "ShootSelf":
        print("\n- The Dealer shoots itself. -")
        ShotTaken("Self")
        
    if Outcome == "ShootPlayer":
        print("\n- The Dealer shoots you. -")
        ShotTaken("Enemy")

    Shotgun.PredictedChamber.pop(0) # Update Dealer AI's Shotgun Prediction Algorithm