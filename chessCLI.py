#To Do
#Add ability to keep track of turn
#Add ability to save game
#Add piece tally
#Add ALL RULES


import string
from copy import deepcopy

class boardState:
    #Class that decribes the current state of the board
    def __init__(self):
        #Set variables for new game
        self.state = [["♖","♘","♗","♕","♔","♗","♘","♖"],["♙","♙","♙","♙","♙","♙","♙","♙"],["","","","","","","",""],["","","","","","","",""],["","","","","","","",""],["","","","","","","",""],["♟","♟","♟","♟","♟","♟","♟","♟"],["♜","♞","♝","♛","♚","♝","♞","♜"],]
        self.player = "White" #Should be white, changed for testing
        self.turn = 1
        self.kingMoved = [False,False] # [White, Black]

    def getState(self):
        #"Public" method, returns board state
        return self.state

    def locTosq(self, loc):
        #Converts a matrix address to a unicode peice or "" if square empty
        return self.state[loc[0]][loc[1]]

    def inCheck(self, stateToTest, player):
        #UNFINISHED
        return False

    def checkDiagonal(self, move):
        #THIS IS BUGGED!
        #Fuckered
        #Validates Diagonal Moves
        if move[1][0]-move[0][0] == move[1][1]-move[0][1]:
            for i in range(move[0][0]+1,move[1][0]): # must start from +1 and end -1
                for j in range(move[0][1]+1,move[1][1]):
                    if self.locTosq([i,j])!="":
                        return False
                        #vertical
            return True
        return False

    def checkLinear(self, move):
        #Validates X/Y only moves
        #horizontal
        if move[0][1]-move[1][1] == 0:
            #print("Y")
            if move[0][0]-move[1][0] < 0:
                offset = 1
            elif move[0][0]-move[1][0] > 0:
                offset = -1
            for i in range(move[0][0]+offset,move[1][0],-1): # must start from +1 and end -1
                #print("I am in a loop")
                #print(i, self.locTosq([move[0][1],i]))
                if self.locTosq([i,move[0][1]])!="":
                    #print("Hard Fail")
                    return False
            #print("There")
            return True
        elif move[0][0]-move[1][0] == 0:
            #print("X")
            if move[0][1]-move[1][1] < 0:
                offset = 1
            elif move[0][1]-move[1][1] > 0:
                offset = -1
            for i in range(move[0][1]+offset,move[1][1],-1): # must start from +1 and end -1
                #print("I am in a loop")
                #print(i, self.locTosq([move[0][0],i]))
                if self.locTosq([move[0][0],i])!="":
                    #print("Hard Fail")
                    return False
            #print("There")
            return True
        #print("Soft Fail")
        return False

    def testMove(self, move):
            #Return hypothetical board position
            testState = deepcopy(self.state)
            testState[move[1][0]][move[1][1]] = self.locTosq(move[0])
            testState[move[0][0]][move[0][1]] = ""
            return testState

    def movePiece(self, move):
        if self.validateMove(move):
            print(self.locTosq(move[0]))
            self.state[move[1][0]][move[1][1]] = self.locTosq(move[0])
            self.state[move[0][0]][move[0][1]] = ""
            if self.player == "White":
            #    self.player = "Black"
                if self.locTosq(move[1]) == "♚":
                    self.kingMoved[0] = True
            elif self.player == "Black":
                self.player = "White"
                if self.locTosq(move[1]) == "♔":
                    self.kingMoved[1] = True
            return True
        else:
            return False
    def onBoard(self, loc):
        #Check if a location is actually on the board
        if loc[0] >= 0 and loc[0]<8 and loc[1] >= 0 and loc[1]<8:
            return True
        return False
    def validateMove(self, move):
        #Check if the given move is valid
        #Mostly Done just need to make sure orientation is correct
        #and add enpasante, Castling double and first move too pawn
        #add pawn trasformation
        if self.onBoard(move[1]) and move[0] != move[1]:
            if self.player=="Black":
                if self.locTosq(move[0])=="♙":
                    #Advance one square
                    if move[1][1] == move[0][1] and (move[0][0]+1 == move[1][0] or (move[0][0]+2 == move[1][0] and move[0][0]==1)) and self.locTosq(move[1])=="" and not self.inCheck(self.testMove(move), "Black"):
                        return True
                    #Take peice
                    if (move[1][1] == move[0][1]+1 or move[1][0] == move[0][0]-1) and move[0][0]+1 == move[1][0] and self.locTosq(move[1]) not in ["♖","♘","♗","♕","♔","♙","♚",""] and not self.inCheck(self.testMove(move), "Black"):
                        return True
                elif self.locTosq(move[0])=="♕":
                    #Linear
                    if self.checkLinear(move) and self.locTosq(move[1]) not in ["♖","♘","♗","♕","♔","♙","♚"] and not self.inCheck(self.testMove(move), "Black"):
                        return True
                    #Diagonal
                    elif self.checkDiagonal(move) and self.locTosq(move[1]) not in ["♖","♘","♗","♕","♔","♙","♚"] and not self.inCheck(self.testMove(move), "Black"):
                            return True
                elif self.locTosq(move[0])=="♔":
                    #horizontal move
                    if (move[1][0] == move[0][0]+1 or move[1][0] == move[0][0]-1) and self.locTosq(move[1]) not in ["♖","♘","♗","♕","♔","♙","♚"] and not self.inCheck(self.testMove(move), "Black"):
                        return True
                    #vertical move
                    if (move[1][1] == move[0][1]+1 or move[1][1] == move[0][1]-1) and self.locTosq(move[1]) not in ["♖","♘","♗","♕","♔","♙","♚"] and not self.inCheck(self.testMove(move), "Black"):
                        return True
                    #diagonal move
                    if (move[1][0] == move[0][0]+1 or move[1][0] == move[0][0]-1) and (move[1][1] == move[0][1]+1 or move[1][1] == move[0][1]-1) and self.locTosq(move[1]) not in ["♖","♘","♗","♕","♔","♙","♚"] and not self.inCheck(self.testMove(move), "Black"):
                        return True
                elif self.locTosq(move[0])=="♗":
                    if self.checkDiagonal(move) and self.locTosq(move[1]) not in ["♖","♘","♗","♕","♔","♙","♚"] and not self.inCheck(self.testMove(move), "Black"):
                        return True
                elif self.locTosq(move[0])=="♘" :
                    #Horizontal L
                    if (move[1][0] == move[0][0]+2 or move[1][0] == move[0][0]-2) and (move[1][1] == move[0][1]+1 or move[1][1] == move[0][1]-1) and self.locTosq(move[1]) not in ["♖","♘","♗","♕","♔","♙","♚"] and not self.inCheck(self.testMove(move), "Black"):
                        return True
                    #Vertical L
                    if (move[1][0] == move[0][0]+1 or move[1][0] == move[0][0]-1) and (move[1][1] == move[0][1]+2 or move[1][1] == move[0][1]-2) and self.locTosq(move[1]) not in ["♖","♘","♗","♕","♔","♙","♚"] and not self.inCheck(self.testMove(move), "Black"):
                        print(3)
                        return True
                elif self.locTosq(move[0])=="♖":
                    if self.checkLinear(move) and self.locTosq(move[1]) not in ["♖","♘","♗","♕","♔","♙","♚"] and not self.inCheck(self.testMove(move), "Black"):
                        return True
            elif self.player=="White":
                if self.locTosq(move[0])=="♟":
                    #Advance one square
                    if move[1][1] == move[0][1] and (move[0][0]-1 == move[1][0] or (move[0][0]-2 == move[1][0] and move[0][0]==6)) and self.locTosq(move[1])=="" and not self.inCheck(self.testMove(move), "White"):
                        return True
                    #Take peice
                    if (move[1][1] == move[0][1]+1 or move[1][1] == move[0][1]-1) and move[0][0]-1 == move[1][0] and self.locTosq(move[1]) not in ["♜","♞","♝","♛","♚","♟","♔",""] and not self.inCheck(self.testMove(move), "White"):
                        return True
                elif self.locTosq(move[0])=="♛":
                    #Linear
                    print("Checking Queen")
                    print(self.checkLinear(move))
                    if self.checkLinear(move) and self.locTosq(move[1]) not in ["♜","♞","♝","♛","♚","♟","♔"] and not self.inCheck(self.testMove(move), "White"):
                        return True
                    #Diagonal
                    elif self.checkDiagonal(move) and self.locTosq(move[1]) not in ["♜","♞","♝","♛","♚","♟","♔"] and not self.inCheck(self.testMove(move), "White"):
                            return True
                    print(self.checkDiagonal(move))
                elif self.locTosq(move[0])=="♚":
                    #horizontal move
                    if (move[1][0] == move[0][0]+1 or move[1][0] == move[0][0]-1) and self.locTosq(move[1]) not in ["♜","♞","♝","♛","♚","♟","♔"] and not self.inCheck(self.testMove(move), "White"):
                        return True
                    #vertical move
                    if (move[1][1] == move[0][1]+1 or move[1][1] == move[0][1]-1) and self.locTosq(move[1]) not in ["♜","♞","♝","♛","♚","♟","♔"] and not self.inCheck(self.testMove(move), "White"):
                        return True
                    #diagonal move
                    if (move[1][0] == move[0][0]+1 or move[1][0] == move[0][0]-1) and (move[1][1] == move[0][1]+1 or move[1][1] == move[0][1]-1) and self.locTosq(move[1]) not in ["♜","♞","♝","♛","♚","♟","♔"] and not self.inCheck(self.testMove(move), "White"):
                        return True
                elif self.locTosq(move[0])=="♝":
                    if self.checkDiagonal(move) and self.locTosq(move[1]) not in ["♜","♞","♝","♛","♚","♟","♔"] and not self.inCheck(self.testMove(move), "White"):
                        return True
                elif self.locTosq(move[0])=="♞":
                    #Horizontal L
                    if (move[1][0] == move[0][0]+2 or move[1][0] == move[0][0]-2) and (move[1][1] == move[0][1]+1 or move[1][1] == move[0][1]-1) and self.locTosq(move[1]) not in ["♜","♞","♝","♛","♚","♟","♔"] and not self.inCheck(self.testMove(move), "White"):
                        return True
                    #Vertical L
                    if (move[1][0] == move[0][0]+1 or move[1][0] == move[0][0]-1) and (move[1][1] == move[0][1]+2 or move[1][1] == move[0][1]-2) and self.locTosq(move[1]) not in ["♜","♞","♝","♛","♚","♟","♔"] and not self.inCheck(self.testMove(move), "White"):
                        return True
                elif self.locTosq(move[0])=="♜":
                    if self.checkLinear(move) and self.locTosq(move[1]) not in ["♜","♞","♝","♛","♚","♟","♔"] and not self.inCheck(self.testMove(move), "White"):
                        return True
        return False

class cli:
    def __init__(self):
        self.board = boardState()
        self.checkmate = False
        self.showBoard()
        return
    def showBoard(self):
        print("┏━━━━━━━━━━━━━━━┓")
        for i, row in enumerate(self.board.getState()):
            print("┃", end="")
            for j, square in enumerate(row):
                if j !=0:
                    print(" ", end="")
                if square == "":
                    if (i+j)%2 == 1:
                        print("□", end="")
                    else:
                        print("■", end="")
                else:
                    print(square, end="")
            print("┃")
        print("┗━━━━━━━━━━━━━━━┛")
        return
    def makeMove(self, rawMove):
        #validate input text (want to improve this somewhat)
        rawMove = rawMove.lower()
        if len(rawMove) != 5:
            print("Please enter move in form 'a1 b2'")
            return
        #attempt move
        result = self.board.movePiece(self.rawToMove(rawMove))
        if result == False:
            print("That is not a valid move")
        else:
            self.showBoard()
        return
    def rawToMove(self, rawMove):
        move = [[8-int(rawMove[1]), string.ascii_lowercase.index(rawMove[0])],[8-int(rawMove[4]), string.ascii_lowercase.index(rawMove[3])]]
        return move

interface = cli()
while interface.checkmate == False:
    interface.makeMove(input(interface.board.player+" to move: "))
#board = boardState()
#print(board.locTosq([1,1]))
#print(board.validateMove([[0,0],[0,1]]))
