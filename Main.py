import Shotgun
import VariableManager as VM
import TurnManager

######################################## GUI ########################################

### KEY ###

# ! = System Announcement
# # = Turn Announcement
# - = Action
# () = System "Thoughts"

### KEY ###

def GUI(Element, Modifier):
    if Element == "LiveShell" and Modifier == 0:
        TurnManager.Track("System", "Live")
        print("\n! It was a Live. !")
    if Element == "BlankShell" and Modifier == 0:
        TurnManager.Track("System", "Blank")
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

        if Modifier == "Report": 
            if VM.Debugging == 2: # Runs if debugging is enabled.
                GUI("Shotgun", "Debug") # Basically cheats.
            
            print("\n! There are ", Shotgun.LiveShells, "Live Shells left. !")
            print("! There are ", Shotgun.BlankShells, "Blank Shells left. !")
        
        if Modifier == "Empty":
            if VM.PlayerLives == 0:
                GUI("PlayerDied", "Player1") # Report that Player died.
            if VM.Player2Lives == 0:
                GUI("PlayerDied", "Player2") # Report that Player died.
            if VM.DealerLives == 0:
                GUI("PlayerDied", "Dealer") # Report that Player died.
                
            print("\n! Shotgun Chamber Empty, Skipping Turn. !")

######################################## GAME STUFF ########################################

def ShotTaken(Target):
    global PlayerLives
    global Player2Lives
    global DealerLives

    CurrentShell = Shotgun.CheckCurrentShell()
    NextShell = Shotgun.CheckNextShell()

    Shotgun.ShellCount -= 1
    Shotgun.Shotgun.pop(0)

    if Target == "Self" or Target == "Enemy":
        if CurrentShell == "Live":
            GUI("LiveShell", 0)
            Shotgun.LiveShells -= 1
        
        if CurrentShell == "Blank":
            GUI("BlankShell", 0)
            Shotgun.BlankShells -= 1

    if Target == "Self":
        if CurrentShell == "Live":
            if CurrentTurn == "Player1":
                if VM.GameMode == 2: # Player 1 VS Player 2.
                    print("\n! PLAYER 1 LOST A LIFE. !")
                else: # Player 1 VS AI.
                    print("\n! YOU LOST A LIFE. !")
                VM.PlayerLives = VM.PlayerLives - 1
            
            if CurrentTurn == "Player2":
                print("\n! PLAYER 2 LOST A LIFE. !")
                VM.Player2Lives = VM.Player2Lives - 1
                
            if CurrentTurn == "Dealer":
                print("\n! THE DEALER LOST A LIFE. !")
                VM.DealerLives = VM.DealerLives - 1

    if Target == "Enemy":
        if CurrentShell == "Live":
            if CurrentTurn == "Player1":
                if VM.GameMode == 2: # Player 1 VS Player 2.
                    print("\n! PLAYER 2 LOST A LIFE. !")
                    VM.Player2Lives = VM.Player2Lives - 1
                else: # Player 1 VS AI.
                    print("\n! THE DEALER LOST A LIFE. !")
                    VM.DealerLives = VM.DealerLives - 1

            if CurrentTurn == "Player2":
                print("\n! PLAYER 1 LOST A LIFE. !")
                VM.PlayerLives = VM.PlayerLives - 1
                
            if CurrentTurn == "Dealer":
                print("\n! YOU LOST A LIFE. !")
                VM.PlayerLives = VM.PlayerLives - 1
    
    if Target == "Self":
        if CurrentShell == "Blank":
            if NextShell != "Empty":
                if CurrentTurn == "Player1":
                    if VM.GameMode == 2: # Player 1 VS Player 2.
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

######################################## GAME TURNS ########################################

def PrintLives():
    if VM.GameMode == 2: # Player 1 VS Player 2.
        print("! Player 1 has", VM.PlayerLives, "lives remaining. !")
        print("! Player 2 has", VM.Player2Lives, "lives remaining. !")
            
    else: # Player 1 VS Dealer.
        print("! You have", VM.PlayerLives, "lives remaining. !")
        print("! The Dealer has", VM.DealerLives, "lives remaining. !")

def PlayerTurn(Player):
    global CurrentTurn

    if Player == 1: # Player 1's Turn.
        CurrentTurn = "Player1"
        
        GUI("Shotgun", "Report")
        
        if VM.GameMode == 2:
            print("\n### Player 1's Turn:")
        else:
            print("\n### Your Turn:")
        
        PrintLives()

        Outcome = TurnManager.Turn(VM.GameMode, CurrentTurn, VM.AILevel)
        #print("Outcome is: ", Outcome)

        if VM.GameMode == 2: # Player 1 VS Player 2.
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

        Outcome = TurnManager.Turn(VM.GameMode, CurrentTurn, VM.AILevel)
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

    ("Shotgun", "Report")

    print("\n### Dealer's Turn:")
    PrintLives()

    Outcome = TurnManager.Turn(VM.GameMode, CurrentTurn, VM.AILevel)
    #print("Outcome is: ", Outcome)
    
    if Outcome == "ShootSelf":
        print("\n- The Dealer shoots itself. -")
        ShotTaken("Self")
        
    if Outcome == "ShootPlayer":
        print("\n- The Dealer shoots you. -")
        ShotTaken("Enemy")

######################################## GAME ROUNDS ########################################

def GameRounds(GameRound, Lives, ShellCount, ShotgunBalance):
    #Shotgun.ShellCount = ShellCount
    #Shotgun.LoadShotgun(ShellCount, GameRound)
    
    if GameRound == 1:
        print("\n##### NEW GAME #####")

        if VM.AILevel == 3:
            print("\n! THE Dealer's AI difficulty IS SET TO 'CHEATER'. THE DEALER WILL NOT GUESS INCORRECTLY. !")

        print("\n##### ROUND 1 #####")
    
    if GameRound == 2:
        print("\n\n##### ROUND 2 #####")
    
    if GameRound == 3:
        print("\n\n##### ROUND 3 #####")

    if GameRound == "End":
        print("\n\n##### GAME OVER #####")
    
    VM.PlayerLives = Lives # Reset Lives
    VM.Player2Lives = Lives
    VM.DealerLives = Lives

    if ShotgunBalance == False:
        Shotgun.LoadShotgun(ShellCount, False)
    else:
        Shotgun.LoadShotgun(ShellCount, True)
    

    ############## Game Turn Loop ##############
    CurrentShell = Shotgun.CheckCurrentShell() # Update current shell

    while CurrentShell != "Empty": # Only runs whilst shotgun has loaded shells.
        CurrentShell = Shotgun.CheckCurrentShell() # Update current shell

        if VM.GameMode == 1: # Player 1 VS Dealer.
            ###### Player 1's Turn ######
            if VM.PlayerLives != 0 and VM.DealerLives != 0 and CurrentShell != "Empty": # Only runs whilst Player 1 or The Dealer isnt dead, and whilst the shotgun has loaded shells.
                PlayerTurn(1) # Calls for Player 1's turn.
            else:
                if VM.PlayerLives == 0:
                    GUI("PlayerDied", "Player1") # Report that Player died.
                if VM.DealerLives == 0:
                    GUI("PlayerDied", "Dealer") # Report that Dealer died.
                if CurrentShell == "Empty":
                    GUI("Shotgun", "Empty") # Report that shotgun chamber is empty.
                break
            ###### Player 1's Turn ######

            ###### Dealer's Turn ######
            if VM.PlayerLives != 0 and VM.DealerLives != 0 and CurrentShell != "Empty": # Only runs whilst Player 1 or The Dealer isnt dead, and whilst the shotgun has loaded shells.
                DealersTurn() # Calls for Player 1's turn.
            else:
                if VM.PlayerLives == 0:
                    GUI("PlayerDied", "Player1") # Report that Player died.
                if VM.DealerLives == 0:
                    GUI("PlayerDied", "Dealer") # Report that Dealer died.
                if CurrentShell == "Empty":
                    GUI("Shotgun", "Empty") # Report that shotgun chamber is empty.
                break
            ###### Dealer's Turn ######
        
        else: # Player 1 VS Player 2.
            ###### Player 1's Turn ######
            if VM.PlayerLives != 0 and VM.Player2Lives != 0 and CurrentShell != "Empty": # Only runs whilst Player 1 or Player 2 isnt dead, and whilst the shotgun has loaded shells.
                PlayerTurn(1) # Calls for Player 1's turn.
            else:
                if VM.PlayerLives == 0:
                    GUI("PlayerDied", "Player1") # Report that Player died.
                if VM.Player2Lives == 0:
                    GUI("PlayerDied", "Player2") # Report that Dealer died.
                if CurrentShell == "Empty":
                    GUI("Shotgun", "Empty") # Report that shotgun chamber is empty.
                break
            ###### Player 1's Turn ######

            ###### Player 2's Turn ######
            if VM.PlayerLives != 0 and VM.Player2Lives != 0 and CurrentShell != "Empty": # Only runs whilst Player 1 or Player 2 isnt dead, and whilst the shotgun has loaded shells.
                PlayerTurn(2) # Calls for Player 1's turn.
            else:
                if VM.PlayerLives == 0:
                    GUI("PlayerDied", "Player1") # Report that Player died.
                if VM.Player2Lives == 0:
                    GUI("PlayerDied", "Player2") # Report that Dealer died.
                if CurrentShell == "Empty":
                    GUI("Shotgun", "Empty") # Report that shotgun chamber is empty.
                break
            ###### Player 2's Turn ######

        ############## Game Turn Loop ##############

def StartGame(ShotgunBalance): # Define Game Rounds Here.
    GameRounds(VM.GameRound, 2, 5, ShotgunBalance)
        
    VM.GameRound += 1
    #GameRounds(VM.GameRound, 2, 5, ShotgunBalance)
    GameRounds(VM.GameRound, 5, 16, ShotgunBalance)

    VM.GameRound += 1
    #GameRounds(VM.GameRound, 2, 5, ShotgunBalance)
    GameRounds(VM.GameRound, 7, 32, ShotgunBalance)

    VM.GameRound = "End"
    GameRounds(VM.GameRound, 0, 0, ShotgunBalance)

######################################## MAIN RUNTIME ########################################

def Main():
    ChooseGameMode = input("Choose the Game Mode (1 = Player vs Dealer AI, 2 = Player 1 vs Player 2): ") # Choose game mode.
    if ChooseGameMode == "2":
        print("\n! Selecting Player 1 vs Player 2 Game Mode. !")
        VM.GameMode = 2
    else:
        print("\n! Selecting Player vs Dealer AI Game Mode. !")
        VM.GameMode = 1

        ChooseAILevel = input("\nChoose The Dealer's AI difficulty (1 = Normal, 2 = Hard (Work In Progress), 3 = CHEATER): ") # Choose the difficulty of the Dealer's AI.
        if ChooseAILevel == "2":
            print("\n! Starting game with 'Hard' Dealer AI diffiiculty. !")
            VM.AILevel = 2
        elif ChooseAILevel == "3":
            print("\n! Starting game with 'CHEATER' Dealer AI diffiiculty. !")
            VM.AILevel = 3
        else:
            print("\n! Starting game with 'Normal' Dealer AI diffiiculty. !")
            VM.AILevel = 1
    
    ChooseAssistanceLevel = input("\nDo you want to enable debugging? (1 = No, 2 = Yes): ") # Enable debugging.
    if ChooseAssistanceLevel == "2":
        print("\n! Enabling debugging. !")
        VM.Debugging = 2
    else:
        print("\n! Disabling debugging. !")
        VM.Debugging = 1

    ChooseShotgunBalance = input("\nDo you want the shotgun to be balanced or not? (1 = No, 2 = Yes): ") # Choose whether the shotgun is loading balanced or not.
    if ChooseShotgunBalance == "1":
        print("\n! Starting game with a unbalanced shotgun. !")
        StartGame(False)
    else:
        print("\n! Starting game with an balanced shotgun. !")
        StartGame(True)

Main()