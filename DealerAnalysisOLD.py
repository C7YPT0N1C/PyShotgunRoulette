import VariableManager as VM

PlayerDecisions = [] # List of the moves The Player has made.
DealerDecisions = [] # List of the moves The Dealer has made.
CorrectDecision = [] # List of the correct type of shell (generated as each shell is shot.)

def Analyse(Decision): # Analyses the lists for The Dealer to make a decision. Returns the percentage of confidence.
    if Decision == "Live": # If The Dealer thinks the current shell is a Live.
        if CorrectDecision.count("L") != 0 and DealerDecisions.count("L") != 0: # Makes sure lists arent empty to avoid divide by zero error.
            
            DealerCorrectCount = 0
            for i in range (0, len(CorrectDecision)):
                if CorrectDecision[i] == "L" and DealerDecisions[i] == "L":
                    DealerCorrectCount = DealerCorrectCount + 1
            
            DealerIncorrectCount = 0
            for i in range (0, len(CorrectDecision)):
                if CorrectDecision[i] == "L" and DealerDecisions[i] == "B":
                    DealerIncorrectCount = DealerIncorrectCount + 1
            
            if DealerCorrectCount == 0: # Anti Zero Error. Minimal effect on calculations.
                DealerCorrectCount = 1
            if DealerIncorrectCount == 0:
                DealerIncorrectCount = 1
            
            #if VM.Debugging == 2: # Runs if debugging is enabled.
            print("\nCorrect Live Count = ", CorrectDecision.count("L"))
            print("Dealer Correct Count = ", DealerCorrectCount)
            print("Dealer Incorrect Count = ", DealerIncorrectCount)
            
            ShellCount = CorrectDecision.count("L") # Set "ShellCount" variable.

            DealerCorrectAnalysis = ((DealerCorrectCount / ShellCount) * 100)
            DealerIncorrectAnalysis = ((DealerIncorrectCount / ShellCount) * 100)

            print("\nDealer Correct Analysis = ", DealerCorrectAnalysis)
            print("Dealer Incorrect Analysis = ", DealerIncorrectAnalysis)

            Analysis = DealerCorrectAnalysis - DealerIncorrectAnalysis
            
            if VM.Debugging == 2: # Runs if debugging is enabled.
                print("Analysis = ", Analysis) # Print the results of the analysis.

            if Analysis >= 0:
                Decision = "ShootPlayer"
            else:
                Decision = "ShootSelf"
        else:
            print("\n(Not enough live shells have been shot to analyse.)")
            Decision = "ShootPlayer"
        
    if Decision == "Blank": # If The Dealer thinks the current shell is a Blank.
        if CorrectDecision.count("B") != 0 and DealerDecisions.count("B") != 0: # Makes sure lists arent empty to avoid divide by zero error.
            
            DealerCorrectCount = 0
            for i in range (0, len(CorrectDecision)):
                if CorrectDecision[i] == "B" and DealerDecisions[i] == "B":
                    DealerCorrectCount = DealerCorrectCount + 1
            
            DealerIncorrectCount = 0
            for i in range (0, len(CorrectDecision)):
                if CorrectDecision[i] == "B" and DealerDecisions[i] == "L":
                    DealerIncorrectCount = DealerIncorrectCount + 1
            
            if DealerCorrectCount == 0: # Anti Zero Error. Minimal effect on calculations.
                DealerCorrectCount = 1
            if DealerIncorrectCount == 0:
                DealerIncorrectCount = 1
            
            #if VM.Debugging == 2: # Runs if debugging is enabled.
            print("\nCorrect Blank Count = ", CorrectDecision.count("B"))
            print("Dealer Correct Count = ", DealerCorrectCount)
            print("Dealer Incorrect Count = ", DealerIncorrectCount)
            
            ShellCount = CorrectDecision.count("B") # Set "ShellCount" variable.

            DealerCorrectAnalysis = ((DealerCorrectCount / ShellCount) * 100)
            DealerIncorrectAnalysis = ((DealerIncorrectCount / ShellCount) * 100)

            print("\nDealer Correct Analysis = ", DealerCorrectAnalysis)
            print("Dealer Incorrect Analysis = ", DealerIncorrectAnalysis)

            Analysis = DealerIncorrectAnalysis - DealerCorrectAnalysis
            
            if VM.Debugging == 2: # Runs if debugging is enabled.
                print("Analysis = ", Analysis) # Print the results of the analysis.
            
            if Analysis >= 0:
                Decision = "ShootSelf"
            else:
                Decision = "ShootPlayer"
        else:
            print("\n(Not enough live shells have been shot to analyse.)")
            Decision = "ShootSelf"
    
    return Decision

######################################## TESTING STUFF ########################################

def Test():
    global PlayerDecisions
    global DealerDecisions
    global CorrectDecision

    DealerDecisions = ['L', 'L', 'B', 'B', 'L', 'B', 'L']
    CorrectDecision = ['B', 'B', 'L', 'B', 'L', 'L', 'B']
    
    AnalysisResult = Analyse("Blank")
    print("Analysis Result:", AnalysisResult)
 
#Test()