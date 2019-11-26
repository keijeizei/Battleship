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
    1: "\033[1;32;40m○ ○\033[1;37;40m",
    2: "\033[1;32;40m◘ ◘ ◘\033[1;37;40m",
    3: "\033[1;32;40m◙ ◙ ◙\033[1;37;40m",
    4: "\033[1;32;40m■ ■ ■ ■\033[1;37;40m",
    5: "\033[1;32;40m≡ ≡ ≡ ≡ ≡\033[1;37;40m"
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
        
        print(f" • \033[1;32;40m{shipDict[currentShip]}\033[1;37;40m deployed successfully.")
        currentShip += 1
    else:
        print(f" • Ship should be \033[1;31;40m{shipSizeDict[currentShip]}\033[1;37;40m tiles long do not overlap other ships.")

def printPlayerBoard():
    rowCount = 0
    print("   0 1 2 3 4 5 6 7 8 9   YOUR TERRITORY   ", end="")     #prints the columns
    sinkShipChecker(playerBoard, 0)
    while rowCount < 10:
        colCount = 0
        print("", rowConvert(rowCount), end=" ")                    #prints the rows
        while colCount < 10:
            if playerBoard[rowCount][colCount] == 0:                #unoccupied space
                print("\033[1;34;40m·\033[1;37;40m", end=" ")
            elif playerBoard[rowCount][colCount] == 1:              #1st ship occupies
                print("\033[1;32;40m○\033[1;37;40m", end=" ")
            elif playerBoard[rowCount][colCount] == 2:              #2nd ship occupies
                print("\033[1;32;40m◘\033[1;37;40m", end=" ")
            elif playerBoard[rowCount][colCount] == 3:              #3rd ship occupies
                print("\033[1;32;40m◙\033[1;37;40m", end=" ")
            elif playerBoard[rowCount][colCount] == 4:              #4th ship occupies
                print("\033[1;32;40m■\033[1;37;40m", end=" ")
            elif playerBoard[rowCount][colCount] == 5:              #5th ship occupies
                print("\033[1;32;40m≡\033[1;37;40m", end=" ")
            elif playerBoard[rowCount][colCount] == -1:             #bombed sea occupies
                print("\033[1;35;40m*\033[1;37;40m", end=" ")
            elif playerBoard[rowCount][colCount] == -2:             #bombed ship occupies
                print("\033[1;31;40m♦\033[1;37;40m", end=" ")
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
                print("\033[1;34;40m·\033[1;37;40m", end=" ")
            elif cpuBoard[rowCount][colCount] == -1:                #bombed sea occupies
                print("\033[1;35;40m*\033[1;37;40m", end=" ")
            elif cpuBoard[rowCount][colCount] == -2:                #bombed ship occupies
                print("\033[1;31;40m♦\033[1;37;40m", end=" ")
            colCount += 1
        print()
        rowCount += 1

def playerSetUp():
    noEndpoint = False      #to catch the no possible endpoint error
    printLine(0)
    print("                                   PREPARATION PHASE")
    printLine(1)
    print(" • Place your ships by specifying the two ends of the ship.")
    printLine(2)
    global currentShip
    while currentShip < 6:
        try:
            printPlayerBoard()
            print(f"Place your {shipDict[currentShip]} ship on the board (a ship {shipSizeDict[currentShip]} tiles long) {shipLooks[currentShip]}")

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
            print(f"Possible endpoints: \033[1;32;40m{possible1}{possible2}{possible3}{possible4}\033[1;37;40m")
            endInput = input("Enter coordinates of the other end of the ship (ex. A2): ")
            if len(endInput) > 2:
                raise Exception()

            endInput = endInput.upper()
            endR = rowConvert(endInput[0])
            endC = int(endInput[1])

            if playerBoard[endR][endC] > 0:         #already occupied
                raise Exception()
            clearScreen()
            printLine(0)
            print("                                   PREPARATION PHASE")
            printLine(1)
            shipBuilder(startR, startC, endR, endC)
            printLine(2)
        except:                                     #if an error is raised, it means that coord is invalid
            clearScreen()
            printLine(0)
            print("                                   PREPARATION PHASE")
            printLine(1)
            if noEndpoint:
                print(" • \033[1;31;40mThe coordinate you picked has no possible endpoints.\033[1;37;40m")
            else:
                print(" • \033[1;31;40mInvalid coordinate or coordinate already occupied.\033[1;37;40m")
            printLine(2)
        
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
    evalmode argument takes:
    0 = prints the ships left in the game interface
    1 = evaluates whether player or cpu lost
    2 = returns a list of ships left
    """
    ship1count = 0
    ship2count = 0
    ship3count = 0
    ship4count = 0
    ship5count = 0
    ship1exist = "\033[1;32;40m○\033[1;37;40m"
    ship2exist = "\033[1;32;40m◘\033[1;37;40m"
    ship3exist = "\033[1;32;40m◙\033[1;37;40m"
    ship4exist = "\033[1;32;40m■\033[1;37;40m"
    ship5exist = "\033[1;32;40m≡\033[1;37;40m"
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
        if ship1count == 0:                 #if no part of the ship are found, make color red
            ship1exist = "\033[0;31;40m○\033[1;37;40m"
        if ship2count == 0:
            ship2exist = "\033[0;31;40m◘\033[1;37;40m"
        if ship3count == 0:
            ship3exist = "\033[0;31;40m◙\033[1;37;40m"
        if ship4count == 0:
            ship4exist = "\033[0;31;40m■\033[1;37;40m"
        if ship5count == 0:
            ship5exist = "\033[0;31;40m≡\033[1;37;40m"
        print(f"Ships: {ship1exist} {ship2exist} {ship3exist} {ship4exist} {ship5exist}")

    elif evalmode == 1:                     #lose evaluator
        global cpuLose
        global playerLose
        global gamePhase
        if ship1count + ship2count + ship3count + ship4count + ship5count == 0 and board == cpuBoard and gamePhase == 1:
            cpuLose = True
        elif (ship1count + ship2count + ship3count + ship4count + ship5count) == 0 and board == playerBoard and gamePhase == 1:
            playerLose = True
    
    elif evalmode == 2:                     #ship counter
        shipLeftList = []
        if ship1count != 0:
            shipLeftList.append(1)
        if ship2count != 0:
            shipLeftList.append(2)
        if ship3count != 0:
            shipLeftList.append(3)
        if ship4count != 0:
            shipLeftList.append(4)
        if ship5count != 0:
            shipLeftList.append(5)

        return shipLeftList

def hitRateCalculate(bombs):
    """
    bombs argument takes the number of bombs deployed
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
def highScore(username, score, mode):
    """
    username argument takes the name that will be saved. If you just want to print scores, just put None
    score argument takes the score that will be saved. If you just want to print scores, just put None
    mode argument takes:
    0 = save a high score
    1 = print the high scores
    """
    try:                                                        #try if file exists
        highScore = open("highscore.txt", "r")
    except:
        highScore = open("highscore.txt", "w+")                 #create the file if it doesn't exist
        highScore.close()

        highScore = open("highscore.txt", "r")                  #reads the file and create a list
    
    highScoreList = highScore.read()
    highScoreList = highScoreList.split(", ")
    highScore.close()
    highScoreList.pop(-1)                                       #pop the empty element [''] at the end of the list

    highScoreDict = {}                                          #score:name pair will be stored here
    for i in range(len(highScoreList)):                         #fills up the dictionary
        if i%2 == 0:
            highScoreDict[highScoreList[i]] = highScoreList[i+1]
        
    if mode == 0:
        highScoreDict[score] = username

        highScore = open("highscore.txt", "w")                  #overwrites the file
        for k, v in highScoreDict.items():
            highScore.write(str(k) + ", ")
            highScore.write(str(v) + ", ")
        highScore.close()

    if mode == 1:
        printTitle()
        if len(highScoreDict) == 0:
            print("\033[1;31;40mNo scores yet.\033[1;37;40m Play a new game now!")
        else:
            print("\033[1;30;40m╔═════════════════\033[1;37;40mLEADERBOARDS\033[1;30;40m═════════════════╗\033[1;37;40m")
            highScoreCounter = 1
            for k in sorted(highScoreDict.keys()):
                print(f"  {highScoreCounter} : \033[1;36;40m{highScoreDict[k]}\033[1;37;40m")
                print(f"       BOMBS FIRED: {k}   HIT RATE: {round(17/int(k) * 100, 4)} %")
                highScoreCounter += 1
            highScore.close()
            print("\033[1;30;40m╚══════════════════════════════════════════════╝\033[1;37;40m")
        print()
        input("Press Enter to go back to main menu.")
        mainMenu()

def saveBoard():
    savefile = open("savefile.txt", "w+")
    for rowb in range(10):                                    #rowb and colb used to avoid confusion between row and col variables
        for colb in range(10):
            savefile.write(str(playerBoard[rowb][colb]))      #index [0] to index [99]
            savefile.write(", ")
    for rowb in range(10):
        for colb in range(10):
            savefile.write(str(cpuBoard[rowb][colb]))         #index [100] to index [199]
            savefile.write(", ")

    savefile.write(str(turn) + ", ")                          #turn is the 201st value (index [200])
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
        clearScreen()                           #the code is repeated to paint the background
        printTitle()                            #it fixes the color bug in linux
        print(" [1] CONTINUE")
        print(" [2] NEW GAME")
        print(" [3] VIEW LEADERBOARDS")
        print(" [4] SEE IF MY AI IS SMART")
        print(" [0] QUIT")
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
            highScore(None, None, 1)
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
    printLine(0)
    print(f"                          Bombs fired: {bombs} | Hit rate: {hitRateCalculate(bombs)} %")
    if turn % 2 == 0:
        printLine(1)
        print(" • Your previous turns will appear here...")
        printLine(1)
        print(" • Computer's previous turns will appear here...")
        printLine(2)
    else:
        printLine(1)
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
            printLine(0)
            #because stats are printed before the move, bombs need to be bombs + 1
            print(f"                          Bombs fired: {bombs + 1} | Hit rate: {hitRateCalculate(bombs + 1)} %")
            printLine(1)

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
                        printLine(0)
                        #because stats are printed before the move, bombs need to be bombs + 1
                        #re-print the stats again after bombing a tile to make hit rate accurate
                        print(f"                          Bombs fired: {bombs + 1} | Hit rate: {hitRateCalculate(bombs + 1)} %")
                        printLine(1)

                        print(f" • You bombed \033[0;30;47m{turnInput}\033[1;37;40m. It's a \033[1;31;40mhit\033[1;37;40m!", end=" ")
                        cpuShipAfter = sinkShipChecker(cpuBoard, 2)             #count ships after bombing
                        if len(cpuShipAfter) < len(cpuShipBefore):              #a ship has been sunk
                            print("\033[1;32;40mYou sank your opponent's ", end="")
                            for ship in cpuShipBefore:
                                if ship not in cpuShipAfter:
                                    print(f"{shipDict[ship]}!\033[1;37;40m")
                        else:
                            print()
                        
                    elif cpuBoard[row][col] == 0:                               #if the target has no ship
                        print(f" • You bombed \033[0;30;47m{turnInput}\033[1;37;40m. It's a miss!")
                        cpuBoard[row][col] = -1                                 #target has been hit
                    turn += 1
                    bombs += 1
                else:
                    print(" • \033[1;31;40mNo need to bomb the same location twice!\033[1;37;40m")
                    printLine(1)
                    print(" • You can pick another coordinate to bomb.")
                    printLine(2)
            except:
                print(" • \033[1;31;40mInvalid coordinate\033[1;37;40m. Enter a coordinate from A0 to J9.")
                printLine(1)
                print(" • You can pick another coordinate to bomb.")
                printLine(2)

        elif turn % 2 == 1 and cpuLose == False and playerLose == False:        #cpu's turn
            cpuAI()
        elif playerLose:
            printCPUBoard()
            printPlayerBoard()
            print("\033[1;31;40mALL YOUR SHIPS HAVE SUNK! IT'S GAME OVER.\033[1;37;40m Let's play again!")
            os.remove("savefile.txt")                                               #deletes the save file
            break
        elif cpuLose:
            printLine(2)
            printCPUBoard()
            printPlayerBoard()
            print("\033[1;32;40mYOU WIN!\033[1;37;40m You took", bombs, "bombs to beat the computer!")
            while True:
                username = input("What is your name? ")
                if len(username) < 32 and ", " not in username:
                    break
                elif len(username) >= 32:
                    print("What a long name! \033[1;31;40mPlease enter a shorter one.\033[1;37;40m")
                elif ", " in username:
                    print("\033[1;31;40mPlease do not include ', ' in your name.\033[1;37;40m")
            if username == "":
                username = "Anonymous"
            highScore(username, bombs, 0)
            print(f"Thank you for playing, {username}. Your score has been saved!")
            os.remove("savefile.txt")                                               #deletes the save file
            break
    input("Press Enter to go back to main menu.")
    gamePhase = 0
    clearBoard()
    mainMenu()      

def continueGame():
    try:                                                                   #try if save file exists
        savefile = open("savefile.txt", "r")
        loading()
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

        mainGame()

    except:                                                                 #start new game prep phase if save file doesn't exists
        clearScreen()
        printLine(0)
        print("Save file not found. A new game will be started.")
        printLine(2)
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
    printLine(0)
    print("                      All ships deployed. Preparations complete.")
    printLine(2)
    saveBoard()                                                             #auto save
    #-----PRE-BATTLE PHASE
    time.sleep(1)
    print("  The war has begun!")
    time.sleep(1)
    if turn % 2 == 0:
        print("\033[1;32;40m  You\033[1;37;40m will have the first move.")
    else:
        print("\033[1;31;40m  Computer\033[1;37;40m will have the first move.")
    time.sleep(1)
    input("  Press Enter to proceed to the battlefield!")
    clearScreen()
    resetVars()
    mainGame()

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
                printLine(1)
                if playerBoard[row][col] > 0:                               #target has a ship
                    print(f" • Computer bombed \033[0;30;47m{str(rowDict[row])}{str(col)}\033[1;37;40m. It's a \033[1;31;40mhit\033[1;37;40m!", end=" ")
                    playerShipBefore = sinkShipChecker(playerBoard, 2)      #count ships before bombing
                    playerBoard[row][col] = -2                              #ship was bombed
                    playerShipAfter = sinkShipChecker(playerBoard, 2)       #count ships after bombing
                    if playerShipAfter < playerShipBefore:                  #a ship has been sunk
                        print("\033[1;31;40mComputer sank your ", end="")
                        for ship in playerShipBefore:
                            if ship not in playerShipAfter:
                                print(f"{shipDict[ship]}!\033[1;37;40m")
                    else:
                        print()
                    stratMode = 1                                           #switch to target mode
                    rowHit = row                                            #save vars for target mode
                    colHit = col
                    targetDirection = 0

                elif playerBoard[row][col] == 0:                            #if the target has no ship
                    print(f" • Computer bombed \033[0;30;47m{str(rowDict[row])}{str(col)}\033[1;37;40m. It's a miss!")
                    playerBoard[row][col] = -1                              #sea was bombed
                
                turn += 1
                saveBoard()
                printLine(2)
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
                    printLine(1)
                    if playerBoard[rowHit][colHit] > 0:                         #target has a ship
                        print(f" • Computer bombed \033[0;30;47m{str(rowDict[rowHit])}{str(colHit)}\033[1;37;40m. It's a \033[1;31;40mhit\033[1;37;40m!", end=" ")
                        playerShipBefore = sinkShipChecker(playerBoard, 2)      #count ships before bombing
                        playerBoard[rowHit][colHit] = -2                        #ship was bombed
                        playerShipAfter = sinkShipChecker(playerBoard, 2)       #count ships after bombing
                        if len(playerShipAfter) < len(playerShipBefore):        #a ship has been sunk
                            print("\033[1;31;40mComputer sank your ", end="")
                            for ship in playerShipBefore:
                                if ship not in playerShipAfter:
                                    print(f"{shipDict[ship]}!\033[1;37;40m")
                        else:
                            print()

                    elif playerBoard[rowHit][colHit] == 0:                      #if the target has no ship
                        print(f" • Computer bombed \033[0;30;47m{str(rowDict[rowHit])}{str(colHit)}\033[1;37;40m. It's a miss!")
                        playerBoard[rowHit][colHit] = -1                        #sea was bombed

                        rowHit = row                                            #get the original coords
                        colHit = col
                        targetDirection += 1                                    #proceed to the next adjacent tile
                    turn += 1
                    saveBoard()
                    printLine(2)
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
                printLine(1)
                if playerBoard[row][col] > 0:                               #target has a ship
                    print(f" • Computer bombed \033[0;30;47m{str(rowDict[row])}{str(col)}\033[1;37;40m. It's a \033[1;31;40mhit\033[1;37;40m!", end=" ")
                    playerShipBefore = sinkShipChecker(playerBoard, 2)      #count ships before bombing
                    playerBoard[row][col] = -2                              #ship was bombed
                    playerShipAfter = sinkShipChecker(playerBoard, 2)       #count ships after bombing
                    if len(playerShipAfter) < len(playerShipBefore):        #a ship has been sunk
                        print("\033[1;31;40mComputer sank your ", end="")
                        for ship in playerShipBefore:
                            if ship not in playerShipAfter:
                                print(f"{shipDict[ship]}!\033[1;37;40m")
                    else:
                        print()

                    stratMode = 1                                           #switch to target mode
                    rowHit = row                                            #save vars for target mode
                    colHit = col
                    targetDirection = -1

                elif playerBoard[row][col] == 0:                            #if the target has no ship
                    print(" • Computer bombed \033[0;30;47m" + str(rowDict[row]) +  str(col) + "\033[1;37;40m. It's a miss!")
                    playerBoard[row][col] = -1                              #sea was bombed
                turn += 1
                saveBoard()
                printLine(2)
                

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
    
def printLine(position):
    """
    position argument takes:
    0 = top
    1 = middle
    2 = bottom
    """
    if position == 0:
        print("\033[1;30;40m╔═══════════════════════════════════════════════════════════════════════════════════════╗\033[1;37;40m")
    if position == 1:
        print("\033[1;30;40m╠═══════════════════════════════════════════════════════════════════════════════════════╣\033[1;37;40m")
    if position == 2:
        print("\033[1;30;40m╚═══════════════════════════════════════════════════════════════════════════════════════╝\033[1;37;40m")
    

def printTitle():
    print("\033[1;33;40m")
    print(" ██████╗  █████╗ ████████╗████████╗██╗     ███████╗███████╗██╗  ██╗██╗██████╗ ██╗ ○") 
    print(" ██╔══██╗██╔══██╗╚══██╔══╝╚══██╔══╝██║     ██╔════╝██╔════╝██║  ██║██║██╔══██╗██║ ◘")    
    print(" ██████╔╝███████║   ██║      ██║   ██║     █████╗  ███████╗███████║██║██████╔╝██║ ◙")  
    print(" ██╔══██╗██╔══██║   ██║      ██║   ██║     ██╔══╝  ╚════██║██╔══██║██║██╔═══╝ ╚═╝ ■")  
    print(" ██████╔╝██║  ██║   ██║      ██║   ███████╗███████╗███████║██║  ██║██║██║     ██╗ ≡")  
    print(" ╚═════╝ ╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝     ╚═╝ ♦")
    print("\033[1;37;40m")

def rowConvert(input):
    if isinstance(input, int):      #checks if input is an int, convert it to letter
        return rowDict[input]
    elif isinstance(input, str):    #checks if input is a letter, convert it to int
        output = [key for (key, value) in rowDict.items() if value == input]
        if len(output) == 1:        #output will only have a content if a letter between A-J was entered
            output = output[0]
            return output

#------------------------------------DECLARE VARIABLES-----------------------------------
def resetVars():
    #reset variables at the start of a new game
    global gamePhase
    global turn
    global playerLose
    global cpuLose
    global stratMode
    global targetDirection
    global rowHit
    global colHit
    global row
    global col
    global bombs
    global currentShip

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

#-----------------------------------VARIABLE DECLARATION----------------------------------

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

pause = input("bruh")
