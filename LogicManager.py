import time

import Shotgun
import PlayerUI
import DealerAI as DAI

######################################## DECLARE VARIABLES ########################################

GameMode = 1

MaxGameRounds = 3
GameRound = 1

AILevel = 1

StartingTurn = 0
CurrentTurn = 0

WaitTime = 1.5 # Make code wait WaitTime seconds. Makes output more readable while playing.
def Wait():
    time.sleep(WaitTime) # Wait WaitTime seconds. Makes output more readable while playing.

PlayerLives = 3
DealerLives = 3

GameDebug = 0

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
            print("\n! Chamber =", Shotgun.Shotgun, "!")
            print("! Current Shell Is:", Shotgun.CheckCurrentShell(), ". !")
            print("! Next Shell Is:", Shotgun.CheckNextShell(), ". !") 

        if Modifier == "Report": 
            print("\n! --------------------------------------------------------- !")
            if GameDebug == 1:
                GUI("Shotgun", "Debug") #################################################################################### Basically cheats.

            print("\n! There are", Shotgun.LiveShells, "Live Shells left. !")
            print("! There are", Shotgun.BlankShells, "Blank Shells left. !")
        
        if Modifier == "Empty":
            print("\n! Chamber Empty, Skipping Next Turn. !")

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
    print("! You have", PlayerLives, "lives remaining. !")
    print("! The Dealer has", DealerLives, "lives remaining. !")

def PlayersTurn():
    global CurrentTurn

    CurrentTurn = "Player"
    
    #print("\n######DEBUGGING###### ! StartingTurn =", StartingTurn, " !")
    #print("\n######DEBUGGING###### ! CurrentTurn =", CurrentTurn, " !")
    
    Wait()
    GUI("Shotgun", "Report")
    print("\n### PLAYERS' TURN:")
    PrintLives()

    time.sleep(WaitTime/2) # Wait WaitTime seconds. Makes output more readable while playing.
    Outcome = PlayerUI.Turn()
    if GameDebug == 1:
        print("\n######DEBUGGING###### Player Turn Outcome:", Outcome)

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
    
    #print("\n######DEBUGGING###### ! StartingTurn =", StartingTurn, " !")
    #print("\n######DEBUGGING###### ! CurrentTurn =", CurrentTurn, " !")

    Wait()
    GUI("Shotgun", "Report")
    
    Wait()
    print("\n### DEALER'S TURN:")
    PrintLives()

    Wait()
    print("\n(The Dealer is thinking...)")

    Outcome = DAI.Turn(AILevel)

    DealerWaitTime = DAI.WaitTime("End")
    time.sleep(DealerWaitTime) # Wait DealerWaitTime seconds. Makes output more readable while playing and makes it look like the Dealer is "thinking".

    if DAI.DealerDecisionDebug == 1:
        print("\n######DEBUGGING###### Dealer Turn Outcome:", Outcome)
    
    if Outcome == "ShootSelf":
        print("\n- The Dealer shoots itself. -")
        ShotTaken("Self")
        
    if Outcome == "ShootPlayer":
        print("\n- The Dealer shoots you. -")
        ShotTaken("Enemy")

    Shotgun.PredictedChamber.pop(0) # Update Dealer AI's Shotgun Prediction Algorithm