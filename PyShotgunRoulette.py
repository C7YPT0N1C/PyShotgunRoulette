import sys
import os

GameFiles = os.path.abspath("./Game Files") # Add the "Game Files" folder path to sys.path
sys.path.append(GameFiles)

import Main as Main
import LogicManager as LM
import Shotgun as Shotgun
import PlayerUI as PUI
import DealerAI as DAI

######################################## TESTING STUFF ########################################

def DebugMain():
    print("\n! Selecting Player vs Dealer AI Game Mode. !")
    LM.GameMode = 1

    print("\n! Starting game with 'Normal' Dealer AI diffiiculty. !")
    LM.AILevel = 2
    
    print("\n! Activating Debugging. !")
        
    print("\n! Toggling Game Debugging. !")
    LM.GameDebug = 0
    
    print("\n! Toggling Dealer Decision Debugging. !")
    LM.DealerDecisionDebug = 0
    
    print("\n! Toggling Dealer Analysis Debugging. !")
    LM.DealerAnalysisDebug = 0
    
    print("\n! Toggling Shotgun Debugging. !")
    LM.ShotgunDebug = 0
    
    print("\n! Toggling shotgun Balancing. !")
    Main.StartGame(True)

#Shotgun.ShotgunRandomnessTest(8, True)
#Shotgun.LoadShotgunTest(8, True)

######################################## TESTING STUFF ########################################

#DebugMain()
Main.Main()