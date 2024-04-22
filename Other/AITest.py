import random

MaxChoices = 3

AILevel = 1

Choice1 = random.randint(1, MaxChoices)
Choice2 = random.randint(1, MaxChoices)
Choice3 = random.randint(1, MaxChoices)

if AILevel == 1:
    ChoicesList = [Choice1]
if AILevel == 2:
    ChoicesList = [Choice1, Choice2]
if AILevel == 3:
    ChoicesList = [Choice1, Choice2, Choice3]

FinalChoice = 0

print(ChoicesList)

for Choice in range (1, (MaxChoices + 1)):
    print("Final Choice:", FinalChoice)
    print("Choice:", Choice)
    print("Choice appears this number of times:", ChoicesList.count(Choice))
    if ChoicesList.count(Choice) >= FinalChoice:
        FinalChoice = Choice

print("The Final Choice is Choice", FinalChoice)