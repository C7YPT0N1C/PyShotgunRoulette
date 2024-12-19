import random

import LogicManager as LM
import Shotgun

######################################## NOTES ########################################

######## AI Levels ########
# Level 1: AI decides purely on odds. Does not predict future turns.
# Level 2: AI calculates based on odds, and uses player's and its own previous decisions to make guesses on its own next move.

######## HOW THE AI WORKS ########
# Main.py calls for Dealer's turn.
# Turn() receieves Main.py's call.

# If AILevel = 1, Turn() analyses probabilities.

# If AILevel = 2, Turn() analyses probabilities and pushes the decision to AnalyseDecision() (either "Live" or "Blank").
# AnalyseDecision() receieves Turn()'s call.
# AnalyseDecision() checks the chamber prediction and saved the value of the first shell (Prior to the game starting, Shotgun.py generates a prediction of what the chamber is, along with the chamber itself).
# AnalyseDecision() checks the value of the stored shell. If only blanks or only lives remain, The Dealer will decide accordingly. If there is at least 1 of each type of shell, The Dealer makes a decision based on the predicted chamber.
# AnalyseDecision() returns the analysis to Turn().
# AnalyseDecision() checks if the chamber prediction was correct after The Dealer takes its turn. If correct, continue to use prediction. If incorrect, generate a new prediction. This is done AFTER The Dealer's turn to prevent it from actually cheating.

# If AILevel = 3, The Dealer can check what the current shell is (it cheats lol).

# Turn() returns The Dealer's turn to Main.py.
# Main.py updates LogicManager of Dealer's decision.
# LogicManager updates the game.

######################################## DECLARE VARIABLES ########################################

ChancePerShell = 0 # Chance for a shell to be shot. Kinda arbitrary.
BlankChance = 0 # Chance for a Blank shell to be shot.
LiveChance = 0 # Chance for a Live shell to be shot.

######################################## DEBUG STUFF ########################################

def Debug(): # Print variables.
    global ChancePerShell
    global LiveChance
    global BlankChance

    print("\nBlank Shells:", Shotgun.BlankShells, "\nBlankChance:", BlankChance, "%")
    print("\nLive Shells:", Shotgun.LiveShells, "\nLiveChance:", LiveChance, "%")
    print("\nChance Per Shell = ", ChancePerShell)

######################################## DECISION STUFF ########################################

def AnalyseDecision(Decision):
    global AnalysisReturnMin
    global AnalysisReturnMax

    Prediction = Shotgun.PredictedChamber[0] # Store value for comparison.

    if LM.DealerAnalysisDebug == 1: # Print if DealerAnalysisDebug is enabled.
        print("\n--Current Shotgun Chamber = ", Shotgun.Shotgun)
        print("Predicted Shotgun Chamber = ", Shotgun.PredictedChamber)

    if Shotgun.PredictedChamber[0] == Shotgun.Shotgun[0]: # Check if Shotgun Chamber Prediction is correct.
        if LM.DealerAnalysisDebug == 1:
            if Shotgun.BlankShells != 0 and Shotgun.LiveShells != 0: # Print if there is at least 1 of each type of shell left.
                print("! GENERATION CORRECT !")
    
    else: # If Shotgun Chamber Prediction is incorrect.
        if LM.DealerAnalysisDebug == 1:
            if Shotgun.BlankShells != 0 and Shotgun.LiveShells != 0: # Print if there is at least 1 of each type of shell left.
                print("! GENERATION INCORRECT !")

        Shotgun.PredictShotgun(Shotgun.ShellCount, True) # If Shotgun Chamber Prediction is incorrect, regenerate prediction.

    if Shotgun.BlankShells != 0 and Shotgun.LiveShells == 0: # Print if there only Blank Shells left.
        print("! (Prediction N/A, Only Blank Shells Remain.) !")
    elif Shotgun.BlankShells == 0 and Shotgun.LiveShells != 0: # Print if there only Live Shells left.
        print("! (Prediction N/A, Only Live Shells Remain.) !")
  
    ########################################

    if Shotgun.BlankShells == 0: # If the remaining shells are live, shoot player.
        return "ShootPlayer" # Return decision.  
    elif Shotgun.LiveShells == 0: # If the remaining shells are blank, shoot self.
        return "ShootSelf" # Return decision.
    else:
        if Decision == "Blank":
            if Prediction == "B":
                print("\n(The Dealer thinks it's Blank.) \n(After analysing, The Dealer is sure of its initial decision.)")
                return "ShootSelf" # Return decision.
            if Prediction == "L":
                print("\n(The Dealer thinks it's Blank.) \n(After analysing, The Dealer changes its mind.)")
                return "ShootPlayer" # Return decision.

        if Decision == "Live":
            if Prediction == "B":
                print("\n(The Dealer thinks it's Live.) \n(After analysing, The Dealer changes its mind.)")
                return "ShootSelf" # Return decision.
            if Prediction == "L":
                print("\n(The Dealer thinks it's Live.) \n(After analysing, The Dealer is sure of its initial decision.)")
                return "ShootPlayer" # Return decision.

def Turn(AILevel):
    global ChancePerShell
    global BlankChance
    global LiveChance
    
    #MaxChoices = 3

    #ChanceShootAI = random.randint(1, MaxChoices)
    #ChanceShootPlayer = random.randint(1, MaxChoices)
    #ChanceUseItem = random.randint(1, MaxChoices)

    ChancePerShell = int(100 / (Shotgun.LiveShells + Shotgun.BlankShells)) # Calculate chance for a shell to be shot.
    BlankChance = (ChancePerShell * Shotgun.BlankShells) # Calculate chance for a blank shell to be shot.
    #BlankChance = ((ChancePerShell * Shotgun.BlankShells) + 1) # Calculate chance for a blank shell to be shot.
    LiveChance = (ChancePerShell * Shotgun.LiveShells) # Calculate chance for a live shell to be shot.
    #LiveChance = ((ChancePerShell * Shotgun.LiveShells) + 1) # Calculate chance for a live shell to be shot.

    if LM.DealerDecisionDebug == 1:
        Debug() # Print debug.

    #Outcome = 0

    if AILevel == 1:
        if BlankChance > LiveChance: # If shell more likely to be a blank, shoot player.
            return "ShootSelf" # Return decision.
        
        if LiveChance > BlankChance: # If shell more likely to be a live, shoot player.
            return "ShootPlayer" # Return decision.
        
        if LiveChance == BlankChance: # If shell equally likely to be a live or a blank, choose randomly.
            RandomChoice = random.randint(0,1)
            if LM.DealerDecisionDebug == 1: # Print if DealerDecisionDebug is enabled.
               if RandomChoice == 0:
                   print("\nRandom Choice = Blank")
               if RandomChoice == 1:
                   print("\nRandom Choice = Live")

            if RandomChoice == 0:
                return "ShootSelf"
            if RandomChoice == 1:
                return "ShootPlayer"
    
    if AILevel == 2:
        if BlankChance > LiveChance: # If shell more likely to be a blank, analyse chance of shell being a blank.
            if LM.DealerDecisionDebug == 1:
                print("\n(Initial Choice: Blank.)")
            
            return AnalyseDecision("Blank") # See function.

        if LiveChance > BlankChance: # If shell more likely to be a live, analyse chance of shell being a live.
            if LM.DealerDecisionDebug == 1:
                print("\n(Initial Choice: Live.)")
            
            return AnalyseDecision("Live") # See function.
        
        if LiveChance == BlankChance: # If shell equally likely to be a live or a blank, analyse chances.
            if LM.DealerDecisionDebug == 1:
                print("\n(Initial Choice: Equal Chance.)")
            
            RandomChoice = random.randint(0,1)
            if RandomChoice == 0: # "A Blank" randomly chosen.
                if LM.DealerDecisionDebug == 1:
                    print("\n(Random Guess: Blank.)")
                
                return AnalyseDecision("Blank") # See function.
            
            if RandomChoice == 1: # "A Live" randomly chosen.
                if LM.DealerDecisionDebug == 1:
                    print("\n(Random Guess: Live.)")
                
                return AnalyseDecision("Live") # See function.    
    
    if AILevel == 3:
        if Shotgun.Shotgun[0] == "B":
            return "ShootSelf"
        if Shotgun.Shotgun[0] == "L":
            return "ShootPlayer"

######################################## TESTING STUFF ########################################