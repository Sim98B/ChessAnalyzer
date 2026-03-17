import chess
import chess.engine
import chess.pgn
import json
import numpy as np

from utils.winPercentage import get_line_win_percentage
from utils.accuracy import get_move_accuracy, get_player_accuracy, calc_weights
from utils.estimateElo import get_position_cp, get_players_average_cpl, get_elo_from_rating_and_cpl
from utils.moveClassification import basic_move_classification

engine = chess.engine.SimpleEngine.popen_uci("engine/stockfish_16_1")
depth = 22
with open("games/game3.pgn") as f:
    game = chess.pgn.read_game(f)

with open("openings_by_fen.json") as f:
    openings = json.load(f)

w_acc = []
b_acc = []
positions_cp = []
board = game.board()
prev_board = None
for index, move in enumerate(game.mainline_moves()):
    if board.is_checkmate():
        print("Checkmate")
        break
    elif board.is_stalemate():
        print("Stalemate")
        break
    print(f"White {move}" if board.turn else f"Black {move}")
    player = board.turn
    is_forced = len(list(board.legal_moves)) == 1
    if is_forced:
        print("FORCED")
    info_before = engine.analyse(board, chess.engine.Limit(depth=depth), multipv=2)
    win_before = get_line_win_percentage(info_before[0])
    cp_before = get_position_cp(info_before[0])
    positions_cp.append(cp_before)
    best_move = info_before[0]["pv"][0]
    if move == best_move:
        print("BEST MOVE")
    prev_board = board.copy()
    board.push(move)
    info_after = engine.analyse(board, chess.engine.Limit(depth=depth), multipv=2)
    win_after = get_line_win_percentage(info_after[0])
    accuracy = get_move_accuracy(win_before, win_after, player)
    actual_fen = board.fen().split(' ')[0]
    if (opening_name := openings.get(actual_fen)) is not None:
        print(f"OPENING: {opening_name}")
        # --- FALLBACK CLASSIFICATION ---
    if not is_forced and move != best_move and opening_name is None:
        move_class = basic_move_classification(win_before, win_after, player)
        print(move_class)
    if player == chess.WHITE:
        w_acc.append(accuracy)
    else:
        b_acc.append(accuracy)

engine.close()
w_weights = calc_weights(w_acc)
b_weights = calc_weights(b_acc)

white_accuracy = get_player_accuracy(w_acc, w_weights)
black_accuracy = get_player_accuracy(b_acc, b_weights)

print("White Accuracy:", white_accuracy)
print("Black Accuracy:", black_accuracy)

avg_cpl = get_players_average_cpl(positions_cp)
white_cpl = avg_cpl["whiteCpl"]
black_cpl = avg_cpl["blackCpl"]

# Supponiamo di avere i rating reali dei giocatori
white_rating_str = game.headers.get("WhiteElo")  # restituisce una stringa o None
black_rating_str = game.headers.get("BlackElo")
white_rating = int(white_rating_str) if white_rating_str else None
black_rating = int(black_rating_str) if black_rating_str else None

white_elo = get_elo_from_rating_and_cpl(white_cpl, white_rating or black_rating)
black_elo = get_elo_from_rating_and_cpl(black_cpl, black_rating or white_rating)

print("White estimated Elo:", white_elo)
print("Black estimated Elo:", black_elo)
