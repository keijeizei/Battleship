"""
TAN, King James Zoren C.
2019-69363
CMSC 12 T-1L

BATTLESHIP
This is a game where players try to hit the other player’s ships. Each player secretly arranges
their ships on their grid. During each round a player announces the target coordinate in the
opponent’s grid to be shot at. A player wins when all the opponent’s ships have been sunk.
Must include:
❏ Saving and loading the current state of the game using files
❏ File implementation for high scores
❏ A smart AI opponent
"""

import random
import time
import os

#---------------------------------------------DICTIONARIES AND FUNCTIONS
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

#shipDict is a dictionary that keeps the names of the ship
shipDict = {
    1: "Destroyer",
    2: "Submarine",
    3: "Cruiser",
    4: "Battleship",
    5: "Carrier"
}

#shipSizeDict is a dictionary that keeps the sizes of the ships
shipSizeDict = {
    1: 2,
    2: 3,
    3: 3,
    4: 4,
    5: 5
}

#shipLooks is a dictionary that keeps the appearance of the ships
shipLooks = {
    1: "○ ○",
    2: "◘ ◘ ◘",
    3: "◙ ◙ ◙",
    4: "■ ■ ■ ■",
    5: "≡ ≡ ≡ ≡ ≡"
}

playerBoard = [
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

#---------------------------------------------PREPARATION PHASE FUNCTIONS
def shipBuilder(startR, startC, endR, endC):
    global currentShip
    length = shipSizeDict[currentShip] - 1
    buildDirection = -1

    if startR + length == endR and startC == endC:          #ship is vertical downward
        buildDirection = 0
    elif startR - length == endR and startC == endC:        #ship is vertical upward
        buildDirection = 1
    elif startR == endR and startC + length== endC:         #ship is horizontal right
        buildDirection = 2
    elif startR == endR and startC - length == endC:         #ship is horizontal left
        buildDirection = 3

    if buildDirection != -1:
        emptyTester = 0
        for i in range(0, length + 1):
            if buildDirection == 0:
                emptyTester += playerBoard[startR + i][startC]
            elif buildDirection == 1:
                emptyTester += playerBoard[startR - i][startC]
            elif buildDirection == 2:
                emptyTester += playerBoard[startR][startC + i]
            elif buildDirection == 3:
                emptyTester += playerBoard[startR][startC - i]

    if buildDirection != -1 and emptyTester == 0:
        for i in range(0, length + 1):
            if buildDirection == 0:
                playerBoard[startR + i][startC] = currentShip
            elif buildDirection == 1:
                playerBoard[startR - i][startC] = currentShip
            elif buildDirection == 2:
                playerBoard[startR][startC + i] = currentShip
            elif buildDirection == 3:
                playerBoard[startR][startC - i] = currentShip
        
        print(shipDict[currentShip], "deployed successfully.")
        currentShip += 1
    else:
        print("Ship should be", shipSizeDict[currentShip], "tiles long do not overlap other ships.")

def printPlayerBoard():
    rowCount = 0
    print("   0 1 2 3 4 5 6 7 8 9   YOUR TERRITORY   ", end="")     #prints the columns
    sinkShipChecker(playerBoard, 0)
    while rowCount < 10:
        colCount = 0
        print("", rowConvert(rowCount), end=" ")                    #prints the rows
        while colCount < 10:
            if playerBoard[rowCount][colCount] == 0:                #unoccupied space
                print("·", end=" ")
            elif playerBoard[rowCount][colCount] == 1:              #1st ship occupies
                print("○", end=" ")
            elif playerBoard[rowCount][colCount] == 2:              #2nd ship occupies
                print("◘", end=" ")
            elif playerBoard[rowCount][colCount] == 3:              #3rd ship occupies
                print("◙", end=" ")
            elif playerBoard[rowCount][colCount] == 4:              #4th ship occupies
                print("■", end=" ")
            elif playerBoard[rowCount][colCount] == 5:              #5th ship occupies
                print("≡", end=" ")
            elif playerBoard[rowCount][colCount] == -1:             #bombed sea occupies
                print("*", end=" ")
            elif playerBoard[rowCount][colCount] == -2:             #bombed ship occupies
                print("X", end=" ")
            colCount += 1
        print()
        rowCount += 1

def printCPUBoard():
    rowCount = 0
    print("   0 1 2 3 4 5 6 7 8 9   RADAR            ", end="")      #prints the columns
    sinkShipChecker(cpuBoard, 0)
    while rowCount < 10:
        colCount = 0
        print("", rowConvert(rowCount), end=" ")                     #prints the rows
        while colCount < 10:
            """
            #THIS CODE LETS YOU SEE THE CPU's SHIPS (used for debugging)
            if cpuBoard[rowCount][colCount] == 0:                   #unoccupied space
                print("·", end=" ")
            elif cpuBoard[rowCount][colCount] == 1:                 #1st ship occupies
                print("○", end=" ")
            elif cpuBoard[rowCount][colCount] == 2:                 #2nd ship occupies
                print("◘", end=" ")
            elif cpuBoard[rowCount][colCount] == 3:                 #3rd ship occupies
                print("◙", end=" ")
            elif cpuBoard[rowCount][colCount] == 4:                 #4th ship occupies
                print("■", end=" ")
            elif cpuBoard[rowCount][colCount] == 5:                 #5th ship occupies
                print("≡", end=" ")
            elif cpuBoard[rowCount][colCount] == -1:                #bombed ship occupies
                print("*", end=" ")
            elif cpuBoard[rowCount][colCount] == -2:                #bombed ship occupies
                print("♦", end=" ")
            """
            if cpuBoard[rowCount][colCount] > -1:                   #sea or hidden ship
                print("·", end=" ")
            elif cpuBoard[rowCount][colCount] == -1:                #bombed sea occupies
                print("*", end=" ")
            elif cpuBoard[rowCount][colCount] == -2:                #bombed ship occupies
                print("♦", end=" ")
            colCount += 1
        print()
        rowCount += 1

def playerSetUp():
    noEndpoint = False      #to catch the no possible endpoint error
    printLine()
    print("PREPARATION PHASE")
    printLine()
    print("Place your ships by specifying the two ends of the ship.")
    printLine()
    global currentShip
    while currentShip < 6:
        try:
            printPlayerBoard()
            print("Place your", shipDict[currentShip], "ship on the board (a ship", shipSizeDict[currentShip], "tiles long)", shipLooks[currentShip])

            startInput = input("Enter coordinates of the first end of the ship (ex. A1): ")
            if len(startInput) > 2:
                raise Exception()

            #This code splits the coords and convert the row letter to its int counterpart
            startInput = startInput.upper()
            startR = rowConvert(startInput[0])
            startC = int(startInput[1])

            possible1 = ""
            possible2 = ""
            possible3 = ""
            possible4 = ""

            if playerBoard[startR][startC] > 0:         #already occupied
                raise Exception()

            #possible endpoints should not include ships that overlap
            length = shipSizeDict[currentShip] - 1
            if startR + shipSizeDict[currentShip] - 1 <= 9:         #end tile should not be out of bounds
                emptyTester = 0
                for i in range(0, length + 1):                      #test tiles if they are empty
                    emptyTester += playerBoard[startR + i][startC]
                if emptyTester == 0:
                    possible1 = str(rowConvert(startR + shipSizeDict[currentShip] - 1) + str(startC)) + " "

            if startR - shipSizeDict[currentShip] + 1 >= 0:
                emptyTester = 0
                for i in range(0, length + 1):
                    emptyTester += playerBoard[startR - i][startC]
                if emptyTester == 0:
                    possible2 = str(rowConvert(startR - shipSizeDict[currentShip] + 1) + str(startC)) + " "

            if startC + shipSizeDict[currentShip] - 1 <= 9:
                emptyTester = 0
                for i in range(0, length + 1):
                    emptyTester += playerBoard[startR][startC + i]
                if emptyTester == 0:
                    possible3 = str(rowConvert(startR)) + str(startC + shipSizeDict[currentShip] - 1) + " "

            if startC - shipSizeDict[currentShip] + 1 >= 0:
                emptyTester = 0
                for i in range(0, length + 1):
                    emptyTester += playerBoard[startR][startC - i]
                if emptyTester == 0:
                    possible4 = str(rowConvert(startR)) + str(startC - shipSizeDict[currentShip] + 1) + " "

            if possible1 == "" and possible2 == "" and possible3 == "" and possible4 == "":
                noEndpoint = True
                raise Exception()

            print()
            print("Possible endpoints: " + possible1 + possible2 + possible3 + possible4)
            endInput = input("Enter coordinates of the other end of the ship (ex. A2): ")
            if len(endInput) > 2:
                raise Exception()

            endInput = endInput.upper()
            endR = rowConvert(endInput[0])
            endC = int(endInput[1])

            if playerBoard[endR][endC] > 0:         #already occupied
                raise Exception()
            clearScreen()
            printLine()
            print("PREPARATION PHASE")
            printLine()
            shipBuilder(startR, startC, endR, endC)
            printLine()
        except:                                     #if an error is raised, it means that coord is invalid
            clearScreen()
            printLine()
            print("PREPARATION PHASE")
            printLine()
            if noEndpoint:
                print("The coordinate you picked have no possible endpoints.")
            else:
                print("Invalid coordinate or coordinate already occupied.")
            printLine()
        
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
                if cpuRow + shipSizeDict[currentShip] - 1 <= 9:                 #check if ship will not go out of bounds
                    for i in range(1, shipSizeDict[currentShip]):
                        emptyVerifier += cpuBoard[cpuRow + i][cpuCol]           #check spaces if empty

                    if emptyVerifier == 0:                                      #all spaces verified to be empty
                        #add 1 because ship 1 and ship 2 are an extra tile long
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
                        #add 1 because ship 1 and ship 2 are an extra tile long
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
                        #add 1 because ship 1 and ship 2 are an extra tile long
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
                        #add 1 because ship 1 and ship 2 are an extra tile long
                        if currentShip == 2 or currentShip == 1:
                            lengthAdjuster = 1
                        else:
                            lengthAdjuster = 0

                        for i in range(0, currentShip + lengthAdjuster):
                            cpuBoard[cpuRow][cpuCol - i] = currentShip    #generate the ship
                        currentShip += 1

#---------------------------------------------CALCULATOR AND EVALUATOR FUNCTIONS
def sinkShipChecker(board, evalmode):
    """
    board argument takes playerBoard or cpuBoard
    evalmode argument:
    0 = ship printer
    1 = lose evaluator
    2 = ship left counter
    """
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
        global gamePhase
        if ship1count + ship2count + ship3count + ship4count + ship5count == 0 and board == cpuBoard and gamePhase == 1:
            cpuLose = True
        elif (ship1count + ship2count + ship3count + ship4count + ship5count) == 0 and board == playerBoard and gamePhase == 1:
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

def hitRateCalculate(bombs):
    """
    bombs argument is the number of bombs deployed
    """
    hitrate = 0
    for i in range(10):
        for j in range(10):
            if cpuBoard[i][j] == -2:
                hitrate +=1
    if bombs == 0:                                              #avoid zero division
        return 0
    else:
        hitrate = round((hitrate / bombs) * 100, 4)
    return hitrate

#---------------------------------------------FILE HANDLING FUNCTIONS
def highScore(score, mode):
    """
    score argument is the score that will be saved
    mode argument:
    0 = save high score
    1 = print the high scores
    """
    try:                                                        #try if file exists
        highScore = open("highscore.txt", "r")
        highScoreList = highScore.read()
        highScoreList = highScoreList.split(", ")
        highScore.close()
    except:
        highScore = open("highscore.txt", "w+")                 #create the file if it doesn't exist
        highScore.close()

        highScore = open("highscore.txt", "r")                  #reads the file and create a list
        highScoreList = highScore.read()
        highScoreList = highScoreList.split(", ")
        highScore.close()
    highScoreList.pop(-1)                                       #pop the empty element [''] at the end of the list
    for place in range(0, len(highScoreList)):
        highScoreList[place] = int(highScoreList[place])        #convert to int
    if mode == 0:
        highScoreList.append(score)
        highScoreList.sort()

        highScore = open("highscore.txt", "w")
        for namescore in highScoreList:
            highScore.write(str(namescore) + ", ")
        highScore.close()
        print("Your score has been saved!")

    if mode == 1:
        printTitle()
        if len(highScoreList) == 0:
            print("No scores yet. Play a new game now!")
        else:
            print("=================LEADERBOARDS=================")
            for i in range(len(highScoreList)):
                print(" ", i + 1, ": BOMBS FIRED:", highScoreList[i], "  HIT RATE:", round(17/highScoreList[i] * 100, 4), "%")
            highScore.close()
        print()
        input("Press Enter to go back to main menu.")
        mainMenu()

def saveBoard():
    global turn
    savefile = open("savefile.txt", "w+")
    for row in range(10):
        for col in range(10):
            savefile.write(str(playerBoard[row][col]))      #index [0] to index [99]
            savefile.write(", ")
    for row in range(10):
        for col in range(10):
            savefile.write(str(cpuBoard[row][col]))         #index [100] to index [199]
            savefile.write(", ")

    savefile.write(str(turn) + ", ")                        #turn is the 201st value (index [200])
    savefile.write(str(stratMode) + ", ")
    savefile.write(str(targetDirection) + ", ")
    savefile.write(str(rowHit) + ", ")
    savefile.write(str(colHit) + ", ")
    savefile.write(str(bombs) + ", ")
    savefile.write(str(row) + ", ")
    savefile.write(str(col) + ", ")

    savefile.close()

#---------------------------------------------GAME MANAGEMENT FUNCTIONS
def mainMenu():
    while True:                                 #loop until a return statement is executed
        clearScreen()
        printTitle()
        print(" [1] CONTINUE")
        print(" [2] NEW GAME")
        print(" [3] VIEW LEADERBOARDS")
        print(" [4] SEE IF MY AI IS SMART")
        print(" [0] QUIT.")
        print()
        choice = input("Enter choice: ")
        if choice == "1":
            clearScreen()
            continueGame()
            return
        elif choice == "2":
            clearScreen()
            newGame()
            return
        elif choice == "3":
            clearScreen()
            highScore(0, 1)
            return
        elif choice == "4":
            clearScreen()
            try:
                if os.name == "nt":
                    os.system("python aisimulator.py")        #windows
                else:
                    os.system("python3 aisimulator.py")       #linux
            except:
                print("AI simulator file is missing.")
        elif choice == "0":
            quitChoice = input("Are you sure you want to quit? [y/n]: ")
            quitChoice = quitChoice.upper()
            if quitChoice == "Y":
                quit()
        else:
            print("Invalid input. Enter only 1, 2, 3, 4, or 0.")
            time.sleep(1)
        print()

def mainGame():
    global playerLose
    global cpuLose
    global gamePhase
    global turn
    global bombs

    #print the top bar when the game starts
    printLine()
    print("                     Bombs fired:", bombs, "| Hit rate:", hitRateCalculate(bombs), "%")
    if turn % 2 == 0:
        printLine()
        print(" • Your previous turns will appear here...")
        printLine()
        print(" • Computer's previous turns will appear here...")
        printLine()
    else:
        printLine()
        print(" • Your previous turns will appear here...")

    gamePhase = 1
    while True:                                                             #while game is still not done
        sinkShipChecker(cpuBoard, 1)                                            #evaluate if cpu lost
        sinkShipChecker(playerBoard, 1)                                         #evaluate if player lost

        if turn % 2 == 0 and playerLose == False and cpuLose == False:      #player's turn
            printCPUBoard()
            printPlayerBoard()
            turnInput = input(("Your turn. Enter the target coordinate (ex. A1): "))

            clearScreen()
            printLine()
            #because stats are printed before the move, bombs need to be bombs + 1
            print("                     Bombs fired:", bombs + 1, "| Hit rate:", hitRateCalculate(bombs + 1), "%")
            printLine()

            try:
                if len(turnInput) != 2:                                         #input should be 2 characters long
                    raise Exception()

                turnInput = turnInput.upper()
                row = rowConvert(turnInput[0])
                col = int(turnInput[1])

                if cpuBoard[row][col] > -1:                                     #if the target has not been bombed yet
                    if cpuBoard[row][col] > 0:                                  #if the target has a ship
                        cpuShipBefore = sinkShipChecker(cpuBoard, 2)            #count ships before bombing
                        cpuBoard[row][col] = -2                                 #ship was bombed

                        clearScreen()
                        printLine()
                        #because stats are printed before the move, bombs need to be bombs + 1
                        #re-print the stats again after bombing a tile to make hit rate accurate
                        print("                     Bombs fired:", bombs + 1, "| Hit rate:", hitRateCalculate(bombs + 1), "%")
                        printLine()

                        print(" • You bombed " + turnInput + ". It's a hit!", end=" ")
                        if sinkShipChecker(cpuBoard, 2) < cpuShipBefore:        #compare ships after bombing
                            print("You sank one of your opponent's ships!")
                        else:
                            print()
                        
                    elif cpuBoard[row][col] == 0:                               #if the target has no ship
                        print(" • You bombed " + turnInput + ". It's a miss!")
                        cpuBoard[row][col] = -1                                 #target has been hit
                    turn += 1
                    bombs += 1
                else:
                    print(" • No need to bomb the same location twice!")
                    printLine()
                    print(" • You can pick another coordinate to bomb.")
                    printLine()
            except:
                print(" • Invalid coordinate. Enter a coordinate from A0 to J9.")
                printLine()
                print(" • You can pick another coordinate to bomb.")
                printLine()

        elif turn % 2 == 1 and cpuLose == False and playerLose == False:        #cpu's turn
            cpuAI()
        elif playerLose:
            printCPUBoard()
            printPlayerBoard()
            print("All your ships have sunk. It's game over. Let's play again!")
            os.remove("savefile.txt")                                               #deletes the save file
            break
        elif cpuLose:
            printLine()
            printCPUBoard()
            printPlayerBoard()
            print("You win! You took", bombs, "bombs to beat the computer!")
            highScore(bombs, 0)
            os.remove("savefile.txt")                                               #deletes the save file
            break
    input("Press Enter to go back to main menu.")
    gamePhase = 0
    clearBoard()
    
    mainMenu()      

def continueGame():
    loading()
    try:                                                                   #try if save file exists
        savefile = open("savefile.txt", "r")
        tempBoard = savefile.read()
        tempBoard = tempBoard.split(", ")
        for tile in range(100):                                            #load the playerBoard
            playerBoard[tile // 10][tile % 10] = int(tempBoard[tile])
        for tile in range(100, 200):                                       #load the cpuBoard
            cpuBoard[(tile - 100) // 10][(tile - 100) % 10] = int(tempBoard[tile])
        global turn
        global stratMode
        global targetDirection
        global rowHit
        global colHit
        global bombs
        global row
        global col
        turn = int(tempBoard[200])                                          #load the other variables
        stratMode = int(tempBoard[201])
        targetDirection = int(tempBoard[202])
        rowHit = int(tempBoard[203])
        colHit = int(tempBoard[204])
        bombs = int(tempBoard[205])
        row = int(tempBoard[206])
        col = int(tempBoard[207])
        savefile.close()

    except:                                                                 #start new game prep phase if save file doesn't exists
        clearScreen()
        printLine()
        print("Save file not found. A new game will be started.")
        printLine()
        time.sleep(1)
        #-----PLAYER PREPARATION PHASE
        newGame()
        
def newGame():
    global currentShip
    #-----CPU PREPARATION PHASE
    loading()
    cpuSetUp()
    clearScreen()
    #-----PLAYER PREPARATION PHASE
    currentShip = 1
    playerSetUp()
    printPlayerBoard()
    printLine()
    print("All ships deployed. Preparations complete.")
    printLine()
    saveBoard()                                                             #auto save
    #-----PRE-BATTLE PHASE
    time.sleep(1)
    print("The war has begun!")
    time.sleep(1)
    if turn % 2 == 0:
        print("You will have the first move.")
    else:
        print("Computer will have the first move.")
    time.sleep(1)
    input("Press Enter to enter the battlefield!")
    clearScreen()

#---------------------------------------------CPU AI FUNCTION
def cpuAI():
    global turn
    global stratMode
    global targetDirection
    global rowHit
    global colHit
    global row
    global col
    failedAttempt = 0
    # The AI is divided into 3 modes. Hunt mode (0) uses parity to hunt for ships efficiently.
    # Once it successfully bombs a ship, it switches to Target mode (1) where it attacks the 
    # four adjacent tiles around the bombed ship.
    # Once Hunt mode parity is no longer viable, it switches to Hunt mode brute force (2) where
    # it randomly choose a tile to clean any remaining ship parts.

    while turn % 2 == 1:
        if stratMode == 0:
            # HUNT MODE
            # The strategy of hunt mode is to use parity or checkerboarding. It only attacks on
            # alternating tiles since every ship occupies atleast two tiles.
            row = random.randint(0, 9)
            col = random.randint(0, 4)
            col = col * 2
            if row % 2 == 1:
                col = col + 1

            if playerBoard[row][col] > -1:                                  #target has not been bombed yet
                printLine()
                if playerBoard[row][col] > 0:                               #target has a ship
                    print(" • Computer bombed " + str(rowDict[row]) +  str(col) + ". It's a hit!", end=" ")
                    playerShipBefore = sinkShipChecker(playerBoard, 2)      #count ships before bombing
                    playerBoard[row][col] = -2                              #ship was bombed
                    if sinkShipChecker(playerBoard, 2) < playerShipBefore:  #compare ships after bombing
                        print("Computer sank one of your ships!")
                    else:
                        print()
                    stratMode = 1                                           #switch to target mode
                    rowHit = row                                            #save vars for target mode
                    colHit = col
                    targetDirection = 0

                elif playerBoard[row][col] == 0:                            #if the target has no ship
                    print(" • Computer bombed " + str(rowDict[row]) +  str(col) + ". It's a miss!")
                    playerBoard[row][col] = -1                              #sea was bombed
                
                turn += 1
                saveBoard()
                printLine()
            else:
                #if hunt mode is not viable anymore, force switch to hunt mode brute force
                failedAttempt += 1
                if failedAttempt > 150:
                    stratMode = 2

        elif stratMode == 1:
            # TARGET MODE
            # Target mode attacks the adjacent tiles of the bombed tile of hunt mode.
            # Once it miss, it will attack the next adjacent tile until all four directions are bombed

            if targetDirection == 0:        #bottom of most recent bombed tile
                rowHit += 1
            elif targetDirection == 1:      #top of most recent bombed tile
                rowHit -= 1
            elif targetDirection == 2:      #right of most recent bombed tile
                colHit += 1
            elif targetDirection == 3:      #left of most recent bombed tile
                colHit -= 1
            elif targetDirection == 4:      #iteration completed, go back to hunt mode
                stratMode = 0
            
            if rowHit <= 9 and rowHit >= 0 and colHit <= 9 and colHit >= 0:     #coord is valid
                if playerBoard[rowHit][colHit] > -1:                            #target has not been bombed yet
                    printLine()
                    if playerBoard[rowHit][colHit] > 0:                         #target has a ship
                        print(" • Computer bombed " + str(rowDict[rowHit]) +  str(colHit) + ". It's a hit!", end=" ")
                        playerShipBefore = sinkShipChecker(playerBoard, 2)      #count ships before bombing
                        playerBoard[rowHit][colHit] = -2                        #ship was bombed
                        if sinkShipChecker(playerBoard, 2) < playerShipBefore:  #compare ships after bombing
                            print("Computer sank one of your ships!")
                        else:
                            print()

                    elif playerBoard[rowHit][colHit] == 0:                      #if the target has no ship
                        print(" • Computer bombed " + str(rowDict[rowHit]) +  str(colHit) + ". It's a miss!")
                        playerBoard[rowHit][colHit] = -1                        #sea was bombed

                        rowHit = row                                            #get the original coords
                        colHit = col
                        targetDirection += 1                                    #proceed to the next adjacent tile
                    turn += 1
                    saveBoard()
                    printLine()
                else:
                    rowHit = row                                                #get the original coords
                    colHit = col
                    targetDirection += 1                                        #just proceed to the next adjacent tile

            else:
                rowHit = row                                                    #get the original coords
                colHit = col
                targetDirection += 1                                            #just proceed to the next adjacent tile
            
        elif stratMode == 2:
            # HUNT MODE BRUTE FORCE
            # When parity strategy is no longer viable, Hunt mode brute force will be used.
            # it will pick a random square without the checkerboarding restriction
            # and will proceed to the same process as the original hunt mode.
            row = random.randint(0, 9)
            col = random.randint(0, 9)

            if playerBoard[row][col] > -1:                                  #target has not been bombed yet
                printLine()
                if playerBoard[row][col] > 0:                               #target has a ship
                    print(" • Computer bombed " + str(rowDict[row]) +  str(col) + ". It's a hit!", end=" ")
                    playerShipBefore = sinkShipChecker(playerBoard, 2)      #count ships before bombing
                    playerBoard[row][col] = -2                              #ship was bombed
                    if sinkShipChecker(playerBoard, 2) < playerShipBefore:  #compare ships after bombing
                        print("Computer sank one of your ships!")
                    else:
                        print()

                    stratMode = 1                                           #switch to target mode
                    rowHit = row                                            #save vars for target mode
                    colHit = col
                    targetDirection = -1

                elif playerBoard[row][col] == 0:                            #if the target has no ship
                    print(" • Computer bombed " + str(rowDict[row]) +  str(col) + ". It's a miss!")
                    playerBoard[row][col] = -1                              #sea was bombed
                turn += 1
                saveBoard()
                printLine()

#---------------------------------------------MISC FUNCTIONS
def clearScreen():
    if os.name == "nt":
        os.system("cls")        #windows
    else:
        os.system("clear")      #linux

def clearBoard():
    for i in range(10):
        for j in range(10):
            playerBoard[i][j] = 0
            cpuBoard[i][j] = 0

def loading():
    """
    This loading function has no role in loading anything in the game.
    The only purpose of this function is to give delay and suspense in the game,
    giving excitement to the players.
    """
    clearScreen()
    for i in range(101):
        print(" [" + ("█" * (i//5)) + (" " * (20-(i//5))) + "] Loading... " + str(i) + "%", end="\r")
        time.sleep(0.001)
    
def printLine():
    print("==================================================================================")

def printTitle():
    print()
    print(" ██████╗  █████╗ ████████╗████████╗██╗     ███████╗███████╗██╗  ██╗██╗██████╗ ██╗") 
    print(" ██╔══██╗██╔══██╗╚══██╔══╝╚══██╔══╝██║     ██╔════╝██╔════╝██║  ██║██║██╔══██╗██║")    
    print(" ██████╔╝███████║   ██║      ██║   ██║     █████╗  ███████╗███████║██║██████╔╝██║")  
    print(" ██╔══██╗██╔══██║   ██║      ██║   ██║     ██╔══╝  ╚════██║██╔══██║██║██╔═══╝ ╚═╝")  
    print(" ██████╔╝██║  ██║   ██║      ██║   ███████╗███████╗███████║██║  ██║██║██║     ██╗")  
    print(" ╚═════╝ ╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝     ╚═╝")
    print()

def rowConvert(input):
    if isinstance(input, int):      #checks if input is an int, convert it to letter
        return rowDict[input]
    elif isinstance(input, str):    #checks if input is a letter, convert it to int
        output = [key for (key, value) in rowDict.items() if value == input]
        if len(output) == 1:        #output will only have a content if a letter between A-J was entered
            output = output[0]
            return output

#------------------------------------DECLARE VARIABLES-----------------------------------
#declare variables, this can be overwritten later if a savefile exists
gamePhase = 0                       #0 is prep phase, 1 is battle phase.
turn = random.randint(0, 1)         #declares who turns first

playerLose = False                  #both players are alive
cpuLose = False

stratMode = 0                       #default stratmode for AI is hunt mode
targetDirection = 0                 #target direction starts at 0

rowHit = 0                          #rowHit, colHit, row, and col are mostly for AI use
colHit = 0
row = 0
col = 0

bombs = 0                           #counts how many bombs the player has deployed
currentShip = 1                     #current ship for player and cpu preparation

#----------------------------------------MAIN GAME---------------------------------------
mainMenu()
mainGame()