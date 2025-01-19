import LogicManager as LM
import Shotgun as Shotgun
import Timer as Timer

import time as time
import random as random

######################################## NOTES ########################################

######## AI Levels ########
# Level 1: AI decides purely on odds. Does not predict future turns.
# Level 2: AI predicts future turns. It will change its decision if it was wrong last time.
# Level 3: AI knows the future. It knows what the next shell will be. It will always win.

######## HOW THE AI WORKS ########
# TODO
# The AI will decide whether to shoot the player or itself based on the odds of the next shell being a live or a blank.
# The AI will also predict the next shell based on the current chamber and the remaining shells.
# The AI will change its decision if it was wrong last time.

######################################## DECLARE VARIABLES ########################################

ChancePerShell = 0 # Chance for a shell to be shot. Kinda arbitrary.
BlankChance = 0 # Chance for a Blank shell to be shot.
LiveChance = 0 # Chance for a Live shell to be shot.

######################################## MISC ########################################

def Debug(): # Print variables.
    global ChancePerShell
    global LiveChance
    global BlankChance

    #print("\nBlank Shells:", Shotgun.BlankShells, "\nBlankChance:", BlankChance, "%")
    #print("\nLive Shells:", Shotgun.LiveShells, "\nLiveChance:", LiveChance, "%")
    #print("\nChance Per Shell = ", ChancePerShell)

    if LM.DealerAnalysisDebug == 1:
        Timer.WaitTime("Pause") # See function.

    print("\n###DEBUGGING### Blank Shells:", Shotgun.BlankShells, "| Live Shells:", Shotgun.LiveShells)
    print("###DEBUGGING### BlankChance:", BlankChance, "% | LiveChance:", LiveChance, "%")
    print("###DEBUGGING### Chance Per Shell = ", ChancePerShell)

######################################## ANALYSIS STUFF ########################################

PredictionNum = 0
PredictionsCorrectNum = 0
CurrentPredictionCorrect = False

PredictionTemperture = 0
ConfirmPrediction = False

def ResetPredictions():
    global PredictionNum
    global PredictionsCorrectNum
    global CurrentPredictionCorrect
    global PredictionTemperture
    global ConfirmPrediction

    PredictionNum = 0
    PredictionsCorrectNum = 0
    CurrentPredictionCorrect = False

    PredictionTemperture = 0
    ConfirmPrediction = False

def AnalyseDecision(Decision):
    global PredictionNum
    global PredictionsCorrectNum
    global CurrentPredictionCorrect
    global PredictionTemperture
    global ConfirmPrediction ###

    Timer.WaitTime("Wait") # See function.

    Shotgun.PredictShotgun() # Update Dealer AI's Shotgun Prediction Algorithm.
    
    if Shotgun.PredictedChamber[0] == "B": # Store value of Prediction for comparison.
        Prediction = "Blank"
    if Shotgun.PredictedChamber[0] == "L": # Store value of Prediction for comparison.
        Prediction = "Live"

    if LM.DealerAnalysisDebug == 1: # Print if DealerAnalysisDebug is enabled.
        Timer.WaitTime("Pause") # See function.

        print("\n###DEBUGGING### UPDATING SHOTGUN PREDICTION ALGORITHM...")
        print("###DEBUGGING### --Current Shotgun Chamber = ", Shotgun.Shotgun)
        print("###DEBUGGING### Predicted Shotgun Chamber = ", Shotgun.PredictedChamber)

    PredictionNum = PredictionNum + 1 # Increment PredictionNum.

    CurrentPredictionCorrect = False
    if LM.DealerAnalysisDebug == 1:
        if Shotgun.BlankShells != 0 and Shotgun.LiveShells != 0: # Print if there is at least 1 of each type of shell left.
            if Shotgun.PredictedChamber[0] == Shotgun.Shotgun[0]: # If Shotgun Chamber Prediction is correct.
                CurrentPredictionCorrect = True
            else: # If Shotgun Chamber Prediction is incorrect.
                CurrentPredictionCorrect = False
                Shotgun.PredictShotgun() # If Shotgun Chamber Prediction is incorrect, regenerate prediction.

            if Shotgun.BlankShells != 0 and Shotgun.LiveShells == 0: # Print if there only Blank Shells left.
                print("\n###DEBUGGING### ! (Prediction N/A, Only Blank Shells Remain.) !")
            if Shotgun.BlankShells == 0 and Shotgun.LiveShells != 0: # Print if there only Live Shells left.
                print("\n###DEBUGGING### ! (Prediction N/A, Only Live Shells Remain.) !")
    
    if CurrentPredictionCorrect == True: # If the current prediction is correct.
        PredictionsCorrectNum = PredictionsCorrectNum + 1
    else: # If the current prediction is incorrect.
        PredictionsCorrectNum = PredictionsCorrectNum
    
    #PredictionsCorrectNum = PredictionsCorrectNum + 1 if CurrentPredictionCorrect == True else 0 # Increment PredictionsCorrectNum if CurrentPredictionCorrect is True.
    PredictionTemperture = PredictionsCorrectNum / PredictionNum
    if PredictionTemperture >= 0.5:
        ConfirmPrediction = True
    else:
        ConfirmPrediction = False

    if LM.DealerAnalysisDebug == 1:
        print("\n###DEBUGGING### ! Current Shell = ", Shotgun.CheckCurrentShell(), "| Decision = ", Decision, "| Prediction = ", Prediction, "!")
        print("###DEBUGGING### ! Current Prediction Correct? =", CurrentPredictionCorrect, "| Prediction Number =", PredictionNum, "| Correct Predictions Number =", PredictionsCorrectNum, "| Prediction Temperture =", PredictionTemperture, "| Confirm Prediction? =", ConfirmPrediction, "!")

        #print("###DEBUGGING### ! Current Prediction Correct? =", CurrentPredictionCorrect, "| Prediction Number =", PredictionNum, "| Correct Predictions Number =", PredictionsCorrectNum, "| Prediction Temperture =", PredictionTemperture, "| Confirm Prediction? =", ConfirmPrediction, "!")

    ########################################

    if Shotgun.BlankShells == 0: # If the remaining shells are live, shoot player.
        return "ShootPlayer" # Return decision.  
    
    elif Shotgun.LiveShells == 0: # If the remaining shells are blank, shoot self.
        return "ShootSelf" # Return decision.
    
    else:
        Timer.WaitTime("ReportToPlayer") # See function.
        if Decision == "Blank": # If the Decision is a Blank shell.
            print("\n(The Dealer thinks it's Blank.)")

            if Prediction == "Blank": # If the Decision and Prediction agree on it being a Blank shell.
                print("(After analysing, The Dealer is sure of its initial decision.)")
                return "ShootSelf" # Return decision.
            
            if Prediction == "Live": # If the Decision and Prediction disagree on it being a Blank shell.
                if ConfirmPrediction == True: # If the previous Prediction was correct.
                    print("(After analysing, The Dealer changes its mind.)")
                    return "ShootPlayer" # Return decision.
                else:
                    print("(After analysing, The Dealer is sure of its initial decision.)")
                    return "ShootSelf" # Return decision.
        
        if Decision == "Live":
            print("\n(The Dealer thinks it's Live.)")

            if Prediction == "Live": # If the Decision and Prediction agree on it being a Blank shell.
                print("(After analysing, The Dealer is sure of its initial decision.)")
                return "ShootPlayer" # Return decision.

            if Prediction == "Blank": # If the Decision and Prediction diagree on it being a Blank shell.
                if ConfirmPrediction == True: # If the previous Prediction was correct.
                    print("(After analysing, The Dealer changes its mind.)")
                    return "ShootSelf" # Return decision.
                else:    
                    print("(After analysing, The Dealer is sure of its initial decision.)")
                    return "ShootPlayer" # Return decision.

######################################## DECISION STUFF ########################################

def Turn(AILevel):
    global ChancePerShell
    global BlankChance
    global LiveChance

    print("\n(The Dealer is thinking...)")

    Timer.WaitTime("Wait") # See function.
    ChancePerShell = int(100 / (Shotgun.LiveShells + Shotgun.BlankShells)) # Calculate chance for a shell to be shot.
    BlankChance = (ChancePerShell * Shotgun.BlankShells) # Calculate chance for a blank shell to be shot.
    LiveChance = (ChancePerShell * Shotgun.LiveShells) # Calculate chance for a live shell to be shot.

    if LM.DealerDecisionDebug == 1:
        Debug() # Print debug.

    if AILevel == 1: # "Easy" Difficulty.
        if BlankChance > LiveChance: # If shell more likely to be a blank, shoot player.
            return "ShootSelf" # Return decision.
        
        if LiveChance > BlankChance: # If shell more likely to be a live, shoot player.
            return "ShootPlayer" # Return decision.
        
        if LiveChance == BlankChance: # If shell equally likely to be a live or a blank, choose randomly.
            RandomChoice = random.randint(0,1)
            if LM.DealerDecisionDebug == 1: # Print if DealerDecisionDebug is enabled.
               if RandomChoice == 0:
                   print("\n###DEBUGGING### (Random Choice: Blank.)")
               if RandomChoice == 1:
                   print("\n###DEBUGGING### (Random Choice: Live.)")

            if RandomChoice == 0:
                return "ShootSelf"
            if RandomChoice == 1:
                return "ShootPlayer"
    
    if AILevel == 2: # "Normal" Difficulty.

        if BlankChance > LiveChance: # If shell more likely to be a blank, analyse chance of shell being a blank.
            if LM.DealerDecisionDebug == 1:
                print("\n###DEBUGGING### (Initial Choice: Blank.)")
            
            return AnalyseDecision("Blank") # See function.

        if LiveChance > BlankChance: # If shell more likely to be a live, analyse chance of shell being a live.
            if LM.DealerDecisionDebug == 1:
                print("\n###DEBUGGING### (Initial Choice: Live.)")
            
            return AnalyseDecision("Live") # See function.
        
        if LiveChance == BlankChance: # If shell equally likely to be a live or a blank, analyse chances.
            if LM.DealerDecisionDebug == 1:
                print("\n###DEBUGGING### (Initial Choice: Equal Chance.)")
            
            RandomChoice = random.randint(0,1)
            if RandomChoice == 0: # "A Blank" randomly chosen.
                if LM.DealerDecisionDebug == 1:
                    print("\n###DEBUGGING### (Random Guess: Blank.)")
                
                return AnalyseDecision("Blank") # See function.
            
            if RandomChoice == 1: # "A Live" randomly chosen.
                if LM.DealerDecisionDebug == 1:
                    print("\n###DEBUGGING### (Random Guess: Live.)")
                
                return AnalyseDecision("Live") # See function.    
    
    if AILevel == 3: # "CHEATER" Difficulty.
        if Shotgun.Shotgun[0] == "B":
            #AnalyseDecision("Blank") # Not needed. The AI knows the the current shell. This is here for fun. See function.
            return "ShootSelf"
        if Shotgun.Shotgun[0] == "L":
            #AnalyseDecision("Live") # Not needed. The AI knows the the current shell. This is here for fun. See function.
            return "ShootPlayer"