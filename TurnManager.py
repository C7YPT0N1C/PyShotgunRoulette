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
    print("\nLive Chance:", LiveChance, "%.")
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

######################################## DECISION STUFF ########################################

######################################## GAME TURN STUFF ########################################

def PlayerTurn(GameMode, CurrentTurn):
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

######################################## GAME TURN STUFF ########################################

######################################## DEALER AI ########################################

def DealerChoice(Choice):
    AILevel = VM.AILevel

    if Choice == "Live":
        if VM.Debugging == 2: # Runs if debugging is enabled.
            print("\n(The Dealer's thought: a Live.)")
            
        if AILevel == 1: # "Normal" AI.
            return "ShootPlayer" # Return decision.
        if AILevel == 2: # "Hard" AI.
            Decision = DealerAnalysis.Analyse("Live") # Analyse past turns for the chance of the shell being a Live.
            return Decision
    
    if Choice == "Blank":
        if VM.Debugging == 2: # Runs if debugging is enabled.
            print("\n(The Dealer's thought: a Blank.)")
            
        if AILevel == 1: # "Normal" AI.
            return "ShootSelf" # Return decision.
        if AILevel == 2: # "Hard" AI.
            Decision = DealerAnalysis.Analyse("Live") # Analyse past turns for the chance of the shell being a Blank.
            return Decision

def DealerTurn():
    global ChancePerShell
    global LiveChance
    global BlankChance

    AILevel = VM.AILevel
    
    LiveChance = ((Shotgun.LiveShells / (Shotgun.LiveShells + Shotgun.BlankShells)) * 100) # Calculate chance for a live shell to be shot.
    BlankChance = ((Shotgun.BlankShells / (Shotgun.LiveShells + Shotgun.BlankShells)) * 100) # Calculate chance for a blank shell to be shot.

    if VM.Debugging == 2: # Runs if debugging is enabled.
        Debug() # Print debug.

    if LiveChance > BlankChance: # If shell more likely to be a live, shoot player.
        return DealerChoice("Live")

    if BlankChance > LiveChance: # If shell more likely to be a blank, shoot player.
        return DealerChoice("Blank")
    
    if LiveChance == BlankChance: # If shell equally likely to be a live or a blank, choose randomly.
        RandomChoice = random.randint(0,1)
        if VM.Debugging == 2: # Runs if debugging is enabled.
            print("\n(After calculating the odds, The Dealer thinks it is an equal chance.)")
            print("Random Choice = ", RandomChoice)

        if RandomChoice == 0: # "A Live" randomly chosen.
            return DealerChoice("Live")
        
        if RandomChoice == 1: # "A Blank" randomly chosen.
            return DealerChoice("Blank")
    
    if AILevel == 3: # "Cheater" AI.
        CurrentShell = Shotgun.CheckCurrentShell()
        if CurrentShell == "Live":
            return "ShootPlayer"
        if CurrentShell == "Blank":
            return "ShootSelf"

######################################## DEALER AI ########################################