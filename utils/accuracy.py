import chess

import math

def get_move_accuracy(delta: float, turn: chess.Color) -> float:
    if turn == chess.WHITE:
        win_diff = max(0, -delta)
    else:
        win_diff = max(0, delta)
    raw_accuracy = (103.1668100711649* math.exp(-0.04354415386753951 * win_diff)- 3.166924740191411)
    accuracy = min(100, max(0, raw_accuracy + 1))
    return accuracy