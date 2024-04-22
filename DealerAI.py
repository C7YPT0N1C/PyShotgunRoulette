import random
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

PlayerDecisions = [] # List of the moves The Player has made.
DealerDecisions = [] # List of the moves The Dealer has made.
CorrectDecision = [] # List of the correct type of shell (generated as each shell is shot.)

AnalysisReturnMin = 50 # Minimum result of analysis for a positive to be returned. (Default = 50).

ChancePerShell = 0 # Chance for a shell to be shot.
LiveChance = 0 # Chance for a live shell to be shot.
BlankChance = 0 # Chance for a blank shell to be shot.

######################################## DEBUG STUFF ########################################

def Debug(): # Print variables.
    global ChancePerShell
    global LiveChance
    global BlankChance

    print("\nLive Shells:", Shotgun.LiveShells)
    print("Blank Shells:", Shotgun.BlankShells)

    print("\nChance Per Shell = ", ChancePerShell)
    print("LiveChance:", LiveChance)
    print("BlankChance:", BlankChance)

def AnalysisPrint(): # Prints the lists.
    print("\nPlayer Decisions: ", PlayerDecisions)
    print("Dealer Decisions: ", DealerDecisions)
    print("Correct Decisions: ", CorrectDecision)

######################################## DECISION TRACKER STUFF ########################################

def Track(Target, Decision): # Updates lists as decisions are made and shells are shot.
    if Target == "Player":
        if Decision == "Live":
            PlayerDecisions.append("L")
            DealerDecisions.append("-")
        if Decision == "Blank":
            PlayerDecisions.append("B")
            DealerDecisions.append("-")
    
    if Target == "Dealer":
        if Decision == "Live":
            DealerDecisions.append("L")
            PlayerDecisions.append("-")
        if Decision == "Blank":
            DealerDecisions.append("B")
            PlayerDecisions.append("-")

    if Target == "System":
        if Decision == "Live":
            CorrectDecision.append("L")
        if Decision == "Blank":
            CorrectDecision.append("B")

######################################## ANALYSIS STUFF ########################################

def ConfirmAnalysis(Type, Analysis): # Makes a decision depending on results of analysis.
    if Type == "Live":
        #AnalysisPrint() # Print Analysis Stuff

        #if Analysis >= AnalysisReturnMin and (Analysis <= LiveChance or Analysis >= BlankChance):
        if Analysis >= AnalysisReturnMin or Analysis >= BlankChance:
        # Continue with decision if results of analysis are within the positive range, or higher than a chance of shooting a blank.
            
            print("Analysis = ", Analysis)
            if (Analysis >= LiveChance):
                print("\nAnalysis >= AnalysisReturnMin")
            if (Analysis >= BlankChance):
                print("\nAnalysis >= BlankChance")
            
            #print("\n(After analysing the previous turns, The Dealer thinks it is", Analysis, "% Live).")
            print("\n(The Dealer is sure of its decision.)")
            return "ShootPlayer" # Return decision.
        else:
            #print("\n(After analysing the previous turns, The Dealer thinks it is", Analysis, "% Live.)")
            print("\n(The Dealer is unsure of its decision and changes its mind.)")
            
            Track("Dealer", "Self") # Update list of previous moves made.
            return "ShootSelf" # Return decision.
    
    if Type == "Blank":
        #AnalysisPrint() # Print Analysis Stuff

        #if Analysis >= AnalysisReturnMin and (Analysis <= BlankChance and Analysis >= LiveChance):
        if Analysis >= AnalysisReturnMin or Analysis >= LiveChance:
        # Continue with decision if results of analysis are within the positive range, or higher than a chance of shooting a live.
            
            print("Analysis = ", Analysis)
            if (Analysis >= LiveChance):
                print("\nAnalysis >= AnalysisReturnMin")
            if (Analysis >= LiveChance):
                print("\nAnalysis >= LiveChance")
            
            #print("\n(After analysing the previous turns, The Dealer thinks it is", Analysis, "% Blank.)")
            print("\n(The Dealer is sure of its decision.)")
            return "ShootSelf" # Return decision.
        else:
            #print("\n(After analysing the previous turns, The Dealer thinks it is", Analysis, "% Blank.")
            print("\n(The Dealer is unsure of its decision and changes its mind.)")
            
            Track("Dealer", "Enemy") # Update list of previous moves made.
            return "ShootPlayer" # Return decision.
        
################################################################################

def Analyse(Decision): # Analyses the lists for The Dealer to make a decision.
    if Decision == "Live": # If The Dealer's initial calculation of odds suggests that the current shell is a live.
        if CorrectDecision.count("L") != 0 and DealerDecisions.count("L") != 0 and  PlayerDecisions.count("L") != 0: # Makes sure lists arent empty to avoid divide by zero error.
            DealerCorrectCount = 0
            for i in range (0, len(CorrectDecision)):
                if DealerDecisions[i] == "L" and CorrectDecision[i] == "L":
                    DealerCorrectCount = DealerCorrectCount + 1
            
            PlayerCorrectCount = 0
            for i in range (0, len(CorrectDecision)):
                if PlayerDecisions[i] == "L" and CorrectDecision[i] == "L":
                    PlayerCorrectCount = PlayerCorrectCount + 1
            
            if DealerCorrectCount == 0: # Anti Zero Error. Minimal effect on calculations.
                DealerCorrectCount = 1
            if PlayerCorrectCount == 0:
                PlayerCorrectCount = 1
            
            #print("\nCorrect Live Count = ", CorrectDecision.count("L"))
            #print("Dealer Correct Count = ", DealerCorrectCount)
            #print("Player Correct Count = ", PlayerCorrectCount)

            ShellCount = CorrectDecision.count("L") # Set "ShellCount" variable.
            Analysis = int(100 / (ShellCount / (DealerCorrectCount + PlayerCorrectCount)))
            return ConfirmAnalysis("Live", Analysis)
        else:
            #print("\n(Dealer does not enough data to analyse past turns.)")
            return "ShootPlayer"
    
    if Decision == "Blank": # If The Dealer's initial calculation of odds suggests that the current shell is a blank.
        if CorrectDecision.count("B") != 0 and DealerDecisions.count("B") != 0 and  PlayerDecisions.count("B") != 0:
            DealerCorrectCount = 0
            for i in range (0, len(CorrectDecision)):
                if DealerDecisions[i] == "B" and CorrectDecision[i] == "B":
                    DealerCorrectCount = DealerCorrectCount + 1

            PlayerCorrectCount = 0
            for i in range (0, len(CorrectDecision)):
                if PlayerDecisions[i] == "B" and CorrectDecision[i] == "B":
                    PlayerCorrectCount = PlayerCorrectCount + 1
            
            if DealerCorrectCount == 0: # Anti Zero Error. Minimal effect on calculations.
                DealerCorrectCount = 1
            if PlayerCorrectCount == 0:
                PlayerCorrectCount = 1
            
            #print("\nCorrect Live Count = ", CorrectDecision.count("L"))
            #print("Dealer Correct Count = ", DealerCorrectCount)
            #print("Player Correct Count = ", PlayerCorrectCount)
            
            ShellCount = CorrectDecision.count("B") # Set "ShellCount" variable.
            Analysis = int(100 / (ShellCount / (DealerCorrectCount + PlayerCorrectCount)))
            return ConfirmAnalysis("Blank", Analysis)
        else:
            #print("\n(Dealer does not enough data to analyse past turns.)")
            return "ShootSelf"

######################################## DECISION STUFF ########################################

def ReturnDecision(Decision):
    global AnalysisReturnMin
    global AnalysisReturnMax
    
    if Decision == "Live":
        Track("Dealer", "Live") # Updates list of previous moves made.
        Analysis = Analyse("Live") # Analysing chances of shell being a live.
        #print("Analysis = ", Analysis) # Print the results of the analysis.
        return Analysis # Return decision.
    
    if Decision == "Blank":
        Track("Dealer", "Blank") # Updates list of previous moves made.
        Analysis = Analyse("Blank") # Analysing chances of shell being a blank.
        #print("Analysis = ", Analysis) # Print the results of the analysis.
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
    LiveChance = (ChancePerShell * Shotgun.LiveShells) # Calculate chance for a live shell to be shot.
    BlankChance = (ChancePerShell * Shotgun.BlankShells) # Calculate chance for a blank shell to be shot.

    #Debug() # Print debug.

    #Outcome = 0

    if AILevel == 1:
        if LiveChance > BlankChance: # If shell more likely to be a live, shoot player.
            return "ShootPlayer" # Return decision.
        
        if BlankChance > LiveChance: # If shell more likely to be a blank, shoot player.
            return "ShootSelf" # Return decision.
        
        if LiveChance == BlankChance: # If shell equally likely to be a live or a blank, choose randomly.
            RandomChoice = random.randint(0,1)
            if RandomChoice == 0:
                return "ShootPlayer"
            if RandomChoice == 1:
                return "ShootSelf"
    
    if AILevel == 2:
        if LiveChance > BlankChance: # If shell more likely to be a live, analyse chance of shell being a live.
            #print("\n(The Dealer's initial thought: a Live.)")
            return ReturnDecision("Live") # See function.
        
        if BlankChance > LiveChance: # If shell more likely to be a blank, analyse chance of shell being a blank.
            #print("\n(The Dealer's initial thought: a Blank.)")
            return ReturnDecision("Blank") # See function.
        
        if LiveChance == BlankChance: # If shell equally likely to be a live or a blank, analyse chances.
            #print("\n(After calculating the odds, The Dealer thinks it is an equal chance.)")
            RandomChoice = random.randint(0,1)
            #print("Random Choice = ", RandomChoice)

            if RandomChoice == 0: # "A Live" randomly chosen.
                #print("\n(The Dealer's random guess: a Live.)")
                return ReturnDecision("Live") # See function.
            
            if RandomChoice == 1: # "A Blank" randomly chosen.
                #print("\n(The Dealer's random guess: a Blank.)")
                return ReturnDecision("Blank") # See function.

######################################## TESTING STUFF ########################################

def Test():
    global PlayerDecisions
    global DealerDecisions
    global CorrectDecision

    PlayerDecisions = ['E', 'E', 'S', '-', 'E', '-', 'E']
    DealerDecisions = ['-', '-', '-', 'E', '-', 'S', '-']
    CorrectDecision = ['B', 'B', 'L', 'B', 'L', 'L', 'L']
    
    #Analyse("Live")
    #Analyse("Blank")

#Test()