from Spiel2048 import *
from ctypes import windll
import pyautogui as pag

# time:
# getBoard:             0.268
# getpixel:             0.017
# euclidean_distance:   0.0000055
# turnBoard:            0.000011
# addTile:              0.0000046
# move:                 0.0000588
# legalMoves:           0.00015
# displayBoard:         0.052
# output:               0.1

dc= windll.user32.GetDC(0)
Farben = {0: (205, 192, 180),
          1: (238, 228, 218),
          2: (237, 224, 200),
          3: (242, 177, 121),
          4: (245, 149, 99),
          5: (245, 127, 95),
          6: (246, 94, 59),
          7: (237, 207, 114),
          8: (237, 204, 97),
          9: (237, 200, 80),
          10: (237, 197, 63),
          11: (237, 194, 46)
          }

def getpixel(x,y):
    pixel = windll.gdi32.GetPixel(dc,x,y)
    rgb = tuple( int(hex(pixel)[x:x+2], 16) for x in range(6, 1, -2) )
    return rgb

def euclidean_distance(p, q):
    """Calculate the Euclidean distance of two 3-dimensional points"""
    return pow( (p[0]-q[0])**2 + (p[1]-q[1])**2 + (p[2]-q[2])**2 ,0.5 )

def output(move):
    pag.press(["d", "w", "a", "s"][move])

def getPositions():
    """User enters the tile-positions"""
    if pag.alert("Move the Mouse to the \"New Game\" Button and press Enter") != "OK":
        raise Exception("Wrong")
    else:
        NewGame = pag.position()
    Diagonal = []
    for t in range(1, 17, 5):
        # Tiles start at 1
        if pag.alert("Move the Mouse to Tile " + str(t) + " and press Enter (your mouse isn't allowed to touch the number)") != "OK":
            raise Exception("Wrong")
        else:
            Diagonal.append(pag.position())
    Positions = tuple((x[0], y[1]) for y in Diagonal for x in Diagonal)
    return Positions, NewGame

def getBoard(Positions, nested=0):
    """Returns the gamestate"""
    if nested == 2:
        time.sleep(5)
    if nested > 3:
        return False
    RGB_Board = [getpixel(t[0], t[1]) for t in Positions] #Liste aller RGB Tuples
    Board = bytearray()
    for t in RGB_Board: #Check every Tile for the colour 
        for f in Farben.keys():
            if euclidean_distance(t, Farben[f]) <= 8:
                Board.append(f)
                break
    if len(Board) < 16:
        print("Error while reading the board. Trying again...")
        Board = getBoard(Positions, nested+1)
    return Board

def getValue(Board):
    Values = {7: 5, 8: 6, 9: 7, 10: 8, 11: 9, 12: 10, 13: 11, 14: 14.17}
    Value = 0
    for v in range(7, 15):
        Value += int( 2**Values[v] )*Board.count(v)
    return Value/2**5

def AI(Board, legal, turnTime):
    """Berechnet die beste Folge von Bewegungen, indem für
       turnTime viel Zeit zufällige Bewegungen ausprobiert werden,
       und der Zug genommen wird der am besten abschneidet"""
    Zeit = time.time()
    Move_score = [0]*4
    moves = legalMoves(Board)
    Depth = 0
    while time.time() - Zeit < turnTime:
        Depth += len(moves)
        for m in moves:
            b = move(Board, m)
            while True:
                Move_score[m] += 1
                b = addTile(b)
                legal = legalMoves(b)
                if not legal: break
                Move = legal[ int( random.random() * len(legal) ) ]
                b = move( b, Move )
    #print("Durchschnittlich",int(max(Move_score)/(Depth/len(moves))), "Züge vor dem Ende.\nBei", Depth, "Zügen.")
    return Move_score.index(max(Move_score)), Depth+1, Move_score

def outdoor():
    global Positions, NewGame, turnTime
    pag.click(Positions[15][0], Positions[15][1])
    Board = getBoard(Positions)
    displayBoard(Board)
    Zeit = 0
    while True:
        while not time.time()-Zeit > 0.25: time.sleep(0.01)
        Board = getBoard(Positions)
        if not Board:
            pag.click(NewGame)
            continue
        legal = legalMoves(Board)
        if not legal:
            displayBoard(Board)
            pag.click(NewGame)
        if len(legal) == 1:
            Move, Depth, Move_score = legal[0], 0, "?"
        else:
            Move, Depth, Move_score = AI(Board, legal, turnTime)
        output(Move)
        Zeit = time.time()
        print("Depth:", Depth)
        if type(Move_score) != str:
            print("Züge bis zum Ende:", round( max(Move_score) / (Depth/len(legal)), 1 ))
            print("Durchschnittliche Züge bis zum Ende:", round( sum(Move_score) / Depth, 1 ))
        else:
            print("Züge bis zum Ende:", Move_score )
            print("Durchschnittliche Züge bis zum Ende:", Move_score )
        displayBoard(Board)

def indoor():
    global turnTime
    Board = bytearray(16)
    Board = addTile(Board)
    t = time.time()
    for i in range(2**20):
        Board = addTile(Board)
        legal = legalMoves(Board)
        if not legal: break
        if time.time() > t:
            t += displayTime
            if type(Move_score) != str:
                print("Züge bis zum Ende:", round( max(Move_score) / (Depth/len(legal)), 1 ))
                print("Durchschnittliche Züge bis zum Ende:", round( sum(Move_score) / Depth, 1 ))
            else:
                print("Züge bis zum Ende:", Move_score )
                print("Durchschnittliche Züge bis zum Ende:", Move_score )
                displayBoard(Board)
        if len(legal) == 1:
            Move, Depth, Move_score = legal[0], 0, "?"
        else:
            Move, Depth, Move_score = AI(Board, legal, turnTime)
        Board = move(Board, Move)
    displayBoard(Board)
    return i

# Change this to "indoor" or "outdoor"
Modus = "outdoor"
if __name__ == '__main__':
    turnTime = 0.3
    if Modus == "indoor":
        while True:
            t = time.time()
            # After which time the board should be displayed again
            displayTime = 0
            i = indoor()
            print((time.time()-t) / (i - turnTime))
    elif Modus == "outdoor":
        Positions, NewGame = getPositions()
        outdoor()
