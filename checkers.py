import sys, pygame, time
from breadthfirst import *
from depthfirst import *
from minimax import *

pygame.init()
screenSize = (1200, 800)
screen = pygame.display.set_mode((screenSize))
clock = pygame.time.Clock()
gray = 90, 90, 90
black = 0, 0, 0
red = 255, 0, 0
green = 0, 255, 0
lightBoard = 219, 172, 105
darkBoard = 117, 84, 36
singlePlayer = True
AIa = False
AIb = False
font = pygame.font.Font(None, 32)
buttons = []
pieces = []

class Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=True):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False

        self.fillColors = {
            'normal': (117, 84, 36),
            'hover': (107, 74, 26),
            'pressed': (82, 49, 1),
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(buttonText, True, (255, 255, 255))

        buttons.append(self)

    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if self.onePress:
                    self.onclickFunction()
                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False
        
        self.buttonSurface.blit(self.buttonSurf, [
        self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
        self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2])
        
        screen.blit(self.buttonSurface, self.buttonRect)

class board:
    def __init__(self, pieces):
        self.gameOver = False
        self.turn = black
        self.map = self.drawMapFromPieces(pieces)

    def drawMapFromPieces(self, pieces):
        tempMap = [[" " for x in range(8)] for y in range(8)] 

        for piece in pieces:
            tempMap[piece.position[1]][piece.position[0]] = piece.team

        return tempMap
    
    def drawBoard(self):
        pygame.draw.rect(screen, black, (0,0,screenSize[1],screenSize[1]))
        for x in range(8):
            for y in range(8):
                if y % 2 == 0:
                    if x % 2 ==0: pygame.draw.rect(screen, darkBoard, (x*screenSize[1]/8,y*screenSize[1]/8,screenSize[1]/8,screenSize[1]/8))
                    else: pygame.draw.rect(screen, lightBoard, (x*screenSize[1]/8,y*screenSize[1]/8,screenSize[1]/8,screenSize[1]/8))
                else:
                    if x % 2 ==0: pygame.draw.rect(screen, lightBoard, (x*screenSize[1]/8,y*screenSize[1]/8,screenSize[1]/8,screenSize[1]/8))
                    else: pygame.draw.rect(screen, darkBoard, (x*screenSize[1]/8,y*screenSize[1]/8,screenSize[1]/8,screenSize[1]/8))

class boardPiece:
    def __init__(self, id, team, position, king=False):
        self.id = id
        self.team = team
        self.position = position
        self.selected = False
        self.king = king
        self.onStreak = False

    def move(self, newPos):
        self.position = newPos
    
    def getPossibleMoves(self, gameBoard):
        moves = []
        if self.onStreak:
            if self.team == black:
                if not self.king:
                    if self.position[0]-1 > -1 and self.position[1]+1 < 8:
                        if gameBoard.map[self.position[1]+1][self.position[0]-1] == red:
                            if self.position[0] - 2 > -1 and self.position[1]+2 < 8 and gameBoard.map[self.position[1]+2][self.position[0]-2] == " ":
                                moves.append((self.position[0]-2, self.position[1]+2))
                    if self.position[0]+1 < 8 and self.position[1]+1 < 8:
                        if gameBoard.map[self.position[1]+1][self.position[0]+1] == red:
                            if self.position[0] + 2 < 8 and self.position[1]+2 < 8 and gameBoard.map[self.position[1]+2][self.position[0]+2] == " ":
                                moves.append((self.position[0]+2, self.position[1]+2))
                else:
                    if self.position[0]-1 > -1 and self.position[1]-1 > -1:
                        if gameBoard.map[self.position[1]-1][self.position[0]-1] == red:
                            if self.position[0] - 2 > -1 and self.position[1]-2 > -1 and gameBoard.map[self.position[1]-2][self.position[0]-2] == " ":
                                moves.append((self.position[0]-2, self.position[1]-2))
                    if self.position[0]+1 < 8 and self.position[1]-1 > -1:
                        if gameBoard.map[self.position[1]-1][self.position[0]+1] == red:
                            if self.position[0] + 2 < 8 and self.position[1]-2 > -1 and gameBoard.map[self.position[1]-2][self.position[0]+2] == " ":
                                moves.append((self.position[0]+2, self.position[1]-2))
            else:
                if not self.king:
                    if self.position[0]-1 > -1 and self.position[1]-1 > -1:
                        if gameBoard.map[self.position[1]-1][self.position[0]-1] == black:
                            if self.position[0] - 2 > -1 and self.position[1]-2 > -1  and gameBoard.map[self.position[1]-2][self.position[0]-2] == " ":
                                moves.append((self.position[0]-2, self.position[1]-2))
                    if self.position[0]+1 < 8 and self.position[1]-1 > -1:
                        if gameBoard.map[self.position[1]-1][self.position[0]+1] == black:
                            if self.position[0] + 2 < 8 and self.position[1]-2 > -1 and gameBoard.map[self.position[1]-2][self.position[0]+2] == " ":
                                moves.append((self.position[0]+2, self.position[1]-2))
                else:
                    if self.position[0]-1 > -1 and self.position[1] + 1 < 8:
                        if gameBoard.map[self.position[1]+1][self.position[0]-1] == black:
                            if self.position[0] - 2 > -1 and self.position[1]+2 < 8  and gameBoard.map[self.position[1]+2][self.position[0]-2] == " ":
                                moves.append((self.position[0]-2, self.position[1]+2))
                    if self.position[0]+1 < 8 and self.position[1] + 1 < 8:
                        if gameBoard.map[self.position[1]-1][self.position[0]+1] == black:
                            if self.position[0] + 2 < 8 and self.position[1]+2 < 8 and gameBoard.map[self.position[1]+2][self.position[0]+2] == " ":
                                moves.append((self.position[0]+2, self.position[1]+2))
        else: 
            if self.team == black:
                if not self.king:
                    if self.position[0]-1 > -1 and self.position[1]+1 < 8:
                        if gameBoard.map[self.position[1]+1][self.position[0]-1] == " ":
                            moves.append((self.position[0]-1, self.position[1]+1))
                        elif gameBoard.map[self.position[1]+1][self.position[0]-1] == red:
                            if self.position[0] - 2 > -1 and self.position[1]+2 < 8 and gameBoard.map[self.position[1]+2][self.position[0]-2] == " ":
                                moves.append((self.position[0]-2, self.position[1]+2))
                    if self.position[0]+1 < 8 and self.position[1]+1 < 8:
                        if gameBoard.map[self.position[1]+1][self.position[0]+1] == " ":
                            moves.append((self.position[0]+1, self.position[1]+1))
                        elif gameBoard.map[self.position[1]+1][self.position[0]+1] == red:
                            if self.position[0] + 2 < 8 and self.position[1]+2 < 8 and gameBoard.map[self.position[1]+2][self.position[0]+2] == " ":
                                moves.append((self.position[0]+2, self.position[1]+2))
                else:
                    if self.position[0]-1 > -1 and self.position[1]-1 > -1:
                        if gameBoard.map[self.position[1]-1][self.position[0]-1] == " ":
                            moves.append((self.position[0]-1, self.position[1]-1))
                        elif gameBoard.map[self.position[1]-1][self.position[0]-1] == red:
                            if self.position[0] - 2 > -1 and self.position[1]-2 > -1 and gameBoard.map[self.position[1]-2][self.position[0]-2] == " ":
                                moves.append((self.position[0]-2, self.position[1]-2))
                    if self.position[0]+1 < 8 and self.position[1]-1 > -1:
                        if gameBoard.map[self.position[1]-1][self.position[0]+1] == " ":
                            moves.append((self.position[0]+1, self.position[1]-1))
                        elif gameBoard.map[self.position[1]-1][self.position[0]+1] == red:
                            if self.position[0] + 2 < 8 and self.position[1]-2 > -1 and gameBoard.map[self.position[1]-2][self.position[0]+2] == " ":
                                moves.append((self.position[0]+2, self.position[1]-2))
            else:
                if not self.king:
                    if self.position[0]-1 > -1 and self.position[1]-1 > -1:
                        if gameBoard.map[self.position[1]-1][self.position[0]-1] == " ":
                            moves.append((self.position[0]-1, self.position[1]-1))
                        elif gameBoard.map[self.position[1]-1][self.position[0]-1] == black:
                            if self.position[0] - 2 > -1 and self.position[1]-2 > -1  and gameBoard.map[self.position[1]-2][self.position[0]-2] == " ":
                                moves.append((self.position[0]-2, self.position[1]-2))
                    if self.position[0]+1 < 8 and self.position[1]-1 > -1:
                        if gameBoard.map[self.position[1]-1][self.position[0]+1] == " ":
                            moves.append((self.position[0]+1, self.position[1]-1))
                        elif gameBoard.map[self.position[1]-1][self.position[0]+1] == black:
                            if self.position[0] + 2 < 8 and self.position[1]-2 > -1 and gameBoard.map[self.position[1]-2][self.position[0]+2] == " ":
                                moves.append((self.position[0]+2, self.position[1]-2))
                else:
                    if self.position[0]-1 > -1 and self.position[1]+1 < 8:
                        if gameBoard.map[self.position[1]+1][self.position[0]-1] == " ":
                            moves.append((self.position[0]-1, self.position[1]+1))
                        elif gameBoard.map[self.position[1]+1][self.position[0]-1] == black:
                            if self.position[0] - 2 > -1 and self.position[1]+2 < 8  and gameBoard.map[self.position[1]+2][self.position[0]-2] == " ":
                                moves.append((self.position[0]-2, self.position[1]+2))
                    if self.position[0]+1 < 8 and self.position[1]+1 < 8:
                        if gameBoard.map[self.position[1]+1][self.position[0]+1] == " ":
                            moves.append((self.position[0]+1, self.position[1]+1))
                        elif gameBoard.map[self.position[1]+1][self.position[0]+1] == black:
                            if self.position[0] + 2 < 8 and self.position[1]+2 < 8 and gameBoard.map[self.position[1]+2][self.position[0]+2] == " ":
                                moves.append((self.position[0]+2, self.position[1]+2))
        return moves
                



def checkScore(pieces):
    nRed = 0
    nBlack = 0
    for piece in pieces:
        if piece.team == red: nRed += 1
        if piece.team == black: nBlack += 1
    
    return nRed, nBlack
        

def drawPieces(pieces, gameBoard):
    for piece in pieces:
        pygame.draw.circle(screen, piece.team, (screenSize[1]/8/2+screenSize[1]/8*piece.position[0], screenSize[1]/8/2+screenSize[1]/8*piece.position[1]), screenSize[1]/8/3)
        if piece.king:
            if piece.team == red:
                pygame.draw.circle(screen, black, (screenSize[1]/8/2+screenSize[1]/8*piece.position[0], screenSize[1]/8/2+screenSize[1]/8*piece.position[1]), screenSize[1]/64)
            else:
                pygame.draw.circle(screen, red, (screenSize[1]/8/2+screenSize[1]/8*piece.position[0], screenSize[1]/8/2+screenSize[1]/8*piece.position[1]), screenSize[1]/64)
        if piece.selected:
            moves = piece.getPossibleMoves(gameBoard)
            for move in moves:
                pygame.draw.circle(screen, green, (screenSize[1]/8/2+screenSize[1]/8*move[0], screenSize[1]/8/2+screenSize[1]/8*move[1]), screenSize[1]/8/6)
        

def handleClick(pos):
    column = int(pos[0] / (screenSize[1]/8))
    if column > 8-1: column = None
    row = int(pos[1] / ((screenSize[1]/8)))
    if row > 8-1: row = None
    return column, row

            
def getAllMoves(pieces, gameBoard):
    moves = []
    for piece in pieces:
        tempMoves = piece.getPossibleMoves(gameBoard)
        if tempMoves is not None and tempMoves != []:
            moves.append([tempMoves, piece.id])

    return moves

def executeMove(piece, newPos, gameBoard, pieces):
    x, y = newPos
    jumped = False

    if gameBoard.turn == red:
        if x - piece.position[0] > 1:
            for np in pieces:
                if (np.position == (x-1, y+1) and not piece.king) or (np.position == (x-1, y-1) and piece.king):
                    pieces.remove(np)
                    jumped = True
                    piece.onStreak = True
        elif x - piece.position[0] < -1:
            for np in pieces:
                if (np.position == (x+1, y+1) and not piece.king) or (np.position == (x+1, y-1) and piece.king):
                    pieces.remove(np)
                    jumped = True
                    piece.onStreak = True
        else: 
            gameBoard.turn = black
        
    else: 
        if x - piece.position[0] > 1:
            for np in pieces:
                if (np.position == (x-1, y-1) and not piece.king) or (np.position == (x-1, y+1) and piece.king):
                    pieces.remove(np)
                    jumped = True
                    piece.onStreak = True
        elif x - piece.position[0] < -1:
            for np in pieces:
                if (np.position == (x+1, y-1) and not piece.king) or (np.position == (x+1, y+1) and piece.king):
                    pieces.remove(np)
                    jumped = True
                    piece.onStreak = True
        else: 
            gameBoard.turn = red

        gameBoard.map[y][x] = black
        
    piece.move((x, y))
    gameBoard.map = gameBoard.drawMapFromPieces(pieces)

    if piece.team == red:
        if piece.position[1] == 0:
            piece.king = True
        elif piece.position[1] == 7 and piece.king == True:
            piece.king = False
    else: 
        if piece.position[1] == 7:
            piece.king = True
        elif piece.position[1] == 0 and piece.king == True:
            piece.king = False

    if jumped:
        if len(piece.getPossibleMoves(gameBoard)) < 1:
            if gameBoard.turn == red: gameBoard.turn = black
            else: gameBoard.turn = red
            jumped = False
            piece.onStreak = False
            for np in pieces:
                np.selected = False
    else:
        for np in pieces:
            np.selected = False

    return jumped
    
def renderText(gameBoard, pieces, AIa, AIb):
    if gameBoard.gameOver:
        nRed, nBlack = checkScore(pieces)
        if nRed == 0:
            textRender = "Game over! Black wins!"
        elif nBlack == 0:
            textRender = "Game over! Red wins!"
    else:
        if gameBoard.turn == red:
            textRender = "Turn: Red"
        else:
            textRender = "Turn: Black"

    textRender2 = "No AI is active."

    if AIa is not None:
        if AIb is not None:
            textRender2 = "Two AI (Color: Black, Red) are active"
        else:
            textRender2 = "One AI (Color: Black) is active."
    

    text = font.render(textRender, True, (255,255,255))
    text2 = font.render(textRender2, True, (255,255,255))
    textRect = text.get_rect()
    textRect2 = text.get_rect()
    textRect.x, textRect.y = (screenSize[1] + 30, 30)
    textRect2.x, textRect2.y = (screenSize[1] + 30, 70)
    

    screen.blit(text,textRect)
    screen.blit(text2,textRect2)

    for button in buttons:
        button.process()

def endGame():
    sys.exit()

def mouseClicked(event, gameBoard, pieces, canSelect):
    x, y = handleClick(event.pos)
    for piece in pieces:
        if piece.position == (x,y):
            if piece.team == gameBoard.turn and canSelect:
                for np in pieces:
                    np.selected = False
                piece.selected = True
        elif piece.selected:
            for move in piece.getPossibleMoves(gameBoard):
                if (x, y) == move:
                    canSelect = not executeMove(piece, (x,y), gameBoard, pieces)

def gameLoop(pieces, players, draw, AIa=None, AIb=None):
    if AIa is not None:
        if AIa == "breadth-first":
            AIa = breadthFirstSearch(black)
        elif AIa == "depth-first":
            AIa = depthFirstSearch(black)
        elif AIa == "minimax":
            AIa = minimax(black)
        else:
            print("AIa provided is not valid")
            sys.exit()
    
    if AIb is not None:
        if AIb == "breadth-first":
            AIb = breadthFirstSearch(red)
        elif AIb == "depth-first":
            AIb = depthFirstSearch(red)
        elif AIb == "minimax":
            AIb = minimax(red)
        else:
            print("AIb provided is not valid")
            sys.exit()
    pieces.append(boardPiece(0, black, (0, 0)))
    pieces.append(boardPiece(1, black, (2, 0)))
    pieces.append(boardPiece(2, black, (4, 0)))
    pieces.append(boardPiece(3, black, (6, 0)))
    pieces.append(boardPiece(4, black, (1, 1)))
    pieces.append(boardPiece(5, black, (3, 1)))
    pieces.append(boardPiece(6, black, (5, 1)))
    pieces.append(boardPiece(7, black, (7, 1)))
    pieces.append(boardPiece(8, black, (0, 2)))
    pieces.append(boardPiece(9, black, (2, 2)))
    pieces.append(boardPiece(10, black, (4, 2)))
    pieces.append(boardPiece(11, black, (6, 2)))
    pieces.append(boardPiece(12, red, (1, 7)))
    pieces.append(boardPiece(13, red, (3, 7)))
    pieces.append(boardPiece(14, red, (5, 7)))
    pieces.append(boardPiece(15, red, (7, 7)))
    pieces.append(boardPiece(16, red, (0, 6)))
    pieces.append(boardPiece(17, red, (2, 6)))
    pieces.append(boardPiece(18, red, (4, 6)))
    pieces.append(boardPiece(19, red, (6, 6)))
    pieces.append(boardPiece(20, red, (1, 5)))
    pieces.append(boardPiece(21, red, (3, 5)))
    pieces.append(boardPiece(22, red, (5, 5)))
    pieces.append(boardPiece(23, red, (7, 5)))
    gameBoard = board(pieces)
    Button(screenSize[1] + 30, 110, 130, 50, 'End Game', endGame, True)
    canSelect = True
    running = True
    while running:
        lRed = []
        lBlack = []
        for piece in pieces:
            if piece.team == black:
                lBlack.append(piece)
            elif piece.team == red:
                lRed.append(piece)
        if getAllMoves(lRed, gameBoard) == [] or getAllMoves(lBlack, gameBoard) == []:
            nRed, nBlack = checkScore(pieces)
            if nRed > nBlack:
                return ("red", AIa.team, AIb.team)
            elif nRed < nBlack:
                return ("black", AIa.team, AIb.team)
            else: 
                return ("tie", AIa.team, AIb.team)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if players > 0:
                if event.type == pygame.MOUSEBUTTONDOWN and not gameBoard.gameOver:
                    if players == 1 and gameBoard.turn == red:
                        mouseClicked(event, gameBoard, pieces, canSelect)
                    elif players == 2:
                        mouseClicked(event, gameBoard, pieces, canSelect)
        if AIa is not None:
            if gameBoard.turn == AIa.team:
                idxPiece, tLocation = AIa.getMove(pieces, gameBoard)
                for piece in pieces:
                    if piece.id == idxPiece:
                        if tLocation != []:
                            executeMove(piece, tLocation, gameBoard, pieces)
        if AIb is not None:
            if gameBoard.turn == AIb.team:
                idxPiece, tLocation = AIb.getMove(pieces, gameBoard)
                for piece in pieces:
                    if piece.id == idxPiece:
                        if tLocation != []:
                            executeMove(piece, tLocation, gameBoard, pieces)
        if draw:
            screen.fill(gray)
            gameBoard.drawBoard()
            drawPieces(pieces, gameBoard)
            renderText(gameBoard, pieces, AIa, AIb)
            pygame.display.flip()
        
        nRed, nBlack = checkScore(pieces)
        if nRed < 1 or nBlack < 1:
            gameBoard.gameOver = True
            if nRed < 1: return ("black", AIa.team, AIb.team)
            else: return ("red", AIa.team, AIb.team)

        clock.tick(30)
