import numpy as np
import random
import time

def displayBoard(b, move=-1):
    """Displays the Board"""
    s = "#"*33
    s += "\n"
    for row in range(4):
        for tile in range(4):
            if b[4*row + tile] == 0:
                s += "0\t"
            else:
                s += str(2** b[4*row + tile]) + "\t"
        s += ["#", "➡", "⬆", "⬅", "⬇"][move+1] + "\n"
    s += "#"*33
    print(s)

def turnBoard(b, n):
    """Rotates a Board n-times clockwise"""
    for turns in range(n % 4):
        new = bytearray([ b[12], b[8], b[4], b[0], b[13], b[9], b[5], b[1], b[14], b[10], b[6], b[2], b[15], b[11], b[7], b[3] ])
        b = new.copy()
    return b

def legalMoves(b):
    """Returns all the legal moves"""
    legal = bytearray()
    for m in range(1, 5):
        b = turnBoard(b, 1)
        # Es muss nur eine Reihe Legit sein
        for r in range(4):
            # Wenn ein Platz rechts von einer nicht 0 frei sind ist der move legit
            if b[r*4+ 0] != 0 and b[r*4+ 1] == 0:
                legal.append(m)
                break
            elif b[r*4+ 0] != 0 and b[r*4+ 2] == 0:
                legal.append(m)
                break
            elif b[r*4+ 0] != 0 and b[r*4+ 3] == 0:
                legal.append(m)
                break
            elif b[r*4+ 1] != 0 and b[r*4+ 2] == 0:
                legal.append(m)
                break
            elif b[r*4+ 1] != 0 and b[r*4+ 3] == 0:
                legal.append(m)
                break
            elif b[r*4+ 2] != 0 and b[r*4+ 3] == 0:
                legal.append(m)
                break
            else:
                for t in range(1, 4):
                    if b[r*4+ t-1] != 0 and b[r*4+ t-1] == b[r*4+ t]:
                        legal.append(m)
                        break    
    legal = [ x%4 for x in set(legal) ]
    return legal

def move(b, Direction):
    """Returns the Gamestate after a move
       0 = right, 1 = up, 2 = left, 3 = down"""
    Before = turnBoard(b, Direction) # Dreht das Brett in die richtige Richtung
    After = bytearray()
    for r in range(4)[::-1]:
        row = Before[r*4:r*4+4]
        row = row.replace(b"\x00", b"") # Löscht die 0er
        length = len(row)

        if length == 0 or length == 1:  #Bei k-/einer Zahl/-en muss nichts gemacht werden
            pass
        
        elif length == 2:          #Entweder gleich oder nicht
            if row[0] == row[1]:
                row[1] += 1
                del row[0]
            else:
                pass
                
        elif length == 3:        #Entweder die 1. beiden gleich, die letzten 2 oder nicht
            if row[1] == row[2]:
                row[2] += 1
                del row[1]
            elif row[0] == row[1]:
                row[1] += 1
                del row[0]
            else:
                pass

        elif length == 4:    #vorne und hinten gleich, die 1. beiden, die letzten 2 oder nicht
            if row[0] == row[1] and row[2] == row[3]:
                row[3] += 1
                row[2] = row[0]+1
                del row[:2]
            elif row[2] == row[3]:
                row[3] += 1
                del row[2]
            elif row[1] == row[2]:
                row[2] += 1
                del row[1]
            elif row[0] == row[1]:
                row[1] += 1
                del row[0]
            else:
                pass
        for removed in range(4-len(row)): row.insert(0, 0)
        After.extend(row.copy())
    After.reverse()
    After = turnBoard(After, 4-Direction) # Dreht Brett zurück
    return After

def addTile(b):
    while True:
        r = int(random.random()*16)
        if b[r] == 0:
            if random.random() < 0.9:
                b[r] = 1
            else:
                b[r] = 2
            break
    return b

def t(g):
    t = time.time()
    for i in range(g):
        Board = bytearray([0])*16
        while True:
            Board = addTile(Board)
            legal = legalMoves(Board)
            if not legal: break
            Move = random.choice(legal)
            Board = move(Board, Move)
    return (time.time() - t) / g
