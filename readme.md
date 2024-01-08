# Welcome to AI checkers!

To start a basic game of checkers with two human players, run the command:
`python init.py`
This will, by default, run one standard game of checkers, classic human v. human style.


## Running checkers with AI
The initializer is extremely sensitive to command line arguments, and will fail to run the game properly if the command line arguments are not in the correct order. There are three different formats that the arguments can be in:

 1. No AI. If, for some reason, you plan to play a game with two human players and either turn off drawing the game, or you would like to play multiple games and keep an average, the format is:\
   `python init.py nAI(optional, 0) nGames(optional, required if drawBool) drawBool(optional)`
   i.e. if you want to play with 2 humans (0 robots), you want to play 3 games, and you want the game to be drawn on screen:\
   `python init.py 0 3 True`
 2. One AI. If you specify that there is one AI player, init.py expects an additional argument after the number of AIs for what type of algorithm the AI is using. It can be only one of three values: `breadth-first`, `depth-first` or `minimax`. The format is now:\
 `python init.py nAI(optional, 1) AIaType(required, if nAI>0) nGames(optional, required if drawBool) drawBool(optional)`\
 i.e. if you want to play two games against the breadth-first algorithm, but you didn't want to be able to see the game:
 `python init.py 1 breadth-first 2 False`
 3. Lastly, two AI. If you specify that there are two AIs playing against each other, init.py expects two arguments after the number of AIs for what type of algorithm each AI should use. The same three algorithms from above still apply. The format is now:\
 `python init.py nAI(optional, 2) AIaType(required, if nAI>0) AIbType(required, if nAI>1) nGames(optional, required if drawBool) drawBool(optional)`\
 i.e. One game of depth-first vs minimax:\
 `python init.py 2 depth-first minimax`

The final two arguments, nGames (number of games) and drawBool (are you going to draw the board? ) are both optional, and by default, nGames = 1, drawBool = True.
However, if you choose to leave nGames out of the command, you have to leave drawBool out as well. nGames can be specified without drawBool.

All of this to say, I am bad at setting up multiple ways to run a program, so this was the best solution I could come up with. All of the command line arguments are based on length and contents of what is already in the command, which is less than ideal, but it makes sense in my brain.