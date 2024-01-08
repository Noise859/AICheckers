import copy
black = (0, 0, 0)
red = (255, 0, 0)

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
    
class minimax:
    def __init__(self, team):
        self.team = team
        
    def getMove(self, pieces, gameBoard):
        tPieces = []
        for piece in pieces:
            if piece.team == self.team:
                tPieces.append(piece)
        scoreTree = []
        moves = getAllMoves(tPieces, gameBoard)
        for pieceMoves in moves:
            for move in pieceMoves[0]:
                copyPieces = copy.deepcopy(pieces)
                pieces_dict = {piece.id: piece for piece in copyPieces}
                tGameBoard = board(copyPieces)
                jumped = executeMove(pieces_dict.get(pieceMoves[1]), move, tGameBoard, copyPieces)
                if jumped:
                    tGameBoard.turn = red if tGameBoard.turn == red else black
                else:
                    tGameBoard.turn = red if tGameBoard.turn == black else red
                
                nTPieces = []
                scoreTree.append([])
                for piece2 in copyPieces:
                    if piece2.team == tGameBoard.turn:
                        nTPieces.append(piece2)
                moves2 = getAllMoves(nTPieces, tGameBoard)
                for pieceMoves2 in moves2:
                    for move2 in pieceMoves2[0]:
                        copyPieces2 = copy.deepcopy(copyPieces)
                        pieces_dict2 = {piece.id: piece for piece in copyPieces2}
                        tGameBoard2 = board(copyPieces2)
                        jumped2 = executeMove(pieces_dict2.get(pieceMoves2[1]), move2, tGameBoard2, copyPieces2)
                        nRed, nBlack = checkScoreFromGameboardMap(tGameBoard2.map)
                        tscore = nRed - nBlack if self.team == red else nBlack-nRed
                        scoreTree[len(scoreTree)-1].append(tscore)
        
        try:
            min_values = [min(row) for row in scoreTree]
            max_of_min_values = max(min_values)
            index = min_values.index(max_of_min_values)
        except ValueError:
            for row in range(len(scoreTree)):
                if scoreTree[row] == []:
                    index = row
        
        moveIdx = 0
        for pieceMoves in moves:
            for move in pieceMoves[0]:
                if moveIdx == index:
                    return (pieceMoves[1], move)
                else: moveIdx += 1
        
        return (0, [])


def getAllMoves(pieces, gameBoard):
    moves = []
    for piece in pieces:
        tempMoves = piece.getPossibleMoves(gameBoard)
        if tempMoves is not None and tempMoves != []:
            moves.append([tempMoves, piece.id])

    return moves

def printGameFromBoard(gameBoard):
    print("\n")
    for x in range(8):
        for y in range(8):
            if gameBoard.map[x][y] == red:
                print(" R ", end='')
            elif gameBoard.map[x][y] == black:
                print(" B ", end='')
            else: print(" - ", end='')
        print("\n")
    print("\n")


def checkScoreFromGameboardMap(gameBoard):
    nRed = 0
    nBlack = 0
    for x in range(8):
        for y in range(8):
            if gameBoard[y][x] == red:
                nRed += 1
            elif gameBoard[y][x] == black:
                nBlack += 1
    
    return nRed, nBlack

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
            jumped = False
            piece.onStreak = False
            for np in pieces:
                np.selected = False
    else:
        for np in pieces:
            np.selected = False

    return jumped