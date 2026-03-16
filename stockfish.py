import chess
import chess.engine
import chess.pgn

from utils.winPercentage import get_line_win_percentage
from utils.accuracy import get_move_accuracy


class StockfishWrapper:
    def __init__(self, engine_path: str, depth: int = 22, multipv: int = 2):
        self.engine = chess.engine.SimpleEngine.popen_uci(engine_path)
        self.depth = depth
        self.multipv = multipv

    def close(self):
        self.engine.quit()

engine = chess.engine.SimpleEngine.popen_uci("engine/stockfish_16_1")
depth = 22
with open("games/game.pgn") as f:
    game = chess.pgn.read_game(f)

board = game.board()

moves_win_percentage = []
deltas = []
w_acc = []
b_acc = []
for index, move in enumerate(game.mainline_moves()):
    player = board.turn
    info_before = engine.analyse(board, chess.engine.Limit(depth=depth), multipv=2)
    win_before = get_line_win_percentage(info_before[0], player)
    moves_win_percentage.append(win_before)
    board.push(move)
    info_after = engine.analyse(board, chess.engine.Limit(depth=depth), multipv=2)
    win_after = get_line_win_percentage(info_after[0], player)
    delta = win_after - win_before
    accuracy = get_move_accuracy(delta, player)
    if player == chess.WHITE:
        print(
            f"{(index // 2) + 1}. Before {win_before:.1f}, After {win_after:.1f}, Δ {delta:.1f}, acc {accuracy:.1f}",end=' ')
        w_acc.append(accuracy)
    else:
        print(
            f"Before {win_before:.1f}, After {win_after:.1f}, Δ {delta:.1f}, acc {accuracy:.1f}")
        b_acc.append(accuracy)

engine.close()