black = (0, 0, 0)
red = (255, 0, 0)

class depthFirstSearch:
    def __init__(self, team):
        self.team = team
    
    def getMove(self, pieces, gameBoard):
        tPieces = []
        for piece in pieces:
            if piece.team == self.team:
                tPieces.append(piece)

        moves = getAllMoves(tPieces, gameBoard)
        pieces_dict = {piece.id: piece for piece in pieces}

        if self.team == black:
            for x in range(8):
                for y in range(8):
                    for piece in moves:
                        for move in piece[0]:
                            if ((x, y) == move and not pieces_dict.get(piece[1]).king) or ((7-x, 7-y) == move and pieces_dict.get(piece[1]).king):
                                return (piece[1], move)
        else: 
            for x in range(8):
                for y in range(8):
                    for piece in moves:
                        for move in piece[0]:
                            if ((7-x, 7-y) == move and not pieces_dict.get(piece[1]).king) or ((x, y) == move and pieces_dict.get(piece[1]).king):
                                return (piece[1], move)

        return (0, [])


def getAllMoves(pieces, gameBoard):
    moves = []
    for piece in pieces:
        tempMoves = piece.getPossibleMoves(gameBoard)
        if tempMoves is not None and tempMoves != []:
            moves.append([tempMoves, piece.id])

    return moves
        
