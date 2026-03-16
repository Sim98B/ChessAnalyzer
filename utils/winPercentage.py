import numpy as np
from classes.eval import LineEval, PositionEval

def get_position_win_percentage(position:PositionEval) -> float | int:
    return get_line_win_percentage(position.lines[0])

def get_line_win_percentage(line: LineEval) -> float:
    if line.cp is not None:
        return get_win_percentage_from_cp(line.cp)
    if line.mate is not None:
        return get_win_percentage_from_mate(line.mate)
    raise ValueError("No cp or mate in line")

def get_win_percentage_from_mate(mate: int) -> int:
    return 100 if mate > 0 else 0

def get_win_percentage_from_cp(cp:int) -> float:
    cp_clipped = np.clip(cp, -1000, 1000)
    k = -0.00368208
    win_chance = 2 / (1 + np.exp(k * cp_clipped)) - 1
    return 50 + 50 * win_chance