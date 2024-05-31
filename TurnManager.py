import random

import Shotgun
import VariableManager as VM
import DealerAnalysis

######################################## DECLARE VARIABLES ########################################

AnalysisReturnMax = 100 # Minimum result of analysis for a positive to be returned. (Default = 100).
AnalysisReturnMin = 50 # Minimum result of analysis for a positive to be returned. (Default = 50).
AnalysisResultBuffer = 25

ChancePerShell = 0 # Chance for a shell to be shot.
LiveChance = 0 # Chance for a live shell to be shot.
BlankChance = 0 # Chance for a blank shell to be shot.

######################################## DEBUG STUFF ########################################

def Debug(): # Print variables.
    if Shotgun.LiveShells != 0 and Shotgun.BlankShells != 0: # Avoid Divide By Zero Error
            ChancePerShell = int(100 / (Shotgun.LiveShells + Shotgun.BlankShells)) # Calculate chance for a shell to be shot.
            LiveChance = ((Shotgun.LiveShells / (Shotgun.LiveShells + Shotgun.BlankShells)) * 100) # Calculate chance for a live shell to be shot.
            BlankChance = ((Shotgun.BlankShells / (Shotgun.LiveShells + Shotgun.BlankShells)) * 100) # Calculate chance for a blank shell to be shot.
    else:
        ChancePerShell = "! Chamber Empty !"
        LiveChance = "! Chamber Empty !"
        BlankChance = "! Chamber Empty !"
    
    print("\nChance Per Shell = ", ChancePerShell)
    print("Live Chance:", LiveChance, "%.")
    print("Blank Chance:", BlankChance, "%.")

def AnalysisPrint(): # Prints the lists.
    print("\nPlayer Decisions: ", DealerAnalysis.PlayerDecisions)
    print("Dealer Decisions: ", DealerAnalysis.DealerDecisions)
    print("Correct Decisions: ", DealerAnalysis.CorrectDecision)

######################################## DECISION STUFF ########################################

def Track(Target, Decision): # Updates lists as decisions are made and shells are shot.
    if Target == "Dealer":
        if Decision == "Live":
            DealerAnalysis.DealerDecisions.append("L")
            DealerAnalysis.PlayerDecisions.append("-")
        if Decision == "Blank":
            DealerAnalysis.DealerDecisions.append("B")
            DealerAnalysis.PlayerDecisions.append("-")

    if Target == "System":
        if Decision == "Live":
            DealerAnalysis.CorrectDecision.append("L")
        if Decision == "Blank":
            DealerAnalysis.CorrectDecision.append("B")

def ReturnDecision(Decision):
    Analysis = DealerAnalysis.Analyse(Decision) # Analyse past turns.
    
    if VM.Debugging == 2: # Runs if debugging is enabled.
        print("Analysis = ", Analysis) # Print the results of the analysis.

    return Analysis # Return decision.

def DealerChoice(Choice, AILevel):
    if Choice == "Live":
        if VM.Debugging == 2: # Runs if debugging is enabled.
            print("\n(The Dealer's thought: a Live.)")
            
        if AILevel == 1:
            return "ShootPlayer" # Return decision.
        if AILevel == 2: # Analyse chance of shell being a Live.
            return ReturnDecision("Live") # See function.
    
    if Choice == "Blank":
        if VM.Debugging == 2: # Runs if debugging is enabled.
            print("\n(The Dealer's thought: a Blank.)")
            
        if AILevel == 1:
            return "ShootSelf" # Return decision.
        if AILevel == 2: # Analyse chance of shell being a Blank.
            return ReturnDecision("Blank") # See function.

######################################## GAME TURN STUFF ########################################

def Turn(GameMode, CurrentTurn, AILevel):
    if CurrentTurn == "Player1":
        if GameMode == 2: # Player 1 VS Player 2.
            Decision = input("\n##### Shoot Player 2 or Yourself? (1 = Player 2, 2 = Yourself): ")
            if Decision == "1":
                Outcome = "ShootPlayer2"
                return Outcome
            if Decision == "2":
                Outcome = "ShootPlayer1"
                return Outcome
            else:
                return "ChoiceFailed"
        
        else: # Player 1 VS Dealer.
            Decision = input("\n##### Shoot The Dealer or Yourself? (1 = The Dealer, 2 = Yourself): ")
            if Decision == "1":
                Outcome = "ShootDealer"
                return Outcome
            if Decision == "2":
                Outcome = "ShootPlayer1"
                return Outcome
            else:
                return "ChoiceFailed"
            
    if GameMode == 2: # Player 1 VS Player 2.
        if CurrentTurn == "Player2":
            Decision = input("\n##### Shoot Player 1 or Yourself? (1 = Player 1, 2 = Yourself): ")
            if Decision == "1":
                Outcome = "ShootPlayer1"
                return Outcome
            if Decision == "2":
                Outcome = "ShootPlayer2"
                return Outcome
            else:
                return "ChoiceFailed"
    
######################################## DEALER AI ########################################

    ######## AI Levels ########
    # Level 1: AI decides purely on odds. Does not predict future turns.
    # Level 2: AI calculates based on odds, and uses player's and its own previous decisions to make guesses on its own next move.

    ######## HOW THE AI WORKS ########
    # Main.py calls for Dealer's turn.
    # Turn() receieves Main.py's call.
    # If AILevel = 1, Turn() analyses chances and returns its decision.
    # If AILevel = 2, Turn() analyses chances and returns its decision to ReturnDecision() (either "Live" or "Blank").
    # ReturnDecision() receieves Turn()'s call.
    # ReturnDecision() calls Track() to update the list of moves made (see Track() function for details)
    # ReturnDecision() returns Turn()'s call to Analyse().
    # Analyse() recieves ReturnDecision()'s call.
    # Analyse() analyses the past moves kept updated by Track() (see Analyse() function for details).
    # Analyse() returns the results of the analysis to ConfirmAnalysis().
    # ConfirmAnalysis() recieves Analyse()'s call.
    # ConfirmAnalysis() checks the value of Analyse()'s call (the results of the analysis) to ensure that it is within the range laid out by the variables "AnalysisReturnMin" and "AnalysisReturnMax".
    # ConfirmAnalysis() compares the value of Analyse()'s call (the results of the analysis) to see whether it is bigger than or equal to the variable "BlankChance" in the event that Turn() returned "Live", or whether it is bigger than or equal to the variable "LiveChance" in the event that Turn() returned "Blank".
    # If ConfirmAnalysis() comfirms either of these statements are true, ConfirmAnalysis() will return the decision equal to Turn()'s return. Otherwise, return the opposite decision and update Track().
    # ConfirmAnalysis() returns its decision to Main.py.
    # Main.py updates LogicManager of Dealer's decision.
    # LogicManager updates the game.
    
    if CurrentTurn == "Dealer": # Dealer AI Stuff
        global ChancePerShell
        global LiveChance
        global BlankChance
        
        #MaxChoices = 3

        #ChanceShootAI = random.randint(1, MaxChoices)
        #ChanceShootPlayer = random.randint(1, MaxChoices)
        #ChanceUseItem = random.randint(1, MaxChoices)

        if VM.Debugging == 2: # Runs if debugging is enabled.
            Debug() # Print debug.

        #Outcome = 0

        if LiveChance > BlankChance: # If shell more likely to be a live, shoot player.
            DealerChoice("Live", AILevel)

        if BlankChance > LiveChance: # If shell more likely to be a blank, shoot player.
            DealerChoice("Blank", AILevel)
        
        if LiveChance == BlankChance: # If shell equally likely to be a live or a blank, choose randomly.
            RandomChoice = random.randint(0,1)
            if VM.Debugging == 2: # Runs if debugging is enabled.
                print("\n(After calculating the odds, The Dealer thinks it is an equal chance.)")
                print("Random Choice = ", RandomChoice)

            if RandomChoice == 0: # "A Live" randomly chosen.
                DealerChoice("Live", AILevel)
            
            if RandomChoice == 1: # "A Blank" randomly chosen.
                DealerChoice("Blank", AILevel)
        
        if AILevel == 3: # "Cheater" AI.
            CurrentShell = Shotgun.CheckCurrentShell()
            if CurrentShell == "Live":
                return "ShootPlayer" # Return decision.
            if CurrentShell == "Blank":
                return "ShootSelf" # Return decision.
######################################## DEALER AI ########################################