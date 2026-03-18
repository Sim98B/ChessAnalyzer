from utils.chess_utils import is_simple_piece_recapture, get_is_piece_sacrifice

def basic_move_classification(win_before: float, win_after: float, player: bool):
    win_percentage_diff = (win_after - win_before) * (1 if player else -1)
    if win_percentage_diff < -20:
        return "Blunder"
    elif win_percentage_diff < -10:
        return "Mistake"
    elif win_percentage_diff < -5:
        return "Inaccuracy"
    elif win_percentage_diff < -2:
        return "Good"
    else:
        return "Excellent"

def is_splendid_move(
    last_position_win_percentage: float,
    position_win_percentage: float,
    player: bool,
    played_move: str,
    best_line_pv_to_play: list[str],
    fen: str,
    last_position_alternative_line_win_percentage: float | None
) -> bool:
    if last_position_alternative_line_win_percentage is None:
        return False

    win_percentage_diff = (position_win_percentage - last_position_win_percentage) * (1 if player else -1)
    if win_percentage_diff < -2:
        return False

    if not get_is_piece_sacrifice(fen, played_move, best_line_pv_to_play):
        return False

    if is_losing_or_alternate_completely_winning(position_win_percentage,
                                                 last_position_alternative_line_win_percentage,
                                                 player):
        return False

    return True

def is_perfect_move(
    last_position_win_percentage: float,
    position_win_percentage: float,
    player: bool,
    last_position_alternative_line_win_percentage: float | None,
    fen_two_moves_ago: str | None,
    uci_moves: list[str] | None
) -> bool:
    if last_position_alternative_line_win_percentage is None:
        return False
    win_percentage_diff = (position_win_percentage - last_position_win_percentage) * (1 if player else -1)
    if win_percentage_diff < -2:
        return False
    if fen_two_moves_ago and uci_moves and is_simple_piece_recapture(fen_two_moves_ago, uci_moves):
        return False
    if is_losing_or_alternate_completely_winning(
        position_win_percentage,
        last_position_alternative_line_win_percentage,
        player
    ):
        return False
    has_changed_game_outcome = get_has_changed_game_outcome(
        last_position_win_percentage,
        position_win_percentage,
        player
    )
    is_the_only_good_move = get_is_the_only_good_move(
        position_win_percentage,
        last_position_alternative_line_win_percentage,
        player
    )
    return has_changed_game_outcome or is_the_only_good_move

def is_losing_or_alternate_completely_winning(position_win_percentage: float,
                                               last_position_alternative_line_win_percentage: float,
                                               player: bool) -> bool:
    is_losing = position_win_percentage < 50 if player else position_win_percentage > 50
    is_alternate_completely_winning = (last_position_alternative_line_win_percentage > 97 if player
                                       else last_position_alternative_line_win_percentage < 3)
    return is_losing or is_alternate_completely_winning

def get_has_changed_game_outcome(last_position_win_percentage: float,
                                 position_win_percentage: float,
                                 player: bool) -> bool:
    win_percentage_diff = (position_win_percentage - last_position_win_percentage) * (1 if player else -1)
    return (win_percentage_diff > 10 and
            ((last_position_win_percentage < 50 and position_win_percentage > 50) or
             (last_position_win_percentage > 50 and position_win_percentage < 50)))

def get_is_the_only_good_move(position_win_percentage: float,
                              last_position_alternative_line_win_percentage: float,
                              player: bool) -> bool:
    win_percentage_diff = (position_win_percentage - last_position_alternative_line_win_percentage) * (1 if player else -1)
    return win_percentage_diff > 10
