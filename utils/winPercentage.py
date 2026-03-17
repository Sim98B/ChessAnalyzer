import numpy as np
import chess

def get_position_win_percentage(lines) -> float | int:
    return get_line_win_percentage(lines[0])

def get_line_win_percentage(line: dict, player: chess.Color) -> float:
    score = line["score"].white()
    if isinstance(score, chess.engine.Mate):
        return get_win_percentage_from_mate(score.mate())
    return get_win_percentage_from_cp(score.score())

def get_win_percentage_from_mate(mate: int) -> int:
    return 100 if mate > 0 else 0

def get_win_percentage_from_cp(cp:int) -> float:
    cp_clipped = np.clip(cp, -1000, 1000)
    k = -0.00368208
    win_chance = 2 / (1 + np.exp(k * cp_clipped)) - 1
    return 50 + 50 * win_chance