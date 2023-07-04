import math
import random
import string
import collections
import datetime
import re
import time
import copy

def createGameGrid(nRows, nCols):
   Board = [['~' for j in range(nCols)] for i in range(nRows)]
   return Board

def insertVessel(boardData, nRows, nCols, coord, ship):
    rows = int(coord[0]) - 1 if coord[0].isdigit() else ord(coord[0].upper()) - ord('A') + 9
    columns = int(coord[1]) - 1 if coord[1].isdigit() else ord(coord[1].upper()) - ord('A') + 9
    for i, p in enumerate(ship):
        if 0 <= rows < nRows and 0 <= columns+i < nCols:
            boardData[rows][columns + i] = p
    return boardData

 
def checkCoord(nRows, nCols, coord):
    if len(coord) != 2 or not coord.isalnum():
        return False
    rows = int(coord[0]) - 1 if coord[0].isdigit() else ord(coord[0].upper()) - ord('A') + 9
    columns = int(coord[1]) - 1 if coord[1].isdigit() else ord(coord[1].upper()) - ord('A') + 9
    return 0 <= rows < nRows and 0 <= columns < nCols


def changeGameGrid(boardData, boardMask, nRows, nCols, coord, score, lastMove):
    if not checkCoord(nRows, nCols, coord):
        lastMove = "[{},{}] is not a valid coordinate".format(*coord)
        return boardData, boardMask, score, lastMove
    rows = int(coord[0]) - 1 if coord[0].isdigit() else ord(coord[0].upper()) - ord('A') + 9
    columns = int(coord[1]) - 1 if coord[1].isdigit() else ord(coord[1].upper()) - ord('A') + 9
    if boardData[rows][columns] not in ["~", "X"]:
        score += 5
        lastMove = "Torpedo HIT '{}' at [{},{}]".format(boardData[rows][columns], *coord)
        boardMask[rows][columns] = boardData[rows][columns]
        i = 1
        while 0 <= rows < nRows and 0 <= columns+i < nCols and boardData[rows][columns+i] not in ["~", "X"]:
            boardMask[rows][columns+i] = boardData[rows][columns+i]
            score += 5
            i += 1
    else:
        lastMove = "Torpedo MISS at [{},{}]".format(*coord)
        boardMask[rows][columns] = 'X'
    print("\n  Search And Destroy")
    print("  123456789ABCDEFGHIJKLMNOPQRST")
    for i in range(nRows):
        rowLabel = chr(ord('A') + i - 10) if i >= 9 else str(i + 1)
        row = [boardMask[i][j] for j in range(nCols)]
        print(rowLabel + "|" + "".join(row) + "|")
    print("Current Score:{:03d} Last Move: {}".format(score, lastMove))
    
    return boardData, boardMask, score, lastMove

def main( ) :
   r,c = 16,29
   iCoords = ["11", "1O", "G1", "GM", "77"]
   ships = ["[CARRIER=>", "[FRG=>", "[BCRUSR=>", "[DSTYR=>", "[SUBM=>"]
   score = 0
   lastMove = ""
   #                       carrier      frigate     submarine   cruiser             destroyer
   #           false miss  hit   false  hit   miss  hit   miss  hit    false  miss  hit   miss
   pCoords = ["AZ", "37", "1A", "CXA", "1O", "99", "79", "AP", "G2",  "  ",  "5K", "GO",  "2B"]

   gBoard = createGameGrid(r, c)

   gMask = copy.deepcopy(gBoard)

   for i in range(len(iCoords)) :
      gBoard = insertVessel(gBoard, r, c, iCoords[i], ships[i])
   for j in pCoords :
      print(checkCoord(r, c, j))

   for j in pCoords :
      print( )
      (gBoard, gMask, score, lastMove) = changeGameGrid(gBoard, gMask, r, c, j, score, lastMove)

if __name__ == "__main__" :
   main( )
