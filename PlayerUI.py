import DealerAI as DAI

def Turn():
    Decision = input("\n##### Shoot The Dealer or Yourself? (1 = The Dealer, 2 = You): ")
    if Decision == "1":
        Outcome = "ShootDealer"
        DAI.Track("Player", "Live") # Update list of previous moves made.
        return Outcome
    if Decision == "2":
        Outcome = "ShootSelf"
        DAI.Track("Player", "Blank") # Update list of previous moves made.
        return Outcome
    else:
        return "ChoiceFailed"