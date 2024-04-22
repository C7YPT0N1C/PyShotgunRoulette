import random
import Shotgun

######################################## DECLARE VARIABLES ########################################

PlayerDecisions = [] # List of the moves The Player has made.
DealerDecisions = [] # List of the moves The Dealer has made.
CorrectDecision = [] # List of the correct type of shell (generated as each shell is shot.)

AnalysisReturnMin = 25 # Minimum result of analysis for a positive to be returned. (Default = 25).
AnalysisReturnMax = 100 # Maxiumum result of analysis for a positive to be returned. (Default = 100).

ChancePerShell = 0 # Chance for a shell to be shot.
LiveChance = 0 # Chance for a live shell to be shot.
BlankChance = 0 # Chance for a blank shell to be shot.

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

def AnalysisPrint(): # Prints the lists.
    print("\nPlayer Decisions: ", PlayerDecisions)
    print("Dealer Decisions: ", DealerDecisions)
    print("Correct Decisions: ", CorrectDecision)

    print("\nMin Analysis Return Value: ", AnalysisReturnMin)
    print("Max Analysis Return Value: ", AnalysisReturnMax)


def ConfirmAnalysis(Type, Analysis): # Makes a decision depending on results of analysis.
    if Type == "Live":
        AnalysisPrint() # Print Analysis Stuff

        if Analysis <= AnalysisReturnMax and Analysis >= AnalysisReturnMin: # Print output depending on results.
            print("\n(After analysing the previous turns, The Dealer thinks it is", Analysis, "% Live. The Dealer is sure of this.)")
            return "ShootPlayer" # Return decision.
        else:
            print("\n(After analysing the previous turns, The Dealer thinks it is", Analysis, "% Live. The Dealer is unsure of this analysis and changes its mind.)")
            
            Track("Dealer", "Self")
            return "ShootSelf" # Return decision.
    
    if Type == "Blank":
        AnalysisPrint() # Print Analysis Stuff

        if Analysis <= AnalysisReturnMax and Analysis >= AnalysisReturnMin:
            print("\n(After analysing the previous turns, The Dealer thinks it is", Analysis, "% Blank. The Dealer is sure of this.)")
            return "ShootSelf" # Return decision.
        else:
            print("\n(After analysing the previous turns, The Dealer thinks it is", Analysis, "% Blank. The Dealer is unsure of this analysis and changes its mind.)")
            
            Track("Dealer", "Enemy")
            return "ShootPlayer" # Return decision.
        
################################################################################

def Analyse(Decision): # Analyses the lists for The Dealer to make a decision.
    if Decision == "Live": # If The Dealer's initial calculation of odds suggests that the current shell is a live.
        if CorrectDecision.count("L") != 0 and DealerDecisions.count("L") != 0 and  PlayerDecisions.count("L") != 0: # Makes sure lists arent empty to avoid divide by zero error.
            ShellCount = CorrectDecision.count("L") # Set "ShellCount" variable.
            Analysis = (int(100 / (ShellCount / ((DealerDecisions.count("L") + PlayerDecisions.count("L")) / 2))) / 4)
            # Under the assumption that the current shell is a live, the lists are searched for shots taken against an enemy, and calculates the average between the player and the dealer.
            #The amount of live shells actually shot is divided by the average shots taken against an enemy. 100 is then divided by this number to give a percentage.
            
            return ConfirmAnalysis("Live", Analysis)
        
        else:
            #print("\n(Not enough data to analyse past turns.)")
            return "ShootPlayer"
    
    if Decision == "Blank": # If The Dealer's initial calculation of odds suggests that the current shell is a blank.
        if CorrectDecision.count("B") != 0 and DealerDecisions.count("B") != 0 and  PlayerDecisions.count("B") != 0:
            ShellCount = CorrectDecision.count("B")
            Analysis = ((int(100 / (ShellCount / ((DealerDecisions.count("B") + PlayerDecisions.count("B")) / 2)))) / 4)
            # Under the assumption that the current shell is a blank, the lists are searched for shots taken against themselves, and calculates the average between the player and the dealer.
            #The amount of blank shells actually shot is divided by the average shots taken against themselves. 100 is then divided by this number to give a percentage.
            
            return ConfirmAnalysis("Live", Analysis)
        
        else:
            #print("\n(Not enough data to analyse past turns.)")
            return "ShootSelf"

######################################## DEALER TURN STUFF ########################################

######## Levels ########
#### L1 ####
# AI decides purely on odds. Does not predict future turns.

#### L2 ####
# AI calculates current odds, and uses player's previous decisions to make guesses on its own next move.

#### L3 ####
# AI calculates based on odds, and uses player's and its own previous decisions to make guesses on its own next move.

def Debug(): # Print variables.
    global ChancePerShell
    global LiveChance
    global BlankChance

    print("\n Live Shells:", Shotgun.LiveShells)
    print("Blank Shells:", Shotgun.BlankShells)

    print("\nChance Per Shell = ", ChancePerShell)
    print("LiveChance:", LiveChance)
    print("BlankChance:", BlankChance)

########################################

def ReturnDecision(Decision, LiveAnalysisChance, BlankAnalysisChance):
    global AnalysisReturnMin
    global AnalysisReturnMax
    
    if Decision == "Live":
        AnalysisReturnMin = (BlankAnalysisChance * 0.5) # Set lower threshold for analysis result. Absolute lower threshold = 25.
        AnalysisReturnMax = (LiveAnalysisChance * 2) # Set upper threshold for analysis result.  Absolute upper threshold = 100.

        Track("Dealer", "Live") # Updates list of previous moves made.

        Analysis = Analyse("Live") # Analysing chances of shell being a live.
        #print("Analysis = ", Analysis) # Print the results of the analysis.

        return Analysis # Return decision.
    
    if Decision == "Blank":
        AnalysisReturnMin = (LiveAnalysisChance * 1.5) # Set lower threshold for analysis result.
        AnalysisReturnMax = (BlankAnalysisChance * 3) # Set upper threshold for analysis result.
        
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

    Debug()

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
            return ReturnDecision("Live", LiveChance, BlankChance) # See function.
        
        if BlankChance > LiveChance: # If shell more likely to be a blank, analyse chance of shell being a blank.
            #print("\n(The Dealer's initial thought: a Blank.)")
            return ReturnDecision("Blank", LiveChance, BlankChance) # See function.
        
        if LiveChance == BlankChance: # If shell equally likely to be a live or a blank, analyse chances.
            #print("\n(After calculating the odds, The Dealer thinks it is an equal chance.)")
            RandomChoice = random.randint(0,1)
            #print("Random Choice = ", RandomChoice)

            if RandomChoice == 0: # "A Live" randomly chosen.
                return ReturnDecision("Live", LiveChance, BlankChance) # See function.
            
            if RandomChoice == 1: # "A Blank" randomly chosen.
                return ReturnDecision("Blank", LiveChance, BlankChance) # See function.

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