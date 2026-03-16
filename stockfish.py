import chess
import chess.engine

from classes.eval import LineEval, PositionEval


class StockfishWrapper:
    def __init__(self, engine_path: str, depth: int = 22, multipv: int = 1):
        self.engine = chess.engine.SimpleEngine.popen_uci(engine_path)
        self.depth = depth
        self.multipv = multipv

    def analyze_position(self, board: chess.Board) -> PositionEval:
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

        return PositionEval(lines=lines)

    def close(self):
        self.engine.quit()