from game import Game
from state import State
from Pick import Pick, PickMove, PickState
import numpy as np
import random

def alphaBetaAlgorithm(gameState, depth, alpha, beta, maxPlayer):
    if (depth == 0 or gameState.is_finished()):
        return gameState.heuristic(), None
    
    # maximizing player
    if maxPlayer:
        best_val = float("-inf")
        best_move = None
        same_value_moves = []
        for move in gameState.get_moves():
            new_gameState = gameState.make_move(move)
            value,x = alphaBetaAlgorithm(new_gameState, depth-1, alpha, beta, False)
            
            if value == best_val:
                same_value_moves.append(move)
            if value > best_val:
                best_move = move
                same_value_moves = [best_move]
            best_val = max(best_val, value)
            alpha = max(alpha, best_val)

            if alpha >= beta:
                break
        
        chosen_move = random.choice(same_value_moves)
        return best_val, random.choice(same_value_moves)
    
    else:
        best_val = float("inf")
        best_move = None
        same_value_moves = []
        for move in gameState.get_moves():
            new_gameState = gameState.make_move(move)
            value,x = alphaBetaAlgorithm(new_gameState, depth-1, alpha, beta, True)
            
            if value == best_val:
                same_value_moves.append(move)
            if value < best_val:
                best_move = move
                same_value_moves = [best_move]
            best = min(best_val, value)
            beta = min(beta, best_val)
            
            if alpha >= beta:
                break

        chosen_move = random.choice(same_value_moves)
        return best_val, random.choice(same_value_moves)
