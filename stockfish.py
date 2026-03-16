import chess
import chess.engine
import chess.pgn
import numpy as np

from utils.winPercentage import get_line_win_percentage
from utils.accuracy import get_move_accuracy, get_player_accuracy, calc_weights


class StockfishWrapper:
    def __init__(self, engine_path: str, depth: int = 22, multipv: int = 2):
        self.engine = chess.engine.SimpleEngine.popen_uci(engine_path)
        self.depth = depth
        self.multipv = multipv

    def close(self):
        self.engine.quit()

engine = chess.engine.SimpleEngine.popen_uci("engine/stockfish_16_1")
depth = 22
with open("games/game2.pgn") as f:
    game = chess.pgn.read_game(f)

board = game.board()

moves_win_percentage = []
moves_accuracy = []
deltas = []
w_acc = []
b_acc = []

for index, move in enumerate(game.mainline_moves()):
    player = board.turn
    info_before = engine.analyse(board, chess.engine.Limit(depth=depth), multipv=2)
    win_before = get_line_win_percentage(info_before[0], player)
    moves_win_percentage.append(win_before)
    board.push(move)
    if board.is_checkmate():
        win_after = 100.0 if player == chess.WHITE else 0.0
        delta = win_after - win_before
        accuracy = get_move_accuracy(delta, player)
        if player == chess.WHITE:
            w_acc.append(accuracy)
        else:
            b_acc.append(accuracy)
        print(f"{(index//2)+1}. ({'B' if player==chess.WHITE else 'N'}) "
              f"Before {win_before:.1f}, After {win_after:.1f}, Δ {delta:.1f}, acc {accuracy:.1f}")
        print("Partita finita dopo questa mossa (checkmate)")
        break
    elif board.is_stalemate():
        win_after = 50.0  # patta
        delta = win_after - win_before
        accuracy = get_move_accuracy(delta, player)
        if player == chess.WHITE:
            w_acc.append(accuracy)
        else:
            b_acc.append(accuracy)
        print(f"{(index//2)+1}. "
              f"Before {win_before:.1f}, After {win_after:.1f}, Δ {delta:.1f}, acc {accuracy:.1f}")
        print("Partita finita dopo questa mossa (stalemate)")
        break
    info_after = engine.analyse(board, chess.engine.Limit(depth=depth), multipv=2)
    win_after = get_line_win_percentage(info_after[0], player)
    delta = win_after - win_before
    accuracy = get_move_accuracy(delta, player)
    moves_accuracy.append(accuracy)
    if player == chess.WHITE:
        w_acc.append(accuracy)
        print(f"{(index//2)+1}. Before {win_before:.1f}, After {win_after:.1f}, Δ {delta:.1f}", end=' ')
    else:
        b_acc.append(accuracy)
        print(f"Before {win_before:.1f}, After {win_after:.1f}, Δ {delta:.1f}, acc {accuracy:.1f}")

engine.close()

# calcolo pesi per bianco e nero separatamente
w_weights = calc_weights(w_acc)
b_weights = calc_weights(b_acc)

white_accuracy = get_player_accuracy(w_acc, w_weights)
black_accuracy = get_player_accuracy(b_acc, b_weights)

print("White Accuracy:", white_accuracy)
print("Black Accuracy:", black_accuracy)