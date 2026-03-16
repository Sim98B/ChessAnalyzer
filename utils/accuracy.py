from classes.eval import Accuracy, PositionEval
from winPercentage import get_position_win_percentage

import math

def get_moves_accuracy(moves_win_percentage: list[float]) -> list[float]:
    moves_accuracy = []
    for index, win_percent in enumerate(moves_win_percentage[1:]):
        last_win_percent = moves_win_percentage[index]
        is_white_move = index % 2 == 0
        if is_white_move:
            win_diff = max(0, last_win_percent - win_percent)
        else:
            win_diff = max(0, win_percent - last_win_percent)
        raw_accuracy = (103.1668100711649 * math.exp(-0.04354415386753951 * win_diff) - 3.166924740191411)
        accuracy = min(100, max(0, raw_accuracy + 1))
        moves_accuracy.append(accuracy)
    return moves_accuracy