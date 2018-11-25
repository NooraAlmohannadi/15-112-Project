import pygame
import sys

#   colors
black  = (  0,  0,  0)
white  = (255,255,255)
red    = (255,  0,  0)
yellow = (255,255,  0)
blue   = (  0,  0,255)  

#   picture imports
boardPic = pygame.image.load("board1.jpg")

class setBoard:
    def __init__(self, color):
        self.boardStat = self.startBoard()
        self.playerColor = color
        



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
#   of the game in indexes corresponding to positions
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
        
        
    def allMoves(self, (column,row)):
        moves = []
        
        
        if self.boardStat[row][column][1] != None:
            
            if self.boardStat[row][column][1] != "king" and self.boardStat[row][column][0] == red:
                

                moves = [self.diagonalSquares((column,row))[2],self.diagonalSquares((column,row))[3]] #   [down right, down left]
                
                
            elif self.boardStat[row][column][1] != "king" and self.boardStat[row][column][0] == blue:
                


                moves = [self.diagonalSquares((column,row))[0],self.diagonalSquares((column,row))[1]] #   [upper right, upper left]
                
            # if king
            else:
                
                moves = self.diagonalSquares((column,row)) # [upper right, upper left, down right, down left]
                
        else:
            
            moves = []

        return moves

    #   eliminate positions that are not in the board and positions that are filled by current player and
    #   positions that allow attacking of enemy  
    def availableMoves(self, (column,row), goOver):
        moves = self.allMoves((column,row))
        
        
        allowedMoves = []
        if goOver == False:
            for move in moves:

                print "move to check",move
                if self.foundOnBoard(move):
                    #print "on board", move,self.boardStat[move[1]][move[0]][1].stat
                    if self.boardStat[move[1]][move[0]][1].stat == None:

                        allowedMoves.append(move)
                    elif self.boardStat[move[1]][move[0]][0] != self.playerColor:
                        newCoords = (2 * move[0] - column, 2 * move[1] - row) # (column,row)
                        if self.foundOnBoard(newCoords) and self.boardStat[newCoords[1]][0][1].stat == None:
                            allowedMoves.append(newCoords)
        else:
            for move in moves:
                if self.foundOnBoard(move):
                    if self.boardStat[move[1]][move[0]][0] != self.playerColor and self.boardStat[move[1]][move[0]][1].stat != None:
                        newCoords = (2 * move[0] - column, 2 * move[1] - row) # (column,row)
                        if self.foundOnBoard(newCoords) and self.boardStat[newCoords[1]][newCoords[0]][1].stat == None:
                            allowedMoves.append(newCoords)
        
        return allowedMoves

    def foundOnBoard(self, coords):
        if coords[0] < 0 or coords[0] > 7 or coords[1] < 0 or coords[1] > 7:
            return False
                                                                                 
        return True
    def movePiece(self,pieceCoords, toCoords):
        #   pieceCoords and toCoords in the form (x,y) == (column,row):
        print pieceCoords
        print toCoords
        # add a circle at to positions and update boardStat accordingly
        fromColor = self.boardStat[pieceCoords[1]][pieceCoords[0]][0]
        pieceStat = self.boardStat[pieceCoords[1]][pieceCoords[0]][1]
   
        self.boardStat[toCoords[1]][toCoords[0]] = (fromColor, pieceStat)
        print " moved", self.boardStat[toCoords[1]][toCoords[0]]
        print toCoords
        self.removePiece(pieceCoords)
        print self.boardStat[pieceCoords[1]][pieceCoords[0]]

        
    # if row is 0 or 7 make piece king by updating boardStat
    def makeKing(self, coords):
        #   coords in form (x,y) == (column,row)
        if self.boardStat[1][0][1] != None:
            if (coords[1] == 0 and self.boardStat[1][0][0] == blue) or (coords[1] == 7 and self.boardStat[1][0][0] == red):
                self.boardStat[1][0][1] == "king"
                
    def removePiece(self, pieceCoords):
        self.boardStat[pieceCoords[1]][pieceCoords[0]] = (black, pieceStat(None))
        
        
                
                
            
            

        
class gameGraphics:
    def __init__(self,color, board):
        self.wndSize = 500
        self.wnd = pygame.display.set_mode((self.wndSize,self.wndSize))
        self.title = "Checkers"
        self.squareSize = self.wndSize / 8
        self.pieceRad = self.squareSize / 4
        self.playerColor = color
        self.board = board
        self.initialWnd()
        self.fps = 60
        self.clock = pygame.time.Clock()

    def initialWnd(self):
        pygame.init()
        pygame.display.set_caption(self.title)
        self.wnd.blit(boardPic, (0,0))
        self.addPieces(self.board.boardStat)
        pygame.display.update()

    def updateWnd(self, board, availMoves, clickedPiece):
        self.wnd.blit(boardPic, (0,0))
        self.addPieces(self.board.boardStat) #setBoard.startBoard(setBoard())
        self.indicatePossibleMoves(availMoves, clickedPiece)
        pygame.display.update()
        self.clock.tick(self.fps)
        
    def addPieces(self,board):
        for column in range(8):
            for row in range(8):
                if (board[row][column][0] == red) or (board[row][column][0] == blue): #board[row][column][0] != white or board[row][column][0] != black:
                    pygame.draw.circle(self.wnd, board[row][column][0], self.pieceCoords((column,row), self.pieceRad),self.pieceRad)
                    if board[row][column][1] == "king":
                        drawCrown((column,row))
                                 

        
    def indicatePossibleMoves(self, movesPos, selected):
        for pos in movesPos:
            pygame.draw.circle(self.wnd, yellow,self.pieceCoords((pos[0], pos[1]), 20), 20)
            
    def drawCrown(self, coords):
        return

    def pieceCoords(self, squareCoords, radius ):
        print squareCoords
        x = squareCoords[0] * self.squareSize + (2 * radius)
        y = squareCoords[1] * self.squareSize + (2 * radius)
        return (x,y)
                  
class game:
    def __init__(self):
        self.playerColor = blue
        self.board = setBoard(self.playerColor)
        self.wnd = gameGraphics(self.playerColor, self.board)
        #self.player = playerDown #up or down based on position on board
        self.allowedMoves = []
        self.clicked = None
        self.goOver = False
        self.done = False
        
        
    def getPlayerColor(self):
        return self.playerColor
    def gameEvents(self):
        self.mousePos = pygame.mouse.get_pos()
        self.simpleMousePos = (self.mousePos[0] / self.wnd.squareSize, self.mousePos[1] / self.wnd.squareSize)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True 
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                print self.simpleMousePos
                print self.goOver
                if self.clicked != None:
                    print self.clicked
                    print self.board.availableMoves(self.clicked, self.goOver)
                if self.goOver == False:
                    if (self.board.boardStat[self.simpleMousePos[1]][self.simpleMousePos[0]][1] != None) and (self.board.boardStat[self.simpleMousePos[1]][self.simpleMousePos[0]][0] == self.playerColor):
                        self.clicked = self.simpleMousePos
                        #self.allowedMoves = self.board.availableMoves(self.clicked, self.goOver)
                        
                        
                    elif self.clicked != None and self.simpleMousePos in self.board.availableMoves(self.clicked, self.goOver):
                        print 1
                        self.board.movePiece(self.clicked,self.simpleMousePos)
                        if self.simpleMousePos not in self.board.diagonalSquares(self.clicked):
                            print 2
                            x = self.clicked[0] + (self.simpleMousePos[0] - self.clicked[0]) / 2
                            y = self.clicked[1] + (self.simpleMousePos[1] - self.clicked[1]) / 2
                            self.board.removePiece((x,y))
                            self.goOver = True
                            self.clicked = self.simpleMousePos
                        else:
                            print 3 
                            self.reset()
                else:
                    availMoves = self.board.availableMoves(self.clicked, self.goOver)
                    if self.clicked != None and (self.simpleMousePos in availMoves):
                        self.board.movePiece(self.clicked, self.simpleMousePos)
                        x = self.clicked[0] + (self.simpleMousePos[0] - self.clicked[0]) / 2
                        y = self.clicked[1] + (self.simpleMousePos[1] - self.clicked[1]) / 2
                        self.board.removePiece((x,y))
                    if self.board.availableMoves(self.simpleMousePos, self.goOver) == []:
                        self.reset()
                    else:
                        self.clicked = self.simpleMousePos
            elif self.clicked != None:
                self.allowedMoves = self.board.availableMoves(self.clicked, self.goOver)
                
                

                
            
        
 
                        
    def quiteGame(self):
        pygame.quit()
        sys.exit
        
    def runGame(self):
        self.wnd.initialWnd()

        while not self.done:
            self.gameEvents()
            self.updateGameDisplay()
        self.quiteGame()
            
    def updateGameDisplay(self):
        self.wnd.updateWnd(self.board, self.allowedMoves, self.clicked)
        
    
            
    #   run out of moves or pieces
    def checkSomeoneWon(self):
        for column in range(8):
            for row in range(8):
                if self.board.boardStat[row][column] == self.playerColor:
                    if self.board.availableMoves[row][column] != []:
                        return False
        return True
    def reset(self):
        if self.playerColor == blue:
            self.playerColor = red
        else:
            self.playerColor = blue
        self.goOver = False
        self.clicked = None
        self.allowedMoves = []
            
        
        
        
class pieceStat:
    def __init__(self, stat = "normal"):
        self.stat = stat
            
            
        
        

##g = gameGraphics()
#g.updateWnd()

g = game()
g.runGame()


            






            
        
        
            
        
        




