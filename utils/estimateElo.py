import math

def get_position_cp(info) -> int:
    score = info["score"].white()
    if score.is_mate():
        mate = score.mate()
        cp = mate * 100000
    else:
        cp = score.score()
    cp = max(-1000, min(1000, cp))
    return cp

def get_players_average_cpl(positions_cp):
    previous_cp = positions_cp[0]
    white_cpl = 0
    black_cpl = 0
    for index, cp in enumerate(positions_cp[1:]):
        if index % 2 == 0:
            white_cpl += 0 if cp > previous_cp else min(previous_cp - cp, 1000)
        else:
            black_cpl += 0 if cp < previous_cp else min(cp - previous_cp, 1000)
        previous_cp = cp
    white_moves = math.ceil((len(positions_cp) - 1) / 2)
    black_moves = math.floor((len(positions_cp) - 1) / 2)
    return {
        "whiteCpl": white_cpl / white_moves if white_moves else 0,
        "blackCpl": black_cpl / black_moves if black_moves else 0,
    }

def get_elo_from_average_cpl(average_cpl: float) -> float:
    return 3100 * math.exp(-0.01 * average_cpl)

def get_average_cpl_from_elo(elo: float) -> float:
    return -100 * math.log(min(elo, 3100) / 3100)

def get_elo_from_rating_and_cpl(game_cpl: float, rating: float | None) -> float:
    elo_from_cpl = get_elo_from_average_cpl(game_cpl)
    if rating is None:
        return elo_from_cpl
    expected_cpl = get_average_cpl_from_elo(rating)
    cpl_diff = game_cpl - expected_cpl
    if cpl_diff == 0:
        return elo_from_cpl
    if cpl_diff > 0:
        return rating * math.exp(-0.005 * cpl_diff)
    else:
        return rating / math.exp(-0.005 * -cpl_diff)