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
        DAI.Track("System", "Live")
        print("\n! It was a Live. !")
    if Element == "BlankShell" and Modifier == 0:
        DAI.Track("System", "Blank")
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
            print("Current Shell Is:", CheckCurrentShell())
            print("Next Shell Is:", CheckNextShell()) 

        if Modifier == "Report": 
            GUI("Shotgun", "Debug") # Basically cheats.
            
            print("\n! There are ", Shotgun.LiveShells, "Live Shells left. !")
            print("! There are ", Shotgun.BlankShells, "Blank Shells left. !")
        
        if Modifier == "Empty":
            print("\n! Shotgun Chamber Empty, Skipping Turn. !")

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
    global Player2Lives
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
            if CurrentTurn == "Player1":
                if GameMode == 2: # Player 1 VS Player 2.
                    print("\n! PLAYER 1 LOST A LIFE. !")
                else: # Player 1 VS AI.
                    print("\n! YOU LOST A LIFE. !")
                PlayerLives = PlayerLives - 1
            
            if CurrentTurn == "Player2":
                print("\n! PLAYER 2 LOST A LIFE. !")
                Player2Lives = Player2Lives - 1
                
            if CurrentTurn == "Dealer":
                print("\n! THE DEALER LOST A LIFE. !")
                DealerLives = DealerLives - 1

    if Target == "Enemy":
        if CurrentShell == "Live":
            if CurrentTurn == "Player1":
                if GameMode == 2: # Player 1 VS Player 2.
                    print("\n! PLAYER 2 LOST A LIFE. !")
                    Player2Lives = Player2Lives - 1
                else: # Player 1 VS AI.
                    print("\n! THE DEALER LOST A LIFE. !")
                    DealerLives = DealerLives - 1

            if CurrentTurn == "Player2":
                print("\n! PLAYER 1 LOST A LIFE. !")
                PlayerLives = PlayerLives - 1
                
            if CurrentTurn == "Dealer":
                print("\n! YOU LOST A LIFE. !")
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
                if CurrentTurn == "Player1":
                    if GameMode == 2: # Player 1 VS Player 2.
                        print("\n! Player 1 gets another go. !")
                        PlayerTurn(1)
                    else: # Player VS AI.
                        print("\n! You get another go. !")
                        PlayerTurn(1)
                
                if CurrentTurn == "Player2":
                    print("\n! Player 2 gets another go. !")
                    PlayerTurn(2)
                    
                if CurrentTurn == "Dealer":
                    print("\n! The Dealer gets another go. !")
                    DealersTurn()
            #else:
            #    GUI("Shotgun", "Empty")

######################################## PLAYER TURNS ########################################

def PrintLives():
    if GameMode == 2: # Player 1 VS Player 2.
        print("! Player 1 has", PlayerLives, "lives remaining. !")
        print("! Player 2 has", Player2Lives, "lives remaining. !")
            
    else: # Player 1 VS Dealer.
        print("! You have", PlayerLives, "lives remaining. !")
        print("! The Dealer has", DealerLives, "lives remaining. !")

def PlayerTurn(Player):
    global CurrentTurn

    if Player == 1: # Player 1's Turn.
        CurrentTurn = "Player1"
        GUI("Shotgun", "Report")
        
        if GameMode == 2:
            print("\n### Player 1's Turn:")
        else:
            print("\n### Your Turn:")
        
        PrintLives()

        Outcome = PlayerUI.Turn(GameMode, CurrentTurn)
        #print("Outcome is: ", Outcome)

        if GameMode == 2: # Player 1 VS Player 2.
            if Outcome == "ShootPlayer1":
                print("\n- Player 1 shoots themself. -")
                ShotTaken("Self")
            
            elif Outcome == "ShootPlayer2":
                print("\n- Player 1 shoots Player 2. -")
                ShotTaken("Enemy")
            
            else:
                print("\n! Error. Defaulting to shooting Player 2. !")
                print("\n- Player 1 shoots Player 2. -")
                ShotTaken("Enemy")
        
        else: # Player VS AI.
            if Outcome == "ShootPlayer1":
                print("\n- You shoot yourself. -")
                ShotTaken("Self")
            
            elif Outcome == "ShootDealer":
                print("\n- You shoot The Dealer. -")
                ShotTaken("Enemy")
            
            else:
                print("\n! Error. Defaulting to shooting The Dealer. !")
                print("\n- You shoot The Dealer. -")
                ShotTaken("Enemy")
                
        if Outcome == "ChoiceFailed":
            PlayerTurn(1)
            
    if Player == 2: # Player 2's Turn.
        CurrentTurn = "Player2"

        GUI("Shotgun", "Report")
        print("\n### Player 2's Turn:")
        PrintLives()

        Outcome = PlayerUI.Turn(GameMode, CurrentTurn)
        #print("Outcome is: ", Outcome)

        if Outcome == "ShootPlayer2":
            print("\n- Player 2 shoots themself. -")
            ShotTaken("Self")
        elif Outcome == "ShootPlayer1":
            print("\n- Player 2 shoots Player 1. -")
            ShotTaken("Enemy")
        elif Outcome == "ChoiceFailed":
            PlayerTurn(1)
        else:
            print("\n! Error. Defaulting to shooting Player 1. !")
            print("\n- Player 2 shoots Player 1. -")
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