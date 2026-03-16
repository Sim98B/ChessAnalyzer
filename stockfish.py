import chess
import chess.engine
import chess.pgn

from utils.winPercentage import (
    get_win_percentage_from_cp,
    get_win_percentage_from_mate,
    get_position_win_percentage,
    get_line_win_percentage
)


class StockfishWrapper:
    def __init__(self, engine_path: str, depth: int = 22, multipv: int = 2):
        self.engine = chess.engine.SimpleEngine.popen_uci(engine_path)
        self.depth = depth
        self.multipv = multipv

    """def analyze_position(self, board: chess.Board):
        info = self.engine.analyse(board, chess.engine.Limit(depth=self.depth), multipv=self.multipv)

        if self.multipv == 1:
            info = [info]

        lines = []

        for i, line in enumerate(info):
            score = line["score"].relative
            pv_moves = line.get("pv", [])
            pv_san = []
            tmp_board = board.copy()
            for move in pv_moves:
                pv_san.append(tmp_board.san(move))
                tmp_board.push(move)
            cp = None
            mate = None
            if score.is_cp():
                cp = score.score()
            elif score.is_mate():
                mate = score.mate()

            lines.append(
                LineEval(
                    pv=pv_san,
                    cp=cp,
                    mate=mate,
                    depth=self.depth,
                    multi_pv=i + 1
                )
            )
        return 0"""

    def close(self):
        self.engine.quit()

engine = chess.engine.SimpleEngine.popen_uci("engine/stockfish_16_1")
with open("games/game.pgn") as f:
    game = chess.pgn.read_game(f)

board = game.board()

for move in game.mainline_moves():
    player = board.turn
    info_before = engine.analyse(board, chess.engine.Limit(depth=22), multipv=2)
    win_before = get_line_win_percentage(info_before[0], player)
    board.push(move)
    info_after = engine.analyse(board, chess.engine.Limit(depth=22), multipv=2)
    win_after = get_line_win_percentage(info_after[0], player)
    delta = win_after - win_before
    print(f"Before {win_before:.3f}, After {win_after:.3f}, delta {delta:.3f}")

engine.close()