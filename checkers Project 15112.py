#   Name: Noora Almohannadi
#   Course: 15112
#   Project: checkers game with AI (project)
#   AndrewID: nooram

##########    Project Description    ##########
#   the checkers board was taken from https://www.pinterest.com/pin/345792077637457088/
#   This project is a checkers game that has three mode to play: Two players, easy Ai, and hard Ai.
#   The game follows standard checkers rules including:
#   - Single and double jumps
#   - when a piece reaches the end of the board it becomes a king piece this is represented by a
#   yellow ring on the piece
#   - King pieces can move both forward and backward
#   - simple pieces can only move towards the opposing end of the board

#   For the easy AI mode the AI makes random moves. I used the random library for this.
#   For the hard mode the minmax algorithm is implemented at a depth of 3 to choose the best move.
#   To evaluate the score of the move in the minmax my evaluation function calculates the difference
#   between the red pieces and the blue pieces and adds it to the difference between the king pieces.
#   The difference between the kings pieces is multiplied by a factor of 1.5 to prioritize a move that
#   that would result in a king for the AI pieces. Such factor was chosen based on the analusis done in
#   this project:
#   http://studentnet.cs.manchester.ac.uk/resources/library/3rd-year-projects/2010/yiannis.charalambous-2.pdf

#   The code is divided to 4 classes: board, gameGraphics, game, pieceStat, and startMenu.
#   Board: has functions used to update board and to get information from the board (availableMoves).
#   The board is stored as a list of lists where the inner lists represent rows and each element is a tuple
#   with the color and state of the piece (king or normal)
#   gameGraphics: uses the board list to set and update the game screen displayed
#   game: has the game events loop and controls the game.It also has the Ai functions and minmax function.
#   pieceStat: has the information of piece (king or normal)
#   startMenu: sets the start menue screen and has the events loop for the start menu. It creates an instance of
#   game class based on the button clicked
###############################################

import pygame
import sys
import time
import random
pygame.init()

#   colors
black  = (  0,  0,  0)
white  = (255,255,255)
red    = (255,  0,  0)
yellow = (255,255,  0)
blue   = (  0,  0,255)  

#   picture imports
boardPic = pygame.image.load("boarda.png")


class setBoard:
    def __init__(self, currentGame):
        self.boardStat = self.startBoard()
        self.game = currentGame
        

#   returns a list of lists where the index of the element in outer list
#   is the column number and the index of element in inner list is row
#   number. The inner list would have the color of the square black or
#   white if a piece is in the square then color would be color of piece
    def startBoard(self):
        colorPos = [[None] * 8 for i in range(8)] # [[None]*8]*8

        for column in range(8):
                for row in range(8):
                        if (row % 2 == 0) and (column % 2 == 0):
                                colorPos[row][column] = (black, pieceStat(None))
                        elif (row % 2 != 0)  and (column % 2 != 0):
                                colorPos[row][column] = (black, pieceStat(None))
                        elif (row % 2 != 0) and (column % 2 == 0):
                                colorPos[row][column] = (white, pieceStat(None))
                        elif (row % 2 == 0) and (column % 2 != 0):
                                colorPos[row][column] = (white, pieceStat(None))
                                
        #   add start pieces
        newColorPos = self.startPieces(colorPos)
        return newColorPos
    
    
#   starting board list updates the list with colors of pieces at the start
#   of the game in indices corresponding to positions
    def startPieces(self,pos):
        for column in range(8):
                for row in range(0,3):
                        if pos[row][column][0] == black:
                                pos[row][column] = (red, pieceStat())

                for row in range(5,8):
                        if pos[row][column][0] == black:
                                pos[row][column] = (blue, pieceStat())
        return pos

# returns coords of surrounding squares
    def diagonalSquares(self, (column,row)):
        x1 = column + 1 #   right
        x2 = column - 1 #   left
        y1 = row + 1    #   down
        y2 = row - 1    #   up
        moves = [(x1,y2),(x2,y2),(x1,y1),(x2,y1)] # [upper right, upper left, down right, down left]
        return moves
        
#   given position of a piece (column, row) it would return all move both allowed and not allowed
    def allMoves(self, (column,row)):
        moves = []
        if self.boardStat[row][column][1].stat != None:
            
            if self.boardStat[row][column][1].stat != "king" and self.boardStat[row][column][0] == red:
                moves = [self.diagonalSquares((column,row))[2],self.diagonalSquares((column,row))[3]] #   [down right, down left]
                
            elif self.boardStat[row][column][1].stat != "king" and self.boardStat[row][column][0] == blue:
                moves = [self.diagonalSquares((column,row))[0],self.diagonalSquares((column,row))[1]] #   [upper right, upper left]
                
            # if king
            else:
                moves = self.diagonalSquares((column,row)) # [upper right, upper left, down right, down left]
                
        else:
            moves = []
        
        return moves

    #   eliminate positions that are not in the board and positions that are filled by current player and add
    #   positions that allow attacking of enemy  
    def availableMoves(self, (column,row), goOver):
        moves = self.allMoves((column,row))
        allowedMoves = []
        
        if goOver == False:
            for move in moves:
                if self.foundOnBoard(move):
                    if self.boardStat[move[1]][move[0]][1].stat == None: #  move[1] is row and move[0] is column
                        allowedMoves.append(move)
                        
                    elif self.game.Ai == True and self.game.AiTurn == True:
                        #   check for attack move
                        if self.boardStat[move[1]][move[0]][0] != red: 
                            newCoords = (2 * move[0] - column, 2 * move[1] - row) # coords of attack move (column,row)
                            if self.foundOnBoard(newCoords) and self.boardStat[newCoords[1]][newCoords[0]][1].stat == None:
                                allowedMoves.append(newCoords)
                                
                    #   check for attack move                      
                    elif self.boardStat[move[1]][move[0]][0] != self.game.playerColor:
                        newCoords = (2 * move[0] - column, 2 * move[1] - row) # coords of attack move (column,row)
                        if self.foundOnBoard(newCoords) and self.boardStat[newCoords[1]][newCoords[0]][1].stat == None:
                            allowedMoves.append(newCoords)
        else:
            for move in moves:
                if self.foundOnBoard(move):
                    if self.game.Ai == True and self.game.AiTurn == True:
                        if self.boardStat[move[1]][move[0]][0] != red and self.boardStat[move[1]][move[0]][1].stat != None:
                            newCoords = (2 * move[0] - column, 2 * move[1] - row) # (column,row)
                            if self.foundOnBoard(newCoords) and self.boardStat[newCoords[1]][newCoords[0]][1].stat == None:
                                allowedMoves.append(newCoords)
                            
                    elif self.boardStat[move[1]][move[0]][0] != self.game.playerColor and self.boardStat[move[1]][move[0]][1].stat != None:
                        newCoords = (2 * move[0] - column, 2 * move[1] - row) # (column,row)
                        if self.foundOnBoard(newCoords) and self.boardStat[newCoords[1]][newCoords[0]][1].stat == None:
                            allowedMoves.append(newCoords)
        
        return allowedMoves

    #   this function checks if a given position is found on the board coords is (column, row)
    def foundOnBoard(self, coords):
        if coords[0] < 0 or coords[0] > 7 or coords[1] < 0 or coords[1] > 7:
            return False
                                                                                 
        return True

    #   Given position of a piece it would update the board stat list and move the piece to the given position 
    def movePiece(self,pieceCoords, toCoords):
        #   pieceCoords and toCoords in the form (x,y) == (column,row):
        fromColor = self.boardStat[pieceCoords[1]][pieceCoords[0]][0]
        pieceStat = self.boardStat[pieceCoords[1]][pieceCoords[0]][1]
        self.boardStat[toCoords[1]][toCoords[0]] = (fromColor, pieceStat)
        self.removePiece(pieceCoords)
        self.makeKing(toCoords)

        
    # if row is 0 or 7 make piece king by updating boardStat
    def makeKing(self, coords):
        #   coords in form (x,y) == (column,row)
        if self.boardStat[coords[1]][coords[0]][1] != None:
            if (coords[1] == 0 and self.boardStat[coords[1]][coords[0]][0] == blue) or (coords[1] == 7 and self.boardStat[coords[1]][coords[0]][0] == red):
                self.boardStat[coords[1]][coords[0]] = (self.boardStat[coords[1]][coords[0]][0],pieceStat("king"))
                
    # updates board stat list to remove a piece at the given position               
    def removePiece(self, pieceCoords):
        self.boardStat[pieceCoords[1]][pieceCoords[0]] = (black, pieceStat(None))
        
class gameGraphics:
    def __init__(self,color, board, wnd, menu, game):
        self.wndSize = 504
        self.wnd = wnd
        self.title = "Checkers"
        self.squareSize = self.wndSize / 8
        self.pieceRad = self.squareSize / 4
        self.playerColor = color
        self.board = board
        self.initialWnd()
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.won = False
        self.menu = menu
        self.message = ""
        self.game = game

    #   displays an instruction message at the beginning of the game
    def startMessage(self):
        message = "Press E to go back to start menu. Have fun!"
        self.font = pygame.font.Font("Chalkduster.ttf", 17)
        self.surface = self.font.render(message,True, black)
        self.surfaceRect = self.surface.get_rect()
        self.surfaceRect.center = (self.wndSize / 2, self.wndSize / 2)
        pygame.draw.rect(self.wnd, yellow, ((self.wndSize / 2) - 225,(self.wndSize / 2) - 35 ,450,70))
        pygame.draw.rect(self.wnd,black, ((self.wndSize / 2) - 225,(self.wndSize / 2) - 35 ,450,70), 5)
        self.wnd.blit(self.surface, self.surfaceRect)
        
    #   sets up the initial board and pieces positions         
    def initialWnd(self):
        self.wnd.blit(boardPic, (0,0))
        self.startMessage()
        time.sleep(3)
        self.addPieces(self.board.boardStat)
        pygame.display.update()
        
    # updates the board displayed
    def updateWnd(self, board, availMoves, clickedPiece):
        self.wnd.blit(boardPic, (0,0))
        self.addPieces(self.board.boardStat) # draw pieces according to board stat lis
        self.indicatePossibleMoves(availMoves, clickedPiece) #  if a piece is clicked it would draw a yellow circle at possible move
        #   displays a win message if a player won
        if self.won:
            self.winMessage(self.message)
            pygame.display.update()
            time.sleep(2)
            self.game.done = True 
        pygame.display.update()
        self.clock.tick(self.fps)
        
    #   draws the pieces
    def addPieces(self,board):
        for column in range(8):
            for row in range(8):
                if (board[row][column][0] == red) or (board[row][column][0] == blue): #board[row][column][0] != white or board[row][column][0] != black:
                    pygame.draw.circle(self.wnd, board[row][column][0], self.pieceCoords((column,row), self.pieceRad),self.pieceRad)
                    if board[row][column][1].stat == "king":
                        self.drawCrown((column,row))
                                 

    #   draws yellow circle in squares that are possible moves for a selected piece
    def indicatePossibleMoves(self, movesPos, selected):
        for pos in movesPos:
            pygame.draw.circle(self.wnd, yellow,self.pieceCoords((pos[0], pos[1]), 5), 5)

    #   draws a yellow ring on a piece to represent a king piece
    def drawCrown(self, coords):
        pygame.draw.circle(self.wnd, yellow, self.pieceCoords((coords[0],coords[1]),self.pieceRad),10,5) 
        return
    
    #   claculate coordinates of the piece based on square coordinates
    def pieceCoords(self, squareCoords, radius ):
        x = squareCoords[0] * self.squareSize + 2 * radius
        y = squareCoords[1] * self.squareSize + 2 * radius
        return (x,y)
    
    #   draw a rectangle and add text for win message
    def winMessage(self, message):
        self.message = message
        self.won = True
        self.font = pygame.font.Font("Chalkduster.ttf", 30)
        self.surface = self.font.render(message,True, black)
        self.surfaceRect = self.surface.get_rect()
        self.surfaceRect.center = (self.wndSize / 2, self.wndSize / 2)
        pygame.draw.rect(self.wnd, yellow, ((self.wndSize / 2) - 100,(self.wndSize / 2) - 35 ,200,70))
        pygame.draw.rect(self.wnd,black, ((self.wndSize / 2) - 100,(self.wndSize / 2) - 35 ,200,70), 5)
        self.wnd.blit(self.surface, self.surfaceRect) 
        
        
class game:
    def __init__(self, menu, wnd, Ai = False, difficulty = 0):
        self.playerColor = blue
        self.board = setBoard(self)
        self.allowedMoves = []
        self.clicked = None
        self.goOver = False
        self.done = False
        self.menu = menu
        self.Ai = Ai
        self.AiTurn = False
        self.wnd = gameGraphics(self.playerColor, self.board, wnd, self.menu, self) #######
        self.AiMode= difficulty
        
        
    #   This is the game loop the function detects mouse click or quit and calls other functionc accordingly
    def gameEvents(self):
        self.mousePos = pygame.mouse.get_pos()
        #   self.simpleMouse is the position of the moues in terms of simple coordinates of squares eg(0,1),(4,5)
        self.simpleMousePos = (self.mousePos[0] / self.wnd.squareSize, self.mousePos[1] / self.wnd.squareSize)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
                self.menu.exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.done = True               
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.goOver == False:
                    #   check if the clicked square has one of the players pieces
                    #   if it does then assign self.clicked to that mouse position
                    if ((self.board.boardStat[self.simpleMousePos[1]][self.simpleMousePos[0]][1] != None) and
                        (self.board.boardStat[self.simpleMousePos[1]][self.simpleMousePos[0]][0] == self.playerColor) and
                        (self.Ai == False or self.AiTurn == False)):
                        self.clicked = self.simpleMousePos
                    #   check if there is already a clicked piece and if the new clicked mouse positions is an available move for that piece
                    elif self.clicked != None and self.simpleMousePos in self.board.availableMoves(self.clicked, self.goOver):
                        self.board.movePiece(self.clicked,self.simpleMousePos)
                        #   check if an attack move was made
                        if self.simpleMousePos not in self.board.diagonalSquares(self.clicked):
                            x = self.clicked[0] + (self.simpleMousePos[0] - self.clicked[0]) / 2
                            y = self.clicked[1] + (self.simpleMousePos[1] - self.clicked[1]) / 2
                            self.board.removePiece((x,y))
                            self.goOver = True
                            self.clicked = self.simpleMousePos
                        else:
                            if self.Ai == True:
                                self.resetAi()
                            else:
                                self.reset()
                #   if self.goOver == True (an attack move was made)
                else:
                    availMoves = self.board.availableMoves(self.clicked, self.goOver)
                    if self.clicked != None and (self.simpleMousePos in availMoves):
                        #   check if a second attack move is available (double jump)
                        if self.simpleMousePos not in self.board.diagonalSquares(self.clicked):
                            self.board.movePiece(self.clicked, self.simpleMousePos)
                            x = self.clicked[0] + (self.simpleMousePos[0] - self.clicked[0]) / 2
                            y = self.clicked[1] + (self.simpleMousePos[1] - self.clicked[1]) / 2
                            self.board.removePiece((x,y))
                            self.goOver = False
                            if self.Ai == True:
                                self.resetAi()
                            else:
                                self.reset()
                                
                    else:
                        if self.Ai == True:
                            self.resetAi()
                        else:
                            self.reset()
            #   check if a piece is clicked and it is the player's piece it would assign available moves to
            #   self.allowedMoves so that a yellow circle would be drawn to represent available move
            elif self.clicked != None and (self.Ai == False or self.AiTurn == False):
                self.allowedMoves = self.board.availableMoves(self.clicked, self.goOver)
            
            #   easy Ai turn                
            elif self.AiTurn == True and self.AiMode == 0:
                self.AiMove()
                
            #   hard Ai turn
            elif self.AiTurn == True and self.AiMode == 1:
                self.hardAi()

    #   sets up the board and runs the game events loop until a player quits (when self.done == True)
    def runGame(self):
        self.wnd.initialWnd()

        while not self.done:
            self.gameEvents()
            self.updateGameDisplay()
        self.menu.quit = True

    #   uses function in gameGraphics class to update the scree
    def updateGameDisplay(self):
        self.wnd.updateWnd(self.board, self.allowedMoves, self.clicked)
        
    
            
    #   checks if one of the players won (run out of moves or pieces)
    def checkSomeoneWon(self): 
        for column in range(8):
            for row in range(8):
                if self.AiTurn == False and self.board.boardStat[row][column][0] == self.playerColor:
                    if self.board.availableMoves((column, row), self.goOver) != []:
                        return False
                if self.Ai == True and self.AiTurn == True:
                    if self.board.boardStat[row][column][0] == red:
                        if self.board.availableMoves((column, row), self.goOver) != []:
                            return False
                                           
        return True

    #   returns if the given player has won or not to specifically determine which player won in Ai mode
    def whoWon(self, player):
        if player == "Ai":
            for column in range(8):
                for row in range(8):
                    if self.board.boardStat[row][column][0] == blue:
                        if self.board.availableMoves((column, row), self.goOver) != []:
                            return False
            return True
        
        elif player == "human":
            for column in range(8):
                for row in range(8):
                    if self.board.boardStat[row][column][0] == red:
                        if self.board.availableMoves((column, row), self.goOver) != []:
                            return False
            return True
            

        
    #   loops through board stat list in board class and returns a dictionary with the key as the Ai piece
    #   and the value is list of avialble moves (moves and piece are in the form (column,row)
    def getAiPieces(self):
        pieces = dict()
        for column in range(8):
            for row in range(8):
                if self.board.boardStat[row][column][0] == red:
                    pieces[(column,row)] = []
        return pieces

    #   loops through board stat list in board class and returns a dictionary with the key as the human player
    #   piece and the value is list of avialble moves (moves and piece are in the form (column,row)
    def getPlayerPieces(self):
        pieces = dict()
        for column in range(8):
            for row in range(8):
                if self.board.boardStat[row][column][0] == blue:
                    pieces[(column,row)] = []
        return pieces

    #   loops through a dictionary of pieces and available moves and returns a dictionary with only the pieces
    #   that have availble moves (removes pieces that cannot move)   
    def getAiAvailMoves(self,pieces):
        updated = dict()
        for pieceCoords in pieces:
            availMoves = self.board.availableMoves(pieceCoords, self.goOver)
            if availMoves != []:
                updated[pieceCoords] = availMoves
        return updated

        
    # Ai that makes a random move for the easy Ai mode
    def AiMove(self):
        #   a dictionary with pieces and available move
        AiPieces = self.getAiPieces()
        #   an updated dictionary with only pieces that have available moves
        updateAiPieces = self.getAiAvailMoves(AiPieces) 
        piecesPos = updateAiPieces.keys()
        #   check if there are pieces with available moves
        if piecesPos != []:
            #   choose a random piece
            pieceIndex = random.randint(0,len(piecesPos) - 1) 
            pieceCoords = piecesPos[pieceIndex]
            
            #   choose a random move for that piece
            moves = updateAiPieces[pieceCoords]
            whichMove = random.randint(0, len(moves) - 1)
            move = moves[whichMove]
            
            if self.goOver == False:
                self.board.movePiece(pieceCoords, move)
                #   check if an attack move was made
                if move not in self.board.diagonalSquares(pieceCoords):
                    x = pieceCoords[0] + (move[0] - pieceCoords[0]) / 2
                    y = pieceCoords[1] + (move[1] - pieceCoords[1]) / 2
                    self.board.removePiece((x,y))
                    self.updateGameDisplay()
                    self.goOver = True
                    pieceCoords = move
                    
                else:
                    self.resetAi()
                    
             #  after an attack move checks for another possible attack move                   
            if self.goOver == True:
                AiPieces = self.getAiPieces()
                moves = AiPieces[pieceCoords]
                if moves != []:
                    whichMove = random.randint(0, len(moves) - 1)
                    move = moves[whichMove]
                    if move not in self.board.diagonalSquares(pieceCoords):
                        self.board.movePiece(pieceCoords, move)
                        x = pieceCoords[0] + (move[0] - pieceCoords[0]) / 2
                        y = pieceCoords[1] + (move[1] - pieceCoords[1]) / 2
                        self.board.removePiece((x,y))
                        self.goOver = False
                        self.resetAi()
                                                   
                else:
                    self.resetAi()
   
    #   moves an Ai piece by updating board stat list in board class
    def move(self,fromCoords, toCoords):
        self.board.movePiece(fromCoords, toCoords)
        if toCoords not in self.board.diagonalSquares(fromCoords):
            x = fromCoords[0] + (toCoords[0] - fromCoords[0]) / 2
            y = fromCoords[1] + (toCoords[1] - fromCoords[1]) / 2
            self.board.removePiece((x,y))
    #   undos a move by updating boards stat list in board class (for minmax function)       
    def undoMove(self,fromPos,fromStat,toPos, enemyRemoved):
        row = fromPos[1]
        column = fromPos[0]
        
        self.board.boardStat[row][column] = (fromStat[0], fromStat[1])
        self.board.removePiece(toPos)

        #   returns an enemy piece to the list if it has been removed
        if enemyRemoved != None:
            self.board.boardStat[enemyRemoved[1]][enemyRemoved[0]] = (enemyRemoved[2],enemyRemoved[3])
     
            
    #   checks if a given move from (fromCoords) to (toCoords) is an attack move (for minmax function)          
    def ifJump(self,fromCoords, toCoords):
        if toCoords not in self.board.diagonalSquares(fromCoords):
            x = fromCoords[0] + (toCoords[0] - fromCoords[0]) / 2
            y = fromCoords[1] + (toCoords[1] - fromCoords[1]) / 2
            removedColor = self.board.boardStat[y][x][0]
            removedStat = self.board.boardStat[y][x][1]
            return [x,y,removedColor, removedStat]
        
        return None
    
    #   scores the board (for minmax function)        
    def evaluate(self, color):
        redNum = 0
        blueNum = 0
        redKingsNum = 0
        blueKingsNum = 0
        for column in range(8):
            for row in range(8):
                if self.board.boardStat[row][column][0] == red:
                    if self.board.boardStat[row][column][1].stat == "king":
                        redKingsNum += 1
                    else:
                        redNum += 1
                if self.board.boardStat[row][column][0] == blue:
                    if self.board.boardStat[row][column][1].stat == "king":
                        blueKingsNum += 1
                    else:
                        blueNum += 1
        if color == blue:
            return (blueNum - redNum) + (1.5 * (blueKingsNum - redKingsNum))
        else:
            return (redNum - blueNum) + (1.5 * (redKingsNum - blueKingsNum))
        
    #   makes the move determined by the minmax function for the hard Ai mode           
    def hardAi(self):
        #   if minmax return a score of either 100 or -100 then the player can make a random move
        #   since it wouldn't matter (it already won or lost)
        if isinstance (self.minMax("Ai"), int):
            AiPieces = self.getAiPieces()
            updateAiPieces = self.getAiAvailMoves(AiPieces)
            pieces = updateAiPieces.keys()
            pieceIndex = random.randint(0,len(pieces)-1)
            piece = pieces[pieceIndex]
            moves = updateAiPieces[piece]
            whichMove = random.randint(0,len(moves)-1)
            move = moves[whichMove]
        #   gets a move from minmax
        else:
            move = self.minMax("Ai")[1]
            piece = self.minMax("Ai")[0]

    
        if self.goOver == False:
            self.board.movePiece(piece, move)
            #   checks if it is an attack move
            if move not in self.board.diagonalSquares(piece):
                x = piece[0] + (move[0] - piece[0]) / 2
                y = piece[1] + (move[1] - piece[1]) / 2
                self.board.removePiece((x,y))
                self.updateGameDisplay()
                self.goOver = True
                piece = move
            else:
                self.resetAi()
                
        #   if an attack move was already made
        if self.goOver == True:
            AiPieces = self.getAiPieces()
            moves = AiPieces[piece]
            for move in moves:
                if move not in self.board.diagonalSquares(piece):
                    self.board.movePiece(piece, move)
                    x = piece[0] + (move[0] - piece[0]) / 2
                    y = piece[1] + (move[1] - piece[1]) / 2
                    self.board.removePiece((x,y))
                    self.goOver = False
                    
            self.resetAi()
                
        
    #   uses minmax algorithm to a depth of 3 to determine the best move for the Ai              
    def minMax(self, player, depth=0):
        playerPieces = self.getPlayerPieces()
        AiPieces = self.getAiPieces()
        updateAiPieces = self.getAiAvailMoves(AiPieces)
        updatedPlayerPieces = self.getAiAvailMoves(playerPieces)
        
        # key is the piece and the value is a list of tuples (move,score)
        AiMoves = dict()
        playerMoves = dict()
        
        if self.whoWon("Ai"):
            return 100
            
        if self.whoWon("human"):
            return -100
            
        if depth == 3:
            if player =="Ai":
                return self.evaluate(red)
                
            else:
                return self.evaluate(red)
                
                
        if player == "Ai":
            for piece in updateAiPieces:
                movesInfo = []
                for move in updateAiPieces[piece]:
                    originalPos = piece
                    originalStat = [self.board.boardStat[piece[1]][piece[0]][0],self.board.boardStat[piece[1]][piece[0]][1]]
                    enemyPieceRemoved = self.ifJump(piece,move) #can be none or [x,y,removedColor, removedStat]
                    self.move(piece,move)
                    result = self.minMax("human", depth+1)
                    if isinstance(result, tuple):
                        moveInfo = (move,result[2])
                    else:
                        moveInfo = (move,result)
                
                    movesInfo.append(moveInfo)
                    self.undoMove(originalPos,originalStat, move, enemyPieceRemoved)
                
                AiMoves[piece] = movesInfo
        if player == "human":
            for piece in updatedPlayerPieces:
                movesInfo = []
                for move in updatedPlayerPieces[piece]:
                    originalPos = piece
                    originalStat = [self.board.boardStat[piece[1]][piece[0]][0],self.board.boardStat[piece[1]][piece[0]][1]]
                    enemyPieceRemoved = self.ifJump(piece,move) #can be none or [x,y,removedColor, removedStat]
                    self.move(piece,move)
                    result = self.minMax("Ai", depth+1)
                    if isinstance(result, tuple):
                        moveInfo = (move,result[2])
                    else:
                        moveInfo = (move,result)
                        
                    movesInfo.append(moveInfo)
                    self.undoMove(originalPos,originalStat, move, enemyPieceRemoved)
                    
                playerMoves[piece] = movesInfo
                
        bestMove = 0
        bestPiece = 0
        if player == "Ai":
            bestScore = -10000
            for piece in AiMoves:
                for move in AiMoves[piece]:
                    if move[1] > bestScore:
                        bestScore = move[1]
                        bestMove = move[0]
                        bestPiece = piece
                        
        #   if player is human player
        else:
            bestScore = 10000
            for piece in playerMoves:
                for move in playerMoves[piece]:
                    if move[1] < bestScore:
                        bestScore = move[1]
                        bestMove = move[0]
                        bestPiece = piece
        return (bestPiece, bestMove, bestScore)

    #   resets game in Ai modes and checks if someone won
    def resetAi(self):
        if self.AiTurn == False:
            self.AiTurn = True
        else:
            self.AiTurn = False
        self.goOver = False
        self.clicked = None
        self.allowedMoves = []
        if self.checkSomeoneWon():
            if self.AiTurn == True:
                self.wnd.winMessage("Blue Won!")
            else:
                self.wnd.winMessage("Red Won!")

    #   resets game for two players mode and checks if someone won using another function 
    def reset(self):
        
        if self.playerColor == blue:
            self.playerColor = red
        else:
            self.playerColor = blue
        self.goOver = False
        self.clicked = None
        self.allowedMoves = []
        if self.checkSomeoneWon():
            if self.playerColor == red:
                self.wnd.winMessage("Blue Won!")
            else:
                self.wnd.winMessage("Red Won!")
                       
class pieceStat:
    def __init__(self, stat = "normal"):
        self.stat = stat
            
            
class startMenu:
    def __init__(self):
        self.startWndSize = 504
        self.startWnd = pygame.display.set_mode((self.startWndSize,self.startWndSize))
        self.title = "Checkers"
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.quit = False
        self.exit = False

    #   set up initial window       
    def setWnd(self):
        self.startWnd.fill((200,200,200))
        pygame.display.set_caption(self.title)
        self.drawTitle((self.startWndSize /2 ,self.startWndSize /4))
        self.drawButtons((152,200), white)
        pygame.display.update()
        self.clock.tick(self.fps)
        
    #   writes and positions the title 
    def drawTitle(self, (x,y)):
        font = pygame.font.Font("Chalkduster.ttf",80)
        textDisplay = font.render("Checkers", True, red)
        textRect = textDisplay.get_rect()
        textRect.center = (x, y)
        self.startWnd.blit(textDisplay, textRect)
        
    #   adds buttons to the star menu by drawing rectangles
    def drawButtons(self, (x,y), color):
        pygame.draw.rect(self.startWnd, color, (x,y,200,50))
        pygame.draw.rect(self.startWnd, color, (x,y + 75,200,50))
        pygame.draw.rect(self.startWnd, color, (x,y + 150,200,50))
        self.addButtonText((x,y), 200,50)
        
    #   adds text to each button (two players, easy, hard)
    def addButtonText(self, (x,y), width, height, btn = "all"):
        if btn == 1 or btn == "all":
            font = pygame.font.Font("Chalkduster.ttf", 20)
            firstBtn = font.render("Two players", True, black)
            firstRect = firstBtn.get_rect()
            firstRect.center = (x + (width/2), y + (height/2))
            self.startWnd.blit(firstBtn, firstRect)
            
        if btn == 2 or btn == "all":
            font = pygame.font.Font("Chalkduster.ttf", 20)
            secBtn = font.render("Easy", True, black)
            secRect = secBtn.get_rect()
            secRect.center = (x + (width/2), y + 75 + (height/2))
            self.startWnd.blit(secBtn, secRect)
            
        if btn == 3 or btn == "all":
            font = pygame.font.Font("Chalkduster.ttf", 20)
            thirdBtn = font.render("Hard", True, black)
            thirdRect = thirdBtn.get_rect()
            thirdRect.center = (x + (width/2), y + 150 + (height/2))
            self.startWnd.blit(thirdBtn, thirdRect)

    #   given a mouse position, x and y coordinates of the top left corner of the first button, and the button
    #   parameters it would return the button on which button the mouse is. return 0 mouse is not
    #   on any of the buttons
    def whichBtn(self, mouse, (x,y), width, height):
        btn = 0
        xPos = mouse[0]
        yPos = mouse[1]
        if x + width > xPos > x and y + height > yPos > y:
            btn = 1
        elif x + width > xPos > x and y + height + 75 > yPos > y + 75:
            btn = 2
        elif x + width > xPos > x and y + height + 150 > yPos > y + 150:
            btn = 3
        return btn
        
    #   if mouse is on one of the buttons the function would change the button color to yellow
    def redrawButton(self, mouse, (x,y), width, height):
        xPos = mouse[0]
        yPos = mouse[1]
        btn = self.whichBtn(mouse, (x,y), width, height) #  the button on which the mouse is
        
        if btn == 1:
            pygame.draw.rect(self.startWnd, yellow, (x,y,200,50))
            self.addButtonText((x,y), width, height,1)
        elif btn == 2:
            pygame.draw.rect(self.startWnd, yellow, (x,y + 75,200,50))
            self.addButtonText((x,y), width, height,2)
        elif btn == 3:
            pygame.draw.rect(self.startWnd, yellow, (x,y + 150,200,50))
            self.addButtonText((x,y), width, height,3)
        else:
            self.drawButtons((152,200), white)
        
    #   events loop that controls the start menu
    def Main(self):
        mousePos = pygame.mouse.get_pos()
        self.redrawButton(mousePos, (152,200), 200, 50)
        
        for event in pygame.event.get():
            #   quits
            if event.type == pygame.QUIT:
                self.exit = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                #   checks if first button is clicked if it is then it would create an instance of
                #   game class with Ai = False (default) and calls runGame function to start
                #   the game
                if self.whichBtn(mousePos, (150,200), 200,50) == 1:
                    g = game(self, self.startWnd)
                    g.runGame()
                #   checks if second button is clicked if it is then it would create an instance of
                #   game class with Ai = True and difficulty = 0 (default) for easy mode and calls
                #   runGame function to start the game
                elif self.whichBtn(mousePos, (150,200), 200,50) == 2:
                    g = game(self, self.startWnd, True)
                    g.runGame()
                    
                #   checks if second button is clicked if it is then it would create an instance of
                #   game class with Ai = True and difficulty = 1 (hard mode) calls runGame function to
                #   start the game
                elif self.whichBtn(mousePos, (150,200), 200,50) == 3:
                    g = game(self, self.startWnd, True, 1)
                    g.runGame()
                    
    # sets up window as long as self. exit is false and runs Main() as long as self.quit is false.                
    def runMain(self):
        while not self.exit:
            self.setWnd()
            self.quit = False
            while not self.quit and not self.exit:
                self.Main()
                pygame.display.update()
        self.quitWnd()
        
    def quitWnd(self):
        pygame.quit()
        sys.exit

        
s = startMenu() 
s.runMain() 

            






            
        
        
            
        
        




