import LogicManager as LM

import time as time
import random as random

# Use to make code wait X seconds. Makes output more readable while playing.

WaitTimeDebug = 0 # Enable debugging.

def GameWait(Length):
    if Length == "Full":
        time.sleep(1.5)
    if Length == "Short":
        time.sleep(1)

######## HOW WaitTime WORKS ########
# TODO

PauseTime = 2 # Controls how long debugging stats wait to print.
RunTime = 1 # Change this variable inside the "WaitTime" function.
StartTime = 0
EndTime = 0

def WaitTime(Operation):  # Accept StartTime as a parameter
    global StartTime
    global EndTime

    global RunTime

    if Operation == "Pause": # Controls how long debugging stats wait to print.
        time.sleep(PauseTime)

    if Operation == "Wait": # Make code wait RunTime seconds.
        time.sleep(RunTime)
        
    if Operation == "Reset":
        RunTime = 1 # Change RunTime variable here.
        if WaitTimeDebug == 1:
            print("\n###DEBUGGING### ! WARNING: TOTAL RUNTIME RESET. Run Time:", RunTime, "s. !")
    
    if Operation == "Start":
        StartTime = 0
        EndTime = 0
        
        if WaitTimeDebug == 1:
            print("\n###DEBUGGING### ! WARNING: WAITING STARTED. !")
        
        StartTime = time.perf_counter()
    
    if Operation == "End":
        EndTime = time.perf_counter()
        
        if WaitTimeDebug == 1:
            print("\n###DEBUGGING### ! WARNING: WAITING ENDED. Previous Run time:", RunTime, "s. !")

            WaitTime("Pause")
            print("###DEBUGGING### ! StartTime =", StartTime, "s. !")
            print("###DEBUGGING### ! EndTime =", EndTime, "s. !")

        RunTime = EndTime - StartTime

        if WaitTimeDebug == 1:
            WaitTime("Pause")
            print("###DEBUGGING### ! WARNING: WAITING ENDED. Returning Current Run time:", RunTime, "s. !")

        ########################################
        
        RunTimeCap = 4
        RunTimeDivider = 4
        RunTimeMultiplyer = 2

        if WaitTimeDebug == 1:
            WaitTime("Pause")
            print("\n###DEBUGGING### ! RunTimeCap =", RunTimeCap, "!")
        
        while RunTime >= RunTimeCap:
            if WaitTimeDebug == 1:
                print("\n###DEBUGGING### ! RunTime UNSUITABLE SIZE. !")
            
            RunTime = RunTime / random.randint(1, RunTimeDivider)
            RunTime = RunTime * random.randint(1, RunTimeMultiplyer)
            
            if WaitTimeDebug == 1:
                print("###DEBUGGING### ! UPDATED Run time:", RunTime, "s. !")
        
        if WaitTimeDebug == 1:
            print("\n###DEBUGGING### ! Returning Total RunTime as:", RunTime, "s. !")
        
        return RunTime
    
    if Operation == "ReportToPlayer":
        time.sleep(WaitTime("End")) # Wait DealerWaitTime seconds. Makes output more readable while playing and makes it look like the Dealer is "thinking".