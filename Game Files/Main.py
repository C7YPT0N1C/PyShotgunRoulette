import Shotgun as Shotgun
import LogicManager as LM
import Timer as Timer
import DealerAI as DAI

Debugging = 0

######################################## GAME ROUNDS ########################################
# TODO: Add custom game rounds.

def StartGame(ShotgunBalance): # Define Game Rounds Here.
    LM.GameRound = 0 # Reset Game Rounds.
    LM.GameRounds(3, 4, 5, ShotgunBalance)

######################################## MAIN RUNTIME ########################################

def Options():
    global Debugging

    print("\nDebugging:", Debugging)
    Debugging = input("Do you want to activate Debugging? (0 = No, 1 = Yes): ") # Enable Debugging.
    if Debugging == "1":
        print("! Activating Debugging. !")
        
        print("\nGame Debugging:", LM.GameDebug)
        GameDebug = input("Do you want to enable Game Debugging? (0 = No, 1 = Yes): ") # Enable Game Debugging.
        if GameDebug == "1":
            print("! Enabling Game Debugging. !")
            LM.GameDebug = 1
        elif GameDebug == "0":
            print("! Disabling Game Debugging. !")
            LM.GameDebug = 0
        else:
            print("! Invalid Input. Defaulting to disabling Game Debugging. !")
            LM.GameDebug = 0
        
        print("\nDealer Decision Debugging:", LM.DealerDecisionDebug)
        DealerDecisionDebug = input("Do you want to enable Dealer Decision Debugging? (0 = No, 1 = Yes): ") # Enable Dealer Decision Debugging.
        if DealerDecisionDebug == "1":
            print("! Enabling Dealer Decision Debugging. !")
            LM.DealerDecisionDebug = 1
        elif DealerDecisionDebug == "0":
            print("! Disabling Dealer Decision Debugging. !")
            LM.DealerDecisionDebug = 0
        else:
            print("! Invalid Input. Defaulting to disabling Dealer Decision Debugging. !")
            LM.DealerDecisionDebug = 0

        print("\nDealer Analysis Debugging:", LM.DealerAnalysisDebug)
        DealerAnalysisDebug = input("Do you want to enable Dealer Analysis Debugging? (0 = No, 1 = Yes): ") # Enable Dealer Analysis Debugging.
        if DealerAnalysisDebug == "1":
            print("! Enabling Dealer Analysis Debugging. !")
            LM.DealerAnalysisDebug = 1
        elif DealerAnalysisDebug == "0":
            print("! Disabling Dealer Analysis Debugging. !")
            LM.DealerAnalysisDebug = 0
        else:
            print("! Invalid Input. Defaulting to disabling Dealer Analysis Debugging. !")
            LM.DealerAnalysisDebug = 0

        print("\nShotgun Debugging:", LM.ShotgunDebug)
        ShotgunDebug = input("Do you want to enable Shotgun Debugging? (0 = No, 1 = Yes): ") # Enable Shotgun Debugging.
        if ShotgunDebug == "1":
            print("! Enabling Shotgun Debugging. !")
            LM.ShotgunDebug = 1
        elif ShotgunDebug == "0":
            print("! Disabling Shotgun Debuggingging. !")
            LM.ShotgunDebug = 0
        else:
            print("! Invalid Input. Defaulting to disabling Shotgun Debugging. !")
            LM.ShotgunDebug = 0
        
        print("\n! Returning to Main Menu. !")
    
    elif Debugging == "0":
        print("! Deactivating Debugging. !")
        
        print("! Disabling Game Debugging. !")
        LM.GameDebug = 0
        
        print("! Disabling Dealer Decision Debugging. !")
        LM.DealerDecisionDebug = 0

        print("! Disabling Dealer Analysis Debugging. !")
        LM.DealerAnalysisDebug = 0

        print("! Disabling Shotgun Debuggingging. !")
        LM.ShotgunDebug = 0
    
    else:
        print("! Invalid Input. Defaulting to disabling Debugging. !")
        Debugging = 0
    
    Main()

def Main():
    GameMenu = input("\nMain Menu! (1 = Play Game, 2 = Options): ") # Choose game mode.
    if GameMenu == "1":
        print("\n! Starting Game. !")
        
        ChooseGameMode = input("\nChoose the Game Mode (1 = Player vs Dealer AI, 2 = Player vs Player, 3 = Dealer AI vs Dealer AI): ") # Choose game mode.
        if ChooseGameMode == "2":
            #print("\n! Selecting Player vs Player Game Mode. !")
            #LM.GameMode = 2

           print("\n! Player vs Player Game Mode has not been implemented. Selecting Player vs Dealer AI Game Mode. !")
           LM.GameMode = 1
        if ChooseGameMode == "3":
            print("\n! Selecting Dealer AI vs Dealer AI Game Mode. !")
            LM.GameMode = 3
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
            
        ChooseShotgunBalance = input("\nDo you want the Shotgun to be balanced? (0 = No, 1 = Yes): ") # Choose whether  loading the shotgun is balanced or not.
        if ChooseShotgunBalance == "0":
            print("\n! Starting game with an unbalanced Shotgun. !")
            StartGame(False)
        else:
            print("\n! Starting game with an balanced Shotgun. !")
            StartGame(True)

    else:
        print("\n! Entering Option Menu. !")
        Options()