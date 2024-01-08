import sys
from checkers import *


players = 2
nGames = 1
draw = True
AIa = None
AIb = None
nArgs = 0

if len(sys.argv) > 1 :
    nArgs += 1
    try:
        players = 2 - int(sys.argv[1])
    except:
        pass

    if players < 2:
        AIa = sys.argv[2]
        nArgs += 1

    if players < 1:
        AIb = sys.argv[3]
        nArgs += 1
    
    
    if len(sys.argv) > nArgs + 1: 
        nArgs += 1
        try:
            nGames = int(sys.argv[nArgs])
        except:
            pass
        if len(sys.argv) > nArgs + 1: 
            nArgs += 1
            try:
                if sys.argv[nArgs].lower() == "true":
                    draw = True
                else:
                    draw = False
            except:
                pass

print("# of human players: ", players, "\nNumber of games: ", nGames, "\nDrawing game: ", draw, "\nAIa: ", AIa, "\nAIb: ", AIb)

for game in range(nGames):
    (winner, AIaTeam, AIbTeam) = gameLoop([], players, draw, AIa, AIb)

    print(f'Winner: {winner}\nAIa Team: {AIa}: {"red" if AIaTeam == (255, 0, 0) else "black"}\nAIb Team: {AIb}: {"red" if AIbTeam == (255, 0, 0) else "black"}')