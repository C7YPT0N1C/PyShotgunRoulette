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

ChancePerShell = 0 # Chance for a shell to be shot.
BlankChance = 0 # Chance for a blank shell to be shot.
LiveChance = 0 # Chance for a live shell to be shot.

######################################## DEBUG STUFF ########################################

def Debug(): # Print variables.
    global ChancePerShell
    global LiveChance
    global BlankChance

    print("\nBlank Shells:", Shotgun.BlankShells, "\nBlankChance:", BlankChance, "%")
    print("Live Shells:", Shotgun.LiveShells, "\nLiveChance:", LiveChance, "%")
    print("Chance Per Shell = ", ChancePerShell)

######################################## DECISION STUFF ########################################

def AnalyseDecision(Decision):
    global AnalysisReturnMin
    global AnalysisReturnMax

    Prediction = Shotgun.PredictedChamber[0] # Store Value

    if LM.DealerAnalysisDebug == 1:
        print("\n-------Shotgun = ", Shotgun.Shotgun)
        print("Dealer Shotgun = ", Shotgun.PredictedChamber)

    if Shotgun.PredictedChamber[0] == Shotgun.Shotgun[0]:
        if LM.DealerAnalysisDebug == 1:
            print("! GENERATION CORRECT !")

    else:
        if LM.DealerAnalysisDebug == 1:
            print("! GENERATION INCORRECT !")

        Shotgun.PredictShotgun(Shotgun.ShellCount, True)
    
    if Shotgun.LiveShells == 0: # If the remaining shells are blank, shoot self.
        return "ShootSelf" # Return decision.
    
    elif Shotgun.BlankShells == 0: # If the remaining shells are live, shoot player.
        return "ShootPlayer" # Return decision.
    
    else:
        if Decision == "Blank":
            if Prediction == "B":
                if LM.DealerAnalysisDebug == 1:
                    print("\n(After analysing, The Dealer thinks it is Blank. The Dealer is sure of its decision.)")
                return "ShootSelf" # Return decision.
            if Prediction == "L":
                if LM.DealerAnalysisDebug == 1:
                    print("\n(After analysing, The Dealer thinks it is Blank. The Dealer is unsure of its decision and changes its mind.)")
                return "ShootPlayer" # Return decision.

        if Decision == "Live":
            if Prediction == "B":
                if LM.DealerAnalysisDebug == 1:
                    print("\n(After analysing, The Dealer thinks it is Live. The Dealer is unsure of its decision and changes its mind.)")
                return "ShootSelf" # Return decision.
            if Prediction == "L":
                if LM.DealerAnalysisDebug == 1:
                    print("\n(After analysing, The Dealer thinks it is Live. The Dealer is sure of its decision.)")
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
            if LM.DealerDecisionDebug == 1:
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