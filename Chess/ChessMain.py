"""
Driver File. Handles user input and displaying current GameState object
"""

import pygame as p
from Chess import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

'''
Initialize a global dictionary of images. 
'''


def loadImages():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "wR", "wN", "wB", "wQ", "wK", "wp", "bp"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    # Note we can access an image by saying the key like IMAGES["wp"]


'''
Main Driver. Handling user input and updating graphics
'''


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False  # Flag variable for when a move is made

    print(gs.board)
    loadImages()
    running = True

    sqSelected = ()  # keep track of the last click of the user (tuple (row, col))
    playerClicks = []  # keep tracks of player clicks (two tuples)

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # (x,y) location of mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, col):  # player clicked the same square
                    sqSelected == ()  # undo the move
                    playerClicks == []  # clear player clicks
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)

                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getRealChessNotation())
                    if move in validMoves:
                        # print(move.getChessNotation())
                        gs.makeMove(move)
                        moveMade = True
                    sqSelected = ()
                    playerClicks = []

            # key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


def printBoard(board):
    for index in range(len(board)):
        print(board[index])
        print("\n")


'''
Responsible for graphics within the current game state
'''


def drawGameState(screen, gs):
    drawBoard(screen)  # draw squares on the board
    drawPieces(screen, gs.board)  # draw pieces on top of squares


'''
Draw Squares on the board
'''


def drawBoard(screen):
    color = 0

    for y in range(0, HEIGHT, SQ_SIZE):
        for x in range(0, WIDTH, SQ_SIZE):
            if color == 0:
                p.draw.rect(screen, p.Color(233, 210, 170), p.Rect(x, y, SQ_SIZE, SQ_SIZE))
                color = 1
            else:
                p.draw.rect(screen, p.Color(77, 89, 115), p.Rect(x, y, SQ_SIZE, SQ_SIZE))
                color = 0

        if color == 0:
            color = 1
        else:
            color = 0


'''
Draw Pieces on the board depending on the game states current board
'''


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]

            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()
