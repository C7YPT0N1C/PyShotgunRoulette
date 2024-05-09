import DealerAI as DAI

def Turn(GameMode, CurrentTurn):
    if CurrentTurn == "Player1":
        if GameMode == 2: # Player 1 VS Player 2.
            Decision = input("\n##### Shoot Player 2 or Yourself? (1 = Player 2, 2 = Yourself): ")
            if Decision == "1":
                Outcome = "ShootPlayer2"
                DAI.Track("Player", "Live") # Update list of previous moves made.
                return Outcome
            if Decision == "2":
                Outcome = "ShootPlayer1"
                DAI.Track("Player", "Blank") # Update list of previous moves made.
                return Outcome
            else:
                return "ChoiceFailed"
        
        else: # Player 1 VS Dealer.
            Decision = input("\n##### Shoot The Dealer or Yourself? (1 = The Dealer, 2 = Yourself): ")
            if Decision == "1":
                Outcome = "ShootDealer"
                DAI.Track("Player", "Live") # Update list of previous moves made.
                return Outcome
            if Decision == "2":
                Outcome = "ShootPlayer1"
                DAI.Track("Player", "Blank") # Update list of previous moves made.
                return Outcome
            else:
                return "ChoiceFailed"
            
    if GameMode == 2: # Player 1 VS Player 2.
        if CurrentTurn == "Player2":
            Decision = input("\n##### Shoot Player 1 or Yourself? (1 = Player 1, 2 = Yourself): ")
            if Decision == "1":
                Outcome = "ShootPlayer1"
                DAI.Track("Player", "Live") # Update list of previous moves made.
                return Outcome
            if Decision == "2":
                Outcome = "ShootPlayer2"
                DAI.Track("Player", "Blank") # Update list of previous moves made.
                return Outcome
            else:
                return "ChoiceFailed"