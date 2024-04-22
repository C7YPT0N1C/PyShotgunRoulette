PlayerDecisions =  ['B', 'B', 'L', '-', 'B', '-']
DealerDecisions =  ['-', '-', '-', 'L', '-', 'B']
CorrectDecision =  ['B', 'B', 'L', 'L', 'L']

def CheckCorrectDecisions(Type):
    if Type == "Live":
        print("\nCorrect Count = ", CorrectDecision.count("L"))

        DealerCorrectCount = 0
        for i in range (0, len(CorrectDecision)):
            if DealerDecisions[i] == "L" and CorrectDecision[i] == "L":
                DealerCorrectCount = DealerCorrectCount + 1
        print("Dealer Correct Count = ", DealerCorrectCount)

        PlayerCorrectCount = 0
        for i in range (0, len(CorrectDecision)):
            if PlayerDecisions[i] == "L" and CorrectDecision[i] == "L":
                PlayerCorrectCount = PlayerCorrectCount + 1
        print("Dealer Correct Count = ", PlayerCorrectCount)

    if Type == "Blank":
        print("\nCorrect Count = ", CorrectDecision.count("B"))

        DealerCorrectCount = 0
        for i in range (0, len(CorrectDecision)):
            if DealerDecisions[i] == "B" and CorrectDecision[i] == "B":
                DealerCorrectCount = DealerCorrectCount + 1
        print("Dealer Correct Count = ", DealerCorrectCount)

        PlayerCorrectCount = 0
        for i in range (0, len(CorrectDecision)):
            if PlayerDecisions[i] == "B" and CorrectDecision[i] == "B":
                PlayerCorrectCount = PlayerCorrectCount + 1
        print("Dealer Correct Count = ", PlayerCorrectCount)
    
    return ((PlayerCorrectCount + DealerCorrectCount) / 2)



ShellCount = CorrectDecision.count("L") # Set "ShellCount" variable.
#Analysis = (int(100 / (ShellCount / ((DealerDecisions.count("L") + PlayerDecisions.count("L")) / 2))) / 4)
Analysis = (int(100 / (ShellCount / (CheckCorrectDecisions("Live") + 1))))
print("\nAnalysis =", Analysis, "%")