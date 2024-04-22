import Shotgun
import PlayerUI
import DealerAI as DAI

######################################## DECLARE VARIABLES ########################################

GameMode = 1

#MaxGameRounds = 3
GameRound = 1

AILevel = 1

CurrentTurn = 0

PlayerLives = 3
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
        DAI.Track("System", "Live")
        print("! It was a Live. !")
    if Element == "BlankShell" and Modifier == 0:
        DAI.Track("System", "Blank")
        print("! It was a Blank. !")

    if Element == "PlayerDied" and Modifier == "Player":
        print("\n! PLAYER HAS DIED. !")
    if Element == "PlayerDied" and Modifier == "Dealer":
        print("\n! DEALER HAS DIED. !")

    if Element == "Shotgun":
        if Modifier == "Debug": # Basically cheats.
            print("\n", Shotgun.Shotgun) 
            print("Current Shell Is:", CheckCurrentShell())
            print("Next Shell Is:", CheckNextShell()) 

        if Modifier == "Report": 
            GUI("Shotgun", "Debug") # Basically cheats.
            
            print("\n! There are ", Shotgun.LiveShells, "Live Shells left. !")
            print("! There are ", Shotgun.BlankShells, "Blank Shells left. !")
        
        if Modifier == "Empty":
            print("\n! Chamber Empty, Skipping Turn. !")

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

    if Target == "Self" or Target == "Enemy":
        if CurrentShell == "Live":
            GUI("LiveShell", 0)

            Shotgun.LiveShells -= 1

    if Target == "Self":
        if CurrentShell == "Live":
            if CurrentTurn == "Player":
                print("! PLAYER LOST A LIFE. !")
                PlayerLives = PlayerLives - 1
                
            if CurrentTurn == "Dealer":
                print("! DEALER LOST A LIFE. !")
                DealerLives = DealerLives - 1

    if Target == "Enemy":
        if CurrentShell == "Live":
            if CurrentTurn == "Player":
                print("\n! DEALER LOST A LIFE. !")
                DealerLives = DealerLives - 1
                
            if CurrentTurn == "Dealer":
                print("\n! PLAYER LOST A LIFE. !")
                PlayerLives = PlayerLives - 1

    if Target == "Enemy":
        if CurrentShell == "Blank":
            GUI("BlankShell", 0)
            Shotgun.BlankShells -= 1
    
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

######################################## PLAYER TURNS ########################################

def PrintLives():
    print("! You have", PlayerLives, "lives remaining. !")
    print("! The Dealer has", DealerLives, "lives remaining. !")

def PlayersTurn():
    global CurrentTurn

    CurrentTurn = "Player"

    GUI("Shotgun", "Report")
    print("\n### Player's Turn:")
    PrintLives()

    Outcome = PlayerUI.Turn()
    #print("Outcome is: ", Outcome)

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

def DealersTurn():
    global CurrentTurn

    CurrentTurn = "Dealer"

    GUI("Shotgun", "Report")
    print("\n### Dealer's Turn:")
    PrintLives()

    Outcome = DAI.Turn(AILevel)
    #print("Outcome is: ", Outcome)
    
    if Outcome == "ShootSelf":
        print("\n- The Dealer shoots itself. -")
        ShotTaken("Self")
        
    if Outcome == "ShootPlayer":
        print("\n- The Dealer shoots you. -")
        ShotTaken("Enemy")