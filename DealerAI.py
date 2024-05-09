import random
import Shotgun

import VariableManager as VM
import DealerAnalysis

######################################## NOTES ########################################

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

######################################## DECLARE VARIABLES ########################################

AnalysisReturnMax = 100 # Minimum result of analysis for a positive to be returned. (Default = 100).
AnalysisReturnMin = 50 # Minimum result of analysis for a positive to be returned. (Default = 50).
AnalysisResultBuffer = 25

ChancePerShell = 0 # Chance for a shell to be shot.
LiveChance = 0 # Chance for a live shell to be shot.
BlankChance = 0 # Chance for a blank shell to be shot.

######################################## DEBUG STUFF ########################################

def Debug(): # Print variables.
    print("\nChance Per Shell = ", ChancePerShell)
    print("Live Chance:", LiveChance, "%.")
    print("Blank Chance:", BlankChance, "%.")

def AnalysisPrint(): # Prints the lists.
    print("\nPlayer Decisions: ", DealerAnalysis.PlayerDecisions)
    print("Dealer Decisions: ", DealerAnalysis.DealerDecisions)
    print("Correct Decisions: ", DealerAnalysis.CorrectDecision)

######################################## DECISION TRACKER STUFF ########################################

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

def ReturnDecision(Decision):
    Analysis = DealerAnalysis.Analyse(Decision) # Analyse past turns.
    
    if VM.Debugging == 2: # Runs if debugging is enabled.
        print("Analysis = ", Analysis) # Print the results of the analysis.

    return Analysis # Return decision.

def Turn(AILevel):
    global ChancePerShell
    global LiveChance
    global BlankChance
    
    #MaxChoices = 3

    #ChanceShootAI = random.randint(1, MaxChoices)
    #ChanceShootPlayer = random.randint(1, MaxChoices)
    #ChanceUseItem = random.randint(1, MaxChoices)

    ChancePerShell = int(100 / (Shotgun.LiveShells + Shotgun.BlankShells)) # Calculate chance for a shell to be shot.
    LiveChance = ((Shotgun.LiveShells / (Shotgun.LiveShells + Shotgun.BlankShells)) * 100) # Calculate chance for a live shell to be shot.
    BlankChance = ((Shotgun.BlankShells / (Shotgun.LiveShells + Shotgun.BlankShells)) * 100) # Calculate chance for a blank shell to be shot.

    if VM.Debugging == 2: # Runs if debugging is enabled.
        Debug() # Print debug.

    #Outcome = 0

    if AILevel == 3: # "Cheater" AI.
        CurrentShell = Shotgun.CheckCurrentShell()
        if CurrentShell == "Live":
            return "ShootPlayer" # Return decision.
        if CurrentShell == "Blank":
            return "ShootSelf" # Return decision.
    
    if BlankChance > LiveChance: # If shell more likely to be a blank, shoot player.
        print("\n(The Dealer's initial thought: a Blank.)")
        
        if AILevel == 1:
            return "ShootSelf" # Return decision.


    if LiveChance > BlankChance: # If shell more likely to be a live, shoot player.
        if VM.Debugging == 2: # Runs if debugging is enabled.
            print("\n(The Dealer's initial thought: a Live.)")
        
        if AILevel == 1:
            return "ShootPlayer" # Return decision.
        if AILevel == 2: # Analyse chance of shell being a Live.
            return ReturnDecision("Live") # See function.
    
    if BlankChance > LiveChance: # If shell more likely to be a blank, shoot player.
        if VM.Debugging == 2: # Runs if debugging is enabled.
            print("\n(The Dealer's initial thought: a Blank.)")
        
        if AILevel == 1:
            return "ShootSelf" # Return decision.
        if AILevel == 2: # Analyse chance of shell being a Blank.
            return ReturnDecision("Blank") # See function.
    
    if LiveChance == BlankChance: # If shell equally likely to be a live or a blank, choose randomly.
        if VM.Debugging == 2: # Runs if debugging is enabled.
            print("\n(After calculating the odds, The Dealer thinks it is an equal chance.)")
        
        RandomChoice = random.randint(0,1)
        
        if VM.Debugging == 2:
            print("Random Choice = ", RandomChoice)

        if RandomChoice == 0: # "A Live" randomly chosen.
            if VM.Debugging == 2:
                print("\n(The Dealer's initial thought: a Live.)")
            
            if AILevel == 1:
                return "ShootPlayer" # Return decision.
            if AILevel == 2:
                return ReturnDecision("Live") # See function.
        
        if RandomChoice == 1: # "A Blank" randomly chosen.
            if VM.Debugging == 2:
                print("\n(The Dealer's initial thought: a Blank.)")
            
            if AILevel == 1:
                return "ShootSelf" # Return decision.
            if AILevel == 2:
                return ReturnDecision("Blank") # See function.