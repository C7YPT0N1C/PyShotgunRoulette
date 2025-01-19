import LogicManager as LM

def Turn(Player):
    if Player == 1:
        if LM.GameMode == 1:
            Decision = (input("\n----- Shoot The Dealer or Yourself? (1 = The Dealer, 2 = Yourself): "))
        if LM.GameMode == 2:
            Decision = (input("\n----- Player 1, Shoot The Dealer or Yourself? (1 = The Dealer, 2 = Yourself): "))
        
        if Decision == "1":
            Outcome = "ShootDealer"
            return Outcome
        if Decision == "2":
            Outcome = "ShootSelf"
            return Outcome
        else:
            return "ChoiceFailed"
    
    if Player == 2:
        Decision = (input("\n----- Player 2, Shoot Player 1 or Yourself? (1 = Player 1, 2 = Yourself): "))
        if Decision == "1":
            Outcome = "ShootDealer"
            return Outcome
        if Decision == "2":
            Outcome = "ShootSelf"
            return Outcome
        else:
            return "ChoiceFailed"