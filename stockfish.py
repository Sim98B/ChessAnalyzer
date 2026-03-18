import chess
import chess.engine
import chess.pgn
import json
import numpy as np

from utils.winPercentage import get_line_win_percentage
from utils.accuracy import get_move_accuracy, get_player_accuracy, calc_weights
from utils.estimateElo import get_position_cp, get_players_average_cpl, get_elo_from_rating_and_cpl
from utils.moveClassification import basic_move_classification, is_perfect_move, is_splendid_move

engine = chess.engine.SimpleEngine.popen_uci("engine/stockfish-windows-x86-64-avx2.exe")
depth = 22
pv = 2
#with open("games/game3.pgn") as f:
with open("games/1splendid1_4perfect0.pgn") as f:
    game = chess.pgn.read_game(f)

with open("openings_by_fen.json") as f:
    openings = json.load(f)

w_acc = []
b_acc = []
positions_cp = []
board = game.board()
prev_board = None
uci_moves = []
for index, move in enumerate(game.mainline_moves()):
    if board.is_checkmate():
        print("Checkmate")
        break
    elif board.is_stalemate():
        print("Stalemate")
        break

    uci_move = move.uci()
    print(f"White {move}" if board.turn else f"Black {move}")

    player = board.turn
    is_forced = len(list(board.legal_moves)) == 1

    info_before = engine.analyse(board, chess.engine.Limit(depth=depth), multipv=pv)
    win_before = get_line_win_percentage(info_before[0])
    cp_before = get_position_cp(info_before[0])
    positions_cp.append(cp_before)
    best_move = info_before[0]["pv"][0]

    prev_board = board.copy()
    board.push(move)

    info_after = engine.analyse(board, chess.engine.Limit(depth=depth), multipv=pv)
    win_after = get_line_win_percentage(info_after[0])
    accuracy = get_move_accuracy(win_before, win_after, player)

    last_position_alternative_line_win_percentage = None
    if len(info_before) > 1:
        last_position_alternative_line_win_percentage = get_line_win_percentage(info_before[1])

    fen_two_moves_ago = None
    prev_two_uci = None
    if len(uci_moves) >= 2:
        # FEN due mosse fa
        temp_board = game.board()
        for m in uci_moves[:-2]:
            temp_board.push(chess.Move.from_uci(m))
        fen_two_moves_ago = temp_board.fen()
        prev_two_uci = [uci_moves[-2], uci_moves[-1]]

    # --- INIZIALIZZO LA CLASSIFICAZIONE ---
    move_class = None

    # 1️⃣ Forced
    if is_forced:
        move_class = "FORCED"

    # 2️⃣ Opening
    actual_fen = board.fen().split(' ')[0]
    opening_name = openings.get(actual_fen)
    if move_class is None and opening_name is not None:
        move_class = f"OPENING: {opening_name}"

    # 3️⃣ Splendid
    fen_after_move = board.fen()
    print(last_position_alternative_line_win_percentage)
    if move_class is None and last_position_alternative_line_win_percentage is not None:
        if is_splendid_move(
                last_position_win_percentage=win_before,
                position_win_percentage=win_after,
                player=player,
                played_move=uci_move,
                best_line_pv_to_play=[m.uci() for m in info_before[0]["pv"][1:]],
                fen=prev_board.fen(),
                #fen = fen_after_move,
                last_position_alternative_line_win_percentage=last_position_alternative_line_win_percentage
        ):
            move_class = "SPLENDID"

    # 4️⃣ Perfect
    if move_class is None and last_position_alternative_line_win_percentage is not None:
        if is_perfect_move(
                last_position_win_percentage=win_before,
                position_win_percentage=win_after,
                player=player,
                last_position_alternative_line_win_percentage=last_position_alternative_line_win_percentage,
                fen_two_moves_ago=fen_two_moves_ago,
                uci_moves=prev_two_uci
        ):
            move_class = "PERFECT"

    # 5️⃣ Best move
    if move_class is None and move == best_move:
        move_class = "BEST"

    # 6️⃣ Fallback classification
    if move_class is None:
        move_class = basic_move_classification(win_before, win_after, player)

    print(move_class)

    if player == chess.WHITE:
        w_acc.append(accuracy)
    else:
        b_acc.append(accuracy)

    uci_moves.append(uci_move)

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
