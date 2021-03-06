#!/usr/bin/python

import constants
from copy import deepcopy

def kingLocator(board, player):
    """
    Determines the location of the king of a given player.
    
    @param board:   A list of lists representing the board state.
    @param player:  Player (e.g. constants.WHITE_PLAYER).
    @return:        Returns the indicies of the current player's king (e.g. [0, 4]).
    """
    if player == constants.WHITE_PLAYER:
        piece = constants.KING_SYMBOL
    else:
        piece = constants.BLACK_KING_SYMBOL
        
    for line in board:
        if piece in line:
            location = [board.index(line), line.index(piece)]
                
    return location

def isCheckMate(board, player):
    """
    Determines if game has ended.

    @param board:   A list of lists representing the board state.
    @param player:  The current player (e.g. constants.WHITE_PLAYER)
    @return:        True if game has ended, False otherwise.
    """
    boardCopy = board.getBoard()
    location = kingLocator(boardCopy, player)
    acceptable = [0, 1, 2, 3, 4, 5, 6, 7]
    
    #Tests if king is in check
    if isCheckStatic(boardCopy, player) == False:
        return False

    #Tests if king can move/attack out of check
    escapeRoutes = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
    for route in escapeRoutes:
        route[0] = route[0] + location[0]
        route[1] = route[1] + location[1]
        testMove = location + route
        if testMove[2] not in acceptable or testMove[3] not in acceptable:
            continue
        if board.isLegalMove(player, testMove) == True:
            if isCheck(boardCopy, player, testMove) == False:
                return False

    #Tests if king can get blocked out of check - for NE/SW diagonal
    if isCheckByDiagonal(location, boardCopy, player) == True:
        for space in range(-len(boardCopy), len(boardCopy)):
            for horizontalSpace in range(len(boardCopy)):
                for verticalSpace in range(len(boardCopy)):
                    if location[0] + space not in acceptable or \
                       location[1] + space not in acceptable:
                        continue
                    move = [horizontalSpace, verticalSpace, location[0] + space, location[1] + space]
                    if board.isLegalMove(player, move) == True:
                        if isCheck(boardCopy, player, move) == False:
                            return False
                   
    #Tests if king can get blocked out of check - for NW/SE diagonal
    if isCheckByDiagonal(location, boardCopy, player) == True:
        for space in range(-len(boardCopy), len(boardCopy)):
            for horizontalSpace in range(len(boardCopy)):
                for verticalSpace in range(len(boardCopy)):
                    if location[0] + space not in acceptable or \
                       location[1] + space not in acceptable:
                        continue
                    move = [horizontalSpace, verticalSpace, location[0] - space, location[1] + space]
                    if board.isLegalMove(player, move) == True:
                        if isCheck(boardCopy, player, move) == False:
                            return False
    
    #Tests if king can get blocked out of check - for horizontal check
    if isCheckByHorizontal(location, boardCopy, player) == True:
        for space in range(len(boardCopy)):
            for horizontalSpace in range(len(boardCopy)):
                for verticalSpace in range(len(boardCopy)):
                    move = [horizontalSpace, verticalSpace, space, location[1]]
                    if board.isLegalMove(player, move) == True:
                        if isCheck(boardCopy, player, move) == False:
                            return False
                    
    #Tests if king can get blocked out of check - for vertical check
    if isCheckByVertical(location, boardCopy, player) == True:
        for space in range(len(boardCopy)):
            for horizontalSpace in range(len(boardCopy)):
                for verticalSpace in range(len(boardCopy)):
                    move = [horizontalSpace, verticalSpace, location[0], space]
                    if board.isLegalMove(player, move) == True:
                        if isCheck(boardCopy, player, move) == False:
                            return False
    
    return True

def isCheck(board, player, move):
    """
    Determines if king is in check after move.

    @param board:   A list of lists representing the board state.
    @param player:  Player (e.g. constants.WHITE_PLAYER).
    @param move:    Four character combination representing move (e.g. [1, 2, 1, 4]).
    @return:        True if king is in check, False otherwise.
    """
    testBoard = deepcopy(board)
    testPiece = board[move[0]][move[1]]
    testBoard[move[2]][move[3]] = testPiece
    testBoard[move[0]][move[1]] = constants.EMPTY_SYMBOL

    location = kingLocator(testBoard, player)
    
    if isCheckByDiagonal(location, testBoard, player) == True:
        return True
    if isCheckByHorizontal(location, testBoard, player) == True:
        return True
    if isCheckByVertical(location, testBoard, player) == True:
        return True
    if isCheckByKing(location, testBoard, player) == True:
        return True
    if isCheckByPawn(location, testBoard, player) == True:
        return True
    if isCheckByKnight(location, testBoard, player) == True:
        return True

    return False

def isCheckStatic(board, player):
    """
    Determines if king is in check.
    
    @param board:   A list of lists representing the board state.
    @param player:  Player (e.g. constants.WHITE_PLAYER).
    @return:        True if king is in check, False otherwise.
    """
    location = kingLocator(board, player)
    
    if isCheckByDiagonal(location, board, player) == True:
        return True
    if isCheckByHorizontal(location, board, player) == True:
        return True
    if isCheckByVertical(location, board, player) == True:
        return True
    if isCheckByKing(location, board, player) == True:
        return True
    if isCheckByPawn(location, board, player) == True:
        return True
    if isCheckByKnight(location, board, player) == True:
        return True

    return False    

def isCheckByDiagonal(location, board, player):
    """
    Helper method to determine if king under attack by bishop or queen diagonally.

    @param location:   Location of current player's king.
    @param board:      A list of lists representing the board state.
    @param player:     Player (e.g. constants.WHITE_PLAYER).
    @return:           True if king is in check, False otherwise.
    """
    acceptable = [0, 1, 2, 3, 4, 5, 6, 7]

    if player == constants.WHITE_PLAYER:
        #Testing for check from NE diagonal
        space = 1
        while location[0] + space in acceptable and location[1] + space in acceptable:
            if board[location[0] + space][location[1] + space] == constants.EMPTY_SYMBOL:
                space += 1
                continue
            if board[location[0] + space][location[1] + space] == constants.BLACK_BISHOP_SYMBOL or \
               board[location[0] + space][location[1] + space] == constants.BLACK_QUEEN_SYMBOL:
               return True
            else:
               break
                
        #Testing for check from NW diagonal
        space = 1
        while location[0] - space in acceptable and location[1] + space in acceptable:
            if board[location[0] - space][location[1] + space] == constants.EMPTY_SYMBOL:
                space += 1
                continue
            if board[location[0] - space][location[1] + space] == constants.BLACK_BISHOP_SYMBOL or \
               board[location[0] - space][location[1] + space] == constants.BLACK_QUEEN_SYMBOL:
               return True
            else:
               break
        
        #Testing for check from SE diagonal        
        space = 1
        while location[0] + space in acceptable and location[1] - space in acceptable:
            if board[location[0] + space][location[1] - space] == constants.EMPTY_SYMBOL:
                space += 1
                continue
            if board[location[0] + space][location[1] - space] == constants.BLACK_BISHOP_SYMBOL or \
               board[location[0] + space][location[1] - space] == constants.BLACK_QUEEN_SYMBOL:
               return True
            else:
               break
         
        #Testing for check from SW diagonal        
        space = 1
        while location[0] - space in acceptable and location[1] - space in acceptable:
            if board[location[0] - space][location[1] - space] == constants.EMPTY_SYMBOL:
                space += 1
                continue
            if board[location[0] - space][location[1] - space] == constants.BLACK_BISHOP_SYMBOL or \
               board[location[0] - space][location[1] - space] == constants.BLACK_QUEEN_SYMBOL:
               return True
            else:
               break
         
        return False
         
    else:
        #Testing for check from NE diagonal
        space = 1
        while location[0] + space in acceptable and location[1] + space in acceptable:
            if board[location[0] + space][location[1] + space] == constants.EMPTY_SYMBOL:
                space += 1
                continue
            if board[location[0] + space][location[1] + space] == constants.BISHOP_SYMBOL or \
               board[location[0] + space][location[1] + space] == constants.QUEEN_SYMBOL:
               return True
            else:
               break
                
        #Testing for check from NW diagonal
        space = 1
        while location[0] - space in acceptable and location[1] + space in acceptable:
            if board[location[0] - space][location[1] + space] == constants.EMPTY_SYMBOL:
                space += 1
                continue
            if board[location[0] - space][location[1] + space] == constants.BISHOP_SYMBOL or \
               board[location[0] - space][location[1] + space] == constants.QUEEN_SYMBOL:
               return True
            else:
               break
        
        #Testing for check from SE diagonal        
        space = 1
        while location[0] + space in acceptable and location[1] - space in acceptable:
            if board[location[0] + space][location[1] - space] == constants.EMPTY_SYMBOL:
                space += 1
                continue
            if board[location[0] + space][location[1] - space] == constants.BISHOP_SYMBOL or \
               board[location[0] + space][location[1] - space] == constants.QUEEN_SYMBOL:
               return True
            else:
               break
         
        #Testing for check from SW diagonal        
        space = 1
        while location[0] - space in acceptable and location[1] - space in acceptable:
            if board[location[0] - space][location[1] - space] == constants.EMPTY_SYMBOL:
                space += 1
                continue
            if board[location[0] - space][location[1] - space] == constants.BISHOP_SYMBOL or \
               board[location[0] - space][location[1] - space] == constants.QUEEN_SYMBOL:
               return True
            else:
               break
         
        return False

def isCheckByHorizontal(location, board, player):
    """
    Helper method to determine if king under attack by rook or queen horizontally.

    @param location:   Location of current player's king.
    @param board:      A list of lists representing the board state.
    @param player:     Player (e.g. constants.WHITE_PLAYER).
    @return:           True if king is in check, False otherwise.
    """
    if player == constants.WHITE_PLAYER:
        #Checks for rooks and queens in the same row as king
        for space in range(len(board)):
            if board[space][location[1]] == constants.BLACK_ROOK_SYMBOL or \
            board[space][location[1]] == constants.BLACK_QUEEN_SYMBOL:
                #Checks for blocking pieces if piece comes before the king horizontally
                if space < location[0]:
                    blocking = 0
                    for new_space in range(space + 1, location[0]):
                        if board[new_space][location[1]] != constants.EMPTY_SYMBOL:
                            blocking += 1
                    if blocking == 0:
                        return True
                #Checks for blocking pieces if piece comes after the king horizontally
                else:
                    blocking = 0
                    for new_space in range(location[0] + 1, space):
                        if board[new_space][location[1]] != constants.EMPTY_SYMBOL:
                            blocking += 1
                    if blocking == 0:
                        return True

        return False
                    
    else:
        #Checks for rooks and queens in the same row as king
        for space in range(len(board)):
            if board[space][location[1]] == constants.ROOK_SYMBOL or \
            board[space][location[1]] == constants.QUEEN_SYMBOL:
                #Checks for blocking pieces if piece comes before the king horizontally
                if space < location[0]:
                    blocking = 0
                    for new_space in range(space + 1, location[0]):
                        if board[new_space][location[1]] != constants.EMPTY_SYMBOL:
                            blocking += 1
                    if blocking == 0:
                        return True
                #Checks for blocking pieces if piece comes after the king horizontally
                else:
                    blocking = 0
                    for new_space in range(location[0] + 1, space):
                        if board[new_space][location[1]] != constants.EMPTY_SYMBOL:
                            blocking += 1
                    if blocking == 0:
                        return True

        return False
                    
def isCheckByVertical(location, board, player):
    """
    Helper method to determine if king under attack by rook or queen vertically.

    @param location:   Location of current player's king.
    @param board:      A list of lists representing the board state.
    @param player:     Player (e.g. constants.WHITE_PLAYER).
    @return:           True if king is in check, False otherwise.
    """
    if player == constants.WHITE_PLAYER:
        #Checks for rooks and queens in same column as king
        for space in range(len(board)):
            if board[location[0]][space] == constants.BLACK_ROOK_SYMBOL or \
            board[location[0]][space] == constants.BLACK_QUEEN_SYMBOL:
                #Checks for blocking pieces if piece comes before the king vertically
                if space < location[1]:
                    blocking = 0
                    for new_space in range(space + 1, location[1]):
                        if board[location[0]][new_space] != constants.EMPTY_SYMBOL:
                            blocking += 1
                    if blocking == 0:
                        return True
                #Checks for blocking pieces if piece comes after the king horizontally
                else:
                    blocking = 0
                    for new_space in range(location[1] + 1, space):
                        if board[location[0]][new_space] != constants.EMPTY_SYMBOL:
                            blocking += 1
                    if blocking == 0:
                        return True
                    
        return False
                    
    else:
        #Checks for rooks and queens in same column as king
        for space in range(len(board)):
            if board[location[0]][space] == constants.ROOK_SYMBOL or \
            board[location[0]][space] == constants.QUEEN_SYMBOL:
                #Checks for blocking pieces if piece comes before the king vertically
                if space < location[1]:
                    blocking = 0
                    for new_space in range(space + 1, location[1]):
                        if board[location[0]][new_space] != constants.EMPTY_SYMBOL:
                            blocking += 1
                    if blocking == 0:
                        return True
                #Checks for blocking pieces if piece comes after the king vertically
                else:
                    blocking = 0
                    for new_space in range(location[1] + 1, space):
                        if board[location[0]][new_space] != constants.EMPTY_SYMBOL:
                            blocking += 1
                    if blocking == 0:
                        return True

        return False
                    
def isCheckByKing(location, board, player):
    """
    Helper method to determine if king under attack by knight.

    @param location:   Location of current player's king.
    @param board:      A list of lists representing the board state.
    @param player:     Player (e.g. constants.WHITE_PLAYER).
    @return:           True if king is in check, False otherwise.
    """
    if player == constants.WHITE_PLAYER:
        #Checks if white king is in check by black king
        if 1 <= location[0]:
            if board[location[0] - 1][location[1]] == constants.BLACK_KING_SYMBOL:
                return True
        if location[0] <= 6:
            if board[location[0] + 1][location[1]] == constants.BLACK_KING_SYMBOL:
                return True
        if 1 <= location[1]:
            if board[location[0]][location[1] - 1] == constants.BLACK_KING_SYMBOL:
                return True
        if location[1] <= 6:
            if board[location[0]][location[1] + 1] == constants.BLACK_KING_SYMBOL:
                return True
        if 1 <= location[0] and 1 <= location[1]:
            if board[location[0] - 1][location[1] - 1] == constants.BLACK_KING_SYMBOL:
                return True
        if location[0] <= 6 and 1 <= location[1]:
            if board[location[0] + 1][location[1] - 1] == constants.BLACK_KING_SYMBOL:
                return True
        if location[0] <= 1 and location[1] <= 6:
            if board[location[0] - 1][location[1] + 1] == constants.BLACK_KING_SYMBOL:
                return True
        if location[0] <= 6 and location[1] <= 6:
            if board[location[0] + 1][location[1] + 1] == constants.BLACK_KING_SYMBOL:
                return True
            
        return False

    else:
        #Checks if black king is in check by white king
        if 1 <= location[0]:
            if board[location[0] - 1][location[1]] == constants.KING_SYMBOL:
                return True
        if location[0] <= 6:
            if board[location[0] + 1][location[1]] == constants.KING_SYMBOL:
                return True
        if 1 <= location[1]:
            if board[location[0]][location[1] - 1] == constants.KING_SYMBOL:
                return True
        if location[1] <= 6:
            if board[location[0]][location[1] + 1] == constants.KING_SYMBOL:
                return True
        if 1 <= location[0] and 1 <= location[1]:
            if board[location[0] - 1][location[1] - 1] == constants.KING_SYMBOL:
                return True
        if location[0] <= 6 and 1 <= location[1]:
            if board[location[0] + 1][location[1] - 1] == constants.KING_SYMBOL:
                return True
        if location[0] <= 1 and location[1] <= 6:
            if board[location[0] - 1][location[1] + 1] == constants.KING_SYMBOL:
                return True
        if location[0] <= 6 and location[1] <= 6:
            if board[location[0] + 1][location[1] + 1] == constants.KING_SYMBOL:
                return True
            
        return False

def isCheckByPawn(location, board, player):
    """
    Helper method to determine if king under attack by pawn.

    @param location:   Location of current player's king.
    @param board:      A list of lists representing the board state.
    @param player:     Player (e.g. constants.WHITE_PLAYER).
    @return:           True if king is in check, False otherwise.
    """
    if player == constants.WHITE_PLAYER:
        #Checks if white king is under attack by black pawn
        if 1 <= location[0] and location[1] <= 6:
            if board[location[0] - 1][location[1] + 1] == constants.BLACK_PAWN_SYMBOL:
                return True
        if location[0] <= 6 and location[1] <= 6:
            if board[location[0] + 1][location[1] + 1] == constants.BLACK_PAWN_SYMBOL:
                return True

        return False

    else:
        #Checks if black king under attack by white pawn
        if 1 <= location[0] and 1 <= location[1]:
            if board[location[0] - 1][location[1] - 1] == constants.PAWN_SYMBOL:
                return True
        if location[0] <= 6 and 1 <= location[1]:
            if board[location[0] + 1][location[1] - 1] == constants.PAWN_SYMBOL:
                return True

        return False

def isCheckByKnight(location, board, player):
    """
    Helper method to determine if king under attack by knight.

    @param location:   Location of current player's king.
    @param board:      A list of lists representing the board state.
    @param player:     Player (e.g. constants.WHITE_PLAYER).
    @return:           True if king is in check, False otherwise.
    """
    if player == constants.WHITE_PLAYER:
        #Checks locations where black knight would put white king in check
        if 2 <= location[0] and 2 <= location[1]:
            if board[location[0] - 2][location[1] - 1] == constants.BLACK_KNIGHT_SYMBOL or \
               board[location[0] - 1][location[1] - 2] == constants.BLACK_KNIGHT_SYMBOL:
                return True
            
        if location[0] <= 5 and location[1] <= 5:
            if board[location[0] + 1][location[1] + 2] == constants.BLACK_KNIGHT_SYMBOL or \
               board[location[0] + 2][location[1] + 1] == constants.BLACK_KNIGHT_SYMBOL:
                return True
        
        if 2 <= location[0] and location[1] <= 5:
            if board[location[0] - 2][location[1] + 1] == constants.BLACK_KNIGHT_SYMBOL or \
            board[location[0] - 1][location[1] + 2] == constants.BLACK_KNIGHT_SYMBOL:
                return True

        if location[0] <= 5 and 2 <= location[1]:
            if board[location[0] + 2][location[1] - 1] == constants.BLACK_KNIGHT_SYMBOL or \
            board[location[0] + 1][location[1] - 2] == constants.BLACK_KNIGHT_SYMBOL:
                return True

        return False
        
    else:
        #Checks locations where white knight would put black king in check
        if 2 <= location[0] and 2 <= location[1]:
            if board[location[0] - 2][location[1] - 1] == constants.KNIGHT_SYMBOL or \
               board[location[0] - 1][location[1] - 2] == constants.KNIGHT_SYMBOL:
                return True
            
        if location[0] <= 5 and location[1] <= 5:
            if board[location[0] + 1][location[1] + 2] == constants.KNIGHT_SYMBOL or \
               board[location[0] + 2][location[1] + 1] == constants.KNIGHT_SYMBOL:
                return True
        
        if 2 <= location[0] and location[1] <= 5:
            if board[location[0] - 2][location[1] + 1] == constants.KNIGHT_SYMBOL or \
            board[location[0] - 1][location[1] + 2] == constants.KNIGHT_SYMBOL:
                return True

        if location[0] <= 5 and 2 <= location[1]:
            if board[location[0] + 2][location[1] - 1] == constants.KNIGHT_SYMBOL or \
            board[location[0] + 1][location[1] - 2] == constants.KNIGHT_SYMBOL:
                return True

        return False
