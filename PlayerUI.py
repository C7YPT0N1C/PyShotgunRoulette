def Turn():
    Decision = (input("\n----- Shoot The Dealer or Yourself? (1 = The Dealer, 2 = You): "))
    if Decision == "1":
        Outcome = "ShootDealer"
        return Outcome
    if Decision == "2":
        Outcome = "ShootSelf"
        return Outcome
    else:
        return "ChoiceFailed"