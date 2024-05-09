import VariableManager as VM

PlayerDecisions = [] # List of the moves The Player has made.
DealerDecisions = [] # List of the moves The Dealer has made.
CorrectDecision = [] # List of the correct type of shell (generated as each shell is shot.)

def Analyse(Decision): # Analyses the lists for The Dealer to make a decision. Returns the percentage of confidence.
    if Decision == "Live": # If The Dealer originally thinks the current shell is a Live.
        if CorrectDecision.count("L") != 0 and DealerDecisions.count("L") != 0: # Makes sure lists arent empty to avoid divide by zero error.
            
            DealerCorrectCount = 0
            for i in range (0, len(CorrectDecision)):
                if DealerDecisions[i] == "L" and CorrectDecision[i] == "B":
                    DealerCorrectCount = DealerCorrectCount + 1
            
            DealerIncorrectCount = 0
            for i in range (0, len(CorrectDecision)):
                if DealerDecisions[i] == "L" and CorrectDecision[i] == "L":
                    DealerIncorrectCount = DealerIncorrectCount + 1
            
            if DealerCorrectCount == 0: # Anti Zero Error. Minimal effect on calculations.
                DealerCorrectCount = 1
            if DealerIncorrectCount == 0:
                DealerIncorrectCount = 1
            
            if VM.Debugging == 2: # Runs if debugging is enabled.
                print("\nCorrect Live Count = ", CorrectDecision.count("L"))
                print("Dealer Correct Count = ", DealerCorrectCount)
                print("Dealer Incorrect Count = ", DealerIncorrectCount)
            
            ShellCount = CorrectDecision.count("L") # Set "ShellCount" variable.
            Analysis = ((((DealerCount + PlayerCount) / 2) / ShellCount) * 100)
        else:
            #print("\n(Not enough live shells have been shot to analyse.)")
            Analysis = 100
    
    return Analysis

######################################## TESTING STUFF ########################################

def Test():
    global PlayerDecisions
    global DealerDecisions
    global CorrectDecision

    DealerDecisions = ['L', 'L', 'B', 'B', 'L', 'B', 'L']
    CorrectDecision = ['B', 'B', 'L', 'B', 'L', 'L', 'B']
    # L
    
    Analyse()
 
#Test()