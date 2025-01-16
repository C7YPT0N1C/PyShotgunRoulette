import glob
import random

import LogicManager as LM
import Shotgun

import time
#WaitTime = 2


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

DealerDecisionDebug = 0
DealerAnalysisDebug = 0

WaitTimeDebug = 0

StartTime = 0
EndTime = 0
RunTime = 0

######################################## MISC ########################################

def Debug(): # Print variables.
    global ChancePerShell
    global LiveChance
    global BlankChance

    #print("\nBlank Shells:", Shotgun.BlankShells, "\nBlankChance:", BlankChance, "%")
    #print("\nLive Shells:", Shotgun.LiveShells, "\nLiveChance:", LiveChance, "%")
    #print("\nChance Per Shell = ", ChancePerShell)

    print("\n######DEBUGGING###### Blank Shells:", Shotgun.BlankShells, "| Live Shells:", Shotgun.LiveShells)
    print("######DEBUGGING###### BlankChance:", BlankChance, "% | LiveChance:", LiveChance, "%")
    print("######DEBUGGING###### Chance Per Shell = ", ChancePerShell)

    #print("\n######DEBUGGING###### TEXT") # TEMPLATE

######## HOW WaitTime WORKS ########
# TODO

def WaitTime(Operation):  # Accept StartTime as a parameter
    global StartTime
    global EndTime

    global RunTime
    
    if Operation == "Start":
        RunTime = 0
        if WaitTimeDebug == 1:
            print("\n######DEBUGGING###### ! WARNING: TOTAL WAIT TIME RESET. Run Time:", RunTime, "s. !")

        StartTime = 0
        EndTime = 0
        
        if WaitTimeDebug == 1:
            print("\n######DEBUGGING###### ! WARNING: WAITING STARTED. !")
        StartTime = time.perf_counter()
    
    if Operation == "End":
        EndTime = time.perf_counter()
        
        if WaitTimeDebug == 1:
            print("\n######DEBUGGING###### ! StartTime =", StartTime, "s. !")
            print("######DEBUGGING###### ! EndTime =", EndTime, "s. !")

        RunTime = EndTime - StartTime
        if WaitTimeDebug == 1:
            print("\n######DEBUGGING###### ! WARNING: WAITING ENDED. Run time:", RunTime, "s. !")
            print("\n######DEBUGGING###### ! WARNING: RETURNING TOTAL TIME. Run time:", RunTime, "s. !")

        ########################################
        
        RunTimeCap = 0.5
        RunTimeMultiplyer = 5

        if WaitTimeDebug == 1:
            print("\n######DEBUGGING###### ! RunTimeCap =", RunTimeCap, "!")
        while RunTime >= 0 and RunTime <= RunTimeCap:
            RunTime = RunTime * RunTimeMultiplyer
            if WaitTimeDebug == 1:
                print("######DEBUGGING###### ! UPDATED Run time:", RunTime, "s. !")
        
        ########################################

        if LM.AILevel == 1:
            if WaitTimeDebug == 1:
                print("\n######DEBUGGING###### ! Returning Total Time as:", RunTime, "s. !")
            return RunTime
        if LM.AILevel == 2:
            if WaitTimeDebug == 1:
                print("\n######DEBUGGING###### ! Returning Total Time as:", RunTime, "s. !")
            return (RunTime)
        if LM.AILevel == 3:
            if WaitTimeDebug == 1:
                print("\n######DEBUGGING###### ! Returning Total Time as:", RunTime, "s. !")
            return RunTime

######################################## DECISION STUFF ########################################
PrevPredictionCorrect = 0
CurrentPredictionCorrect = 0

def AnalyseDecision(Decision):
    global AnalysisReturnMin
    global AnalysisReturnMax

    Prediction = Shotgun.PredictedChamber[0] # Store value for comparison.

    if DealerAnalysisDebug == 1: # Print if DealerAnalysisDebug is enabled.
        print("\n######DEBUGGING###### --Current Shotgun Chamber = ", Shotgun.Shotgun)
        print("######DEBUGGING###### Predicted Shotgun Chamber = ", Shotgun.PredictedChamber)
    
    global PrevPredictionCorrect
    global CurrentPredictionCorrect
    if CurrentPredictionCorrect == 1:
        PrevPredictionCorrect = 1
    else:
        PrevPredictionCorrect = 0
    
    if DealerAnalysisDebug == 1:
        print("\n######DEBUGGING###### PrevPredictionCorrect =", PrevPredictionCorrect)
        print("######DEBUGGING###### CurrentPredictionCorrect =", CurrentPredictionCorrect)
    
    CurrentPredictionCorrect = 0

    if Shotgun.PredictedChamber[0] == Shotgun.Shotgun[0]: # Check if Shotgun Chamber Prediction is correct.
        if DealerAnalysisDebug == 1:
            if Shotgun.BlankShells != 0 and Shotgun.LiveShells != 0: # Print if there is at least 1 of each type of shell left.
                CurrentPredictionCorrect = 1
                print("\n######DEBUGGING###### ! CURRENT GENERATION CORRECT !")
                
                if DealerAnalysisDebug == 1:
                    if PrevPredictionCorrect == 1:
                        print("\n######DEBUGGING###### ! PREVIOUS GENERATION: CORRECT. !")
    
    else: # If Shotgun Chamber Prediction is incorrect.
        if DealerAnalysisDebug == 1:
            if Shotgun.BlankShells != 0 and Shotgun.LiveShells != 0: # Print if there is at least 1 of each type of shell left.
                CurrentPredictionCorrect = 0
                print("\n######DEBUGGING###### ! CURRENT GENERATION INCORRECT !")
                
                if DealerAnalysisDebug == 1:
                    if PrevPredictionCorrect == 0:
                        print("\n######DEBUGGING###### ! PREVIOUS GENERATION: INCORRECT. !")

        Shotgun.PredictShotgun(Shotgun.ShellCount, True) # If Shotgun Chamber Prediction is incorrect, regenerate prediction.

    if Shotgun.BlankShells != 0 and Shotgun.LiveShells == 0: # Print if there only Blank Shells left.
        if DealerAnalysisDebug == 1:
            print("\n######DEBUGGING###### ! (Prediction N/A, Only Blank Shells Remain.) !")
    elif Shotgun.BlankShells == 0 and Shotgun.LiveShells != 0: # Print if there only Live Shells left.
        if DealerAnalysisDebug == 1:
            print("\n######DEBUGGING###### ! (Prediction N/A, Only Live Shells Remain.) !")
  
    ########################################

    if Shotgun.BlankShells == 0: # If the remaining shells are live, shoot player.
        return "ShootPlayer" # Return decision.  
    elif Shotgun.LiveShells == 0: # If the remaining shells are blank, shoot self.
        return "ShootSelf" # Return decision.
    else:
        if Prediction == "B":
            if Decision == "Blank":
                print("\n(The Dealer thinks it's Blank.) \n(After analysing, The Dealer is sure of its initial decision.)")
                return "ShootSelf" # Return decision.
            
            if Decision == "Live":
                if PrevPredictionCorrect == 1:
                    print("\n(The Dealer thinks it's Live.) \n(After analysing, The Dealer changes its mind.)")
                    return "ShootSelf"
                else:
                    print("\n(The Dealer thinks it's Live.) \n(After analysing, The Dealer is sure of its initial decision.)")
                    return "ShootPlayer" # Return decision.
        
        if Prediction == "L":
            if Decision == "Blank":
                if PrevPredictionCorrect == 1:
                    print("\n(The Dealer thinks it's Blank.) \n(After analysing, The Dealer changes its mind.)")
                    return "ShootPlayer" # Return decision.
                else:
                    print("\n(The Dealer thinks it's Blank.) \n(After analysing, The Dealer is sure of its initial decision.)")
                    return "ShootSelf"
            
            if Decision == "Live":
                print("\n(The Dealer thinks it's Live.) \n(After analysing, The Dealer is sure of its initial decision.)")
                return "ShootPlayer" # Return decision.

def Turn(AILevel):
    global ChancePerShell
    global BlankChance
    global LiveChance

    WaitTime("Start")

    ChancePerShell = int(100 / (Shotgun.LiveShells + Shotgun.BlankShells)) # Calculate chance for a shell to be shot.
    BlankChance = (ChancePerShell * Shotgun.BlankShells) # Calculate chance for a blank shell to be shot.
    LiveChance = (ChancePerShell * Shotgun.LiveShells) # Calculate chance for a live shell to be shot.

    if DealerDecisionDebug == 1:
        Debug() # Print debug.

    #Outcome = 0

    if AILevel == 1:
        if BlankChance > LiveChance: # If shell more likely to be a blank, shoot player.
            return "ShootSelf" # Return decision.
        
        if LiveChance > BlankChance: # If shell more likely to be a live, shoot player.
            return "ShootPlayer" # Return decision.
        
        if LiveChance == BlankChance: # If shell equally likely to be a live or a blank, choose randomly.
            RandomChoice = random.randint(0,1)
            if DealerDecisionDebug == 1: # Print if DealerDecisionDebug is enabled.
               if RandomChoice == 0:
                   print("\n######DEBUGGING###### (Random Choice: Blank.)")
               if RandomChoice == 1:
                   print("\n######DEBUGGING###### (Random Choice: Live.)")

            if RandomChoice == 0:
                return "ShootSelf"
            if RandomChoice == 1:
                return "ShootPlayer"
    
    if AILevel == 2:
        if BlankChance > LiveChance: # If shell more likely to be a blank, analyse chance of shell being a blank.
            if DealerDecisionDebug == 1:
                print("\n######DEBUGGING###### (Initial Choice: Blank.)")
            
            return AnalyseDecision("Blank") # See function.

        if LiveChance > BlankChance: # If shell more likely to be a live, analyse chance of shell being a live.
            if DealerDecisionDebug == 1:
                print("\n######DEBUGGING###### (Initial Choice: Live.)")
            
            return AnalyseDecision("Live") # See function.
        
        if LiveChance == BlankChance: # If shell equally likely to be a live or a blank, analyse chances.
            if DealerDecisionDebug == 1:
                print("\n######DEBUGGING###### (Initial Choice: Equal Chance.)")
            
            RandomChoice = random.randint(0,1)
            if RandomChoice == 0: # "A Blank" randomly chosen.
                if DealerDecisionDebug == 1:
                    print("\n######DEBUGGING###### (Random Guess: Blank.)")
                
                return AnalyseDecision("Blank") # See function.
            
            if RandomChoice == 1: # "A Live" randomly chosen.
                if DealerDecisionDebug == 1:
                    print("\n######DEBUGGING###### (Random Guess: Live.)")
                
                return AnalyseDecision("Live") # See function.    
    
    if AILevel == 3:
        if Shotgun.Shotgun[0] == "B":
            return "ShootSelf"
        if Shotgun.Shotgun[0] == "L":
            return "ShootPlayer"