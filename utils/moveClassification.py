import numpy as np
import math


def basic_move_classification(win_before: float, win_after: float, player: bool):
    win_percentage_diff = (win_after - win_before) * (1 if player else -1)
    if win_percentage_diff < -20:
        return "BLUNDER"
    elif win_percentage_diff < -10:
        return "MISTAKE"
    elif win_percentage_diff < -5:
        return "INACCURACY"
    elif win_percentage_diff < -2:
        return "OKAY"
    else:
        return "EXCELLENT"
