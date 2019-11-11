"""
TAN, King James Zoren C.
2019-69363
CMSC 12 T-1L

BATTLESHIP AI SIMULATOR

This is an extra extension of the main battleship game code. This code generates a board and then
defeats it using the AI. Many of the functions here are from the main battleship code.
The AI has the same strategy but the AI code was slightly modified to fight its own board
since there is no player. Code comments about the AI with explanation are on the main battleship code.

This is a game where players try to hit the other player’s ships. Each player secretly arranges
their ships on their grid. During each round a player announces the target coordinate in the
opponent’s grid to be shot at. A player wins when all the opponent’s ships have been sunk.
Must include:
❏ A smart AI opponent
"""

import random
import time
import os

# AI BATTLESHIP TACTIC SIMULATOR
# This is an extension of the main battleship game. This code generates a board and then
# defeats it using the AI. Many of the functions here are from the main battleship code.
# The AI has the same strategy but the code was slightly modified to fight its own board
# since there is no player

#rowDict is a dictionary that helps convert row coordinates to letters
rowDict = {
    0: "A",
    1: "B",
    2: "C",
    3: "D",
    4: "E",
    5: "F",
    6: "G",
    7: "H",
    8: "I",
    9: "J"
}

#shipSizeDict is a dictionary that keeps the sizes of the ships
shipSizeDict = {
    1: 2,
    2: 3,
    3: 3,
    4: 4,
    5: 5
}

cpuBoard = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

def hitRateCalculate():
    global bombs
    hitrate = 0
    for i in range(10):
        for j in range(10):
            if cpuBoard[i][j] == -2:
                hitrate +=1
    if bombs == 0:
        return 0
    else:
        hitrate = round((hitrate / bombs) * 100, 4)
    return hitrate

def sinkShipChecker(board, evalmode): #evalmode 0 = ship printer, 1 = lose evaluator, 2 = ship counter
    ship1count = 0
    ship2count = 0
    ship3count = 0
    ship4count = 0
    ship5count = 0
    ship1exist = "○"
    ship2exist = "◘"
    ship3exist = "◙"
    ship4exist = "■"
    ship5exist = "≡"
    for line in board:                  #iterate through the board to tally the ships count
        for element in line:
            if element == 1:
                ship1count += 1
            if element == 2:
                ship2count += 1
            if element == 3:
                ship3count += 1
            if element == 4:
                ship4count += 1
            if element == 5:
                ship5count += 1
    if evalmode == 0:                       #ship printer
        if ship1count == 0:                 #if no part of the ship are found
            ship1exist = " "
        if ship2count == 0:
            ship2exist = " "
        if ship3count == 0:
            ship3exist = " "
        if ship4count == 0:
            ship4exist = " "
        if ship5count == 0:
            ship5exist = " "
        print("Ships:", ship1exist, ship2exist, ship3exist, ship4exist, ship5exist)

    elif evalmode == 1:                     #lose evaluator
        global cpuLose
        global playerLose
        if ship1count + ship2count + ship3count + ship4count + ship5count == 0 and board == cpuBoard and gamePhase == 1:
            cpuLose = True
        elif (ship1count + ship2count + ship3count + ship4count + ship5count) == 0 and board == cpuBoard and gamePhase == 1:
            playerLose = True
    
    elif evalmode == 2:                     #ship counter for AI
        allShipCount = 0
        if ship1count != 0:
            allShipCount += 1
        if ship2count != 0:
            allShipCount += 1
        if ship3count != 0:
            allShipCount += 1
        if ship4count != 0:
            allShipCount += 1
        if ship5count != 0:
            allShipCount += 1

        return allShipCount

def printLine():
    print("==================================================================================")

def rowConvert(input):
    if isinstance(input, int):      #checks if input is an int, convert it to letter
        return rowDict[input]
    elif isinstance(input, str):    #checks if input is a letter, convert it to int
        output = [key for (key, value) in rowDict.items() if value == input]
        if len(output) == 1:        #output will only have a content if a letter between A-J was entered
            output = output[0]
            return output

def printBoard():
    global bombs
    rowCount = 0
    print("Bombs fired:", bombs, "| Hit rate:", hitRateCalculate(), "%")
    print("   0 1 2 3 4 5 6 7 8 9   SAMPLE BOARD   ", end="")      #prints the columns
    sinkShipChecker(cpuBoard, 0)
    while rowCount < 10:
        colCount = 0
        print("", rowConvert(rowCount), end=" ")                        #prints the rows
        while colCount < 10:
            if cpuBoard[rowCount][colCount] > -1:                   #sea or hidden ship
                print("·", end=" ")
            elif cpuBoard[rowCount][colCount] == -1:                #bombed sea occupies
                print("*", end=" ")
            elif cpuBoard[rowCount][colCount] == -2:                #bombed ship occupies
                print("♦", end=" ")
            colCount += 1
        print()
        rowCount += 1
    
def clearScreen():
    if os.name == "nt":
        os.system("cls")        #windows
    else:
        os.system("clear")      #linux


def ai():
    global stratMode
    global targetDirection
    global rowHit
    global colHit
    global aiteration
    global usedDirection
    global row
    global col
    global directionsTried
    failedAttempt = 0
    #aiteration test if the game is complete
    while aiteration == 0:
        if sinkShipChecker(cpuBoard, 2) == 0:
            aiteration += 1

        if stratMode == 0:
            row = random.randint(0, 9)
            col = random.randint(0, 4)
            col = col * 2
            if row % 2 == 1:
                col = col + 1

            if cpuBoard[row][col] > -1:
                printLine()
                if cpuBoard[row][col] > 0:                               #if the target has a ship
                    print(" • Computer bombed " + str(rowDict[row]) +  str(col) + ". It's a hit!")
                    cpuBoard[row][col] = -2                              #ship was bombed
                    stratMode = 1                                           #switch to target mode
                    rowHit = row                                            #save vars for target mode
                    colHit = col
                    targetDirection = -1

                elif cpuBoard[row][col] == 0:                            #if the target has no ship
                    print(" • Computer bombed " + str(rowDict[row]) +  str(col) + ". It's a miss!")
                    cpuBoard[row][col] = -1                              #sea was bombed
                printLine()
                break
                
            else:
                failedAttempt += 1
                if failedAttempt > 150:
                    stratMode = 2

        elif stratMode == 1:
            if targetDirection == -1:
                targetDirection = 0

            if targetDirection == 0:      #bottom of most recent hit block
                rowHit += 1
            elif targetDirection == 1:    #top of most recent hit block
                rowHit -= 1
            elif targetDirection == 2:    #right of most recent hit block
                colHit += 1
            elif targetDirection == 3:    #left of most recent hit block
                colHit -= 1
            elif targetDirection == 4:
                stratMode = 0
            
            if rowHit <= 9 and rowHit >= 0 and colHit <= 9 and colHit >= 0:     #coord is valid
                if cpuBoard[rowHit][colHit] > -1:                    #if the target has not been bombed yet
                    printLine()
                    if cpuBoard[rowHit][colHit] > 0:                 #if the target has a ship
                        print(" • Computer bombed " + str(rowDict[rowHit]) +  str(colHit) + ". It's a hit!")
                        cpuBoard[rowHit][colHit] = -2                #ship was bombed

                    elif cpuBoard[rowHit][colHit] == 0:              #if the target has no ship
                        print(" • Computer bombed " + str(rowDict[rowHit]) +  str(colHit) + ". It's a miss!")
                        cpuBoard[rowHit][colHit] = -1                #sea was bombed

                        rowHit = row
                        colHit = col
                        targetDirection += 1
                    printLine()
                    break
                else:
                    rowHit = row
                    colHit = col
                    targetDirection += 1

            else:
                rowHit = row
                colHit = col
                targetDirection += 1
            
        elif stratMode == 2:
            row = random.randint(0, 9)
            col = random.randint(0, 9)

            if cpuBoard[row][col] > -1:
                printLine()
                if cpuBoard[row][col] > 0:                               #if the target has a ship
                    print(" • Computer bombed " + str(rowDict[row]) +  str(col) + ". It's a hit!")
                    cpuBoard[row][col] = -2                              #ship was bombed
                    stratMode = 1                                           #switch to target mode
                    rowHit = row                                            #save vars for target mode
                    colHit = col
                    targetDirection = -1

                elif cpuBoard[row][col] == 0:                            #if the target has no ship
                    print(" • Computer bombed " + str(rowDict[row]) +  str(col) + ". It's a miss!")
                    cpuBoard[row][col] = -1                              #sea was bombed
                printLine()
                break

def cpuSetUp():
    global currentShip
    while currentShip < 6:
        cpuRow = random.randint(0,9)                    #generate a random coord
        cpuCol = random.randint(0,9)
        genDirection = random.randint(0,3)              #ship generation orientation VD VU HR HL
        emptyVerifier = 0
        if cpuBoard[cpuRow][cpuCol] == 0:                                       #starting point of generation not occupied
            #ship is vertical downward
            if genDirection == 0:
                if cpuRow + shipSizeDict[currentShip] - 1 <= 9:           #check if ship will not go out of bounds
                    for i in range(1, shipSizeDict[currentShip]):
                        emptyVerifier += cpuBoard[cpuRow + i][cpuCol]           #check spaces if empty

                    if emptyVerifier == 0:                                      #all spaces verified to be empty
                        #add 1 because ship 1 and ship 2 are an extra block long
                        if currentShip == 2 or currentShip == 1:
                            lengthAdjuster = 1
                        else:
                            lengthAdjuster = 0

                        for i in range(0, shipSizeDict[currentShip]):
                            cpuBoard[cpuRow + i][cpuCol] = currentShip    #generate the ship
                        currentShip += 1

            #ship is vertical upward
            if genDirection == 1:
                if cpuRow - shipSizeDict[currentShip] - 1 >= 0:           #check if ship will not go out of bounds
                    for i in range(1, shipSizeDict[currentShip]):
                        emptyVerifier += cpuBoard[cpuRow - i][cpuCol]           #check spaces if empty

                    if emptyVerifier == 0:                                      #all spaces verified to be empty
                        #add 1 because ship 1 and ship 2 are an extra block long
                        if currentShip == 2 or currentShip == 1:
                            lengthAdjuster = 1
                        else:
                            lengthAdjuster = 0

                        for i in range(0, currentShip + lengthAdjuster):
                            cpuBoard[cpuRow - i][cpuCol] = currentShip    #generate the ship
                        currentShip += 1
            
            #ship is horizontal right
            elif genDirection == 2:
                if cpuCol + shipSizeDict[currentShip] - 1 <= 9:           #check if ship will not go out of bounds
                    for i in range(1, shipSizeDict[currentShip]):
                        emptyVerifier += cpuBoard[cpuRow][cpuCol + i]           #check spaces if empty

                    if emptyVerifier == 0:                                      #all spaces verified to be empty
                        #add 1 because ship 1 and ship 2 are an extra block long
                        if currentShip == 2 or currentShip == 1:
                            lengthAdjuster = 1
                        else:
                            lengthAdjuster = 0

                        for i in range(0, currentShip + lengthAdjuster):
                            cpuBoard[cpuRow][cpuCol + i] = currentShip    #generate the ship

                        currentShip += 1

            #ship is horizontal left
            elif genDirection == 3:
                if cpuCol - shipSizeDict[currentShip] - 1 >= 0:           #check if ship will not go out of bounds
                    for i in range(1, shipSizeDict[currentShip]):
                        emptyVerifier += cpuBoard[cpuRow][cpuCol - i]           #check spaces if empty

                    if emptyVerifier == 0:                                      #all spaces verified to be empty
                        #add 1 because ship 1 and ship 2 are an extra block long
                        if currentShip == 2 or currentShip == 1:
                            lengthAdjuster = 1
                        else:
                            lengthAdjuster = 0

                        for i in range(0, currentShip + lengthAdjuster):
                            cpuBoard[cpuRow][cpuCol - i] = currentShip    #generate the ship
                        currentShip += 1

#----------------------------
bombs = 0
stratMode = 0
targetDirection = -1
usedDirection = -1
directionsTried = 0

row = 0
col = 0
rowHit = 0
colHit = 0
currentShip = 1
aiteration = 0

printLine()
print("WELCOME TO AI BATTLESHIP TACTICS SIMULATOR!")
printLine()
printLine()
print("This will run a simulation of the computer's AI")
printLine()
cpuSetUp()
printBoard()

# You can input a number before pressing enter to change the delay between moves.
# Default delay is 0.05 seconds
try:
    delayInput = float(input("Press Enter to start the simulation."))
    delay = delayInput
except:
    delay = 0.05

while aiteration == 0:
    clearScreen()
    printLine()
    print("WELCOME TO AI BATTLESHIP TACTICS SIMULATOR!")
    printLine()
    ai()
    bombs += 1
    printBoard()
    
    print("STRATEGY USED:   ", end="")
    if stratMode == 0:
        print("HUNT MODE")
    elif stratMode == 1:
        print("TARGET MODE: ", end="")
        if targetDirection == 0:
            print("DOWN")
        elif targetDirection == 1:
            print("UP")
        elif targetDirection == 2:
            print("RIGHT")
        elif targetDirection == 3:
            print("LEFT")
        elif targetDirection == 4:
            print("TERMINATE")
        elif targetDirection == -1:
            print("INITIALIZE")
        
    elif stratMode == 2:
        print("HUNT MODE BRUTE FORCE")

    time.sleep(delay)
print()
print("Computer took", bombs, "moves to finish!", end=" ")

if bombs > 70:
    print("The AI can achieve better than this. Try the simulation again!")
else:
    print()
input("Press Enter to go back to main menu.")