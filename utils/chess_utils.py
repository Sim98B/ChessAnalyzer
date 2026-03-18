import chess
import chess.pgn

PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0  # il re normalmente non conta per materiale
}

def is_simple_piece_recapture(fen: str, uci_moves: list[str]) -> bool:
    """
    Controlla se le due mosse sono un semplice ricatturo sullo stesso quadrato.
    """
    board = chess.Board(fen)
    move1 = chess.Move.from_uci(uci_moves[0])
    move2 = chess.Move.from_uci(uci_moves[1])

    # se le due mosse non vanno nella stessa casella, non è recapture
    if move1.to_square != move2.to_square:
        return False

    # controlla se sulla casella finale c'è un pezzo (quello da catturare)
    piece = board.piece_at(move1.to_square)
    return piece is not None

def get_is_piece_sacrifice(fen: str, played_move: str, best_line_pv_to_play: list[str]) -> bool:
    """
    Determina se la mossa giocata è un sacrificio di pezzo rispetto alla linea migliore.
    """
    if not best_line_pv_to_play:
        return False

    board = chess.Board(fen)
    white_to_play = board.turn  # True se bianco

    # differenza materiale iniziale
    starting_material_diff = get_material_difference(fen)  # da implementare come nella tua versione JS

    moves = [played_move] + best_line_pv_to_play
    if len(moves) % 2 == 1:
        moves = moves[:-1]

    non_capturing_moves_temp = 1
    captured_pieces = {"w": [], "b": []}

    for uci in moves:
        move = chess.Move.from_uci(uci)
        if move not in board.legal_moves:
            return False  # errore mossa non legale
        captured_piece = board.piece_at(move.to_square)
        board.push(move)
        if captured_piece:
            captured_pieces["w" if captured_piece.color == chess.WHITE else "b"].append(captured_piece.symbol().lower())
            non_capturing_moves_temp = 1
        else:
            non_capturing_moves_temp -= 1
            if non_capturing_moves_temp < 0:
                break

    # rimuove pezzi catturati in pari
    for p in captured_pieces["w"][:]:
        if p in captured_pieces["b"]:
            captured_pieces["w"].remove(p)
            captured_pieces["b"].remove(p)

    # solo pedoni e numero bilanciato → non è sacrificio
    all_captured = captured_pieces["w"] + captured_pieces["b"]
    if abs(len(captured_pieces["w"]) - len(captured_pieces["b"])) <= 1 and all(p == "p" for p in all_captured):
        return False

    # differenza materiale finale
    ending_material_diff = get_material_difference(board.fen())
    material_diff = ending_material_diff - starting_material_diff
    material_diff_player_relative = material_diff if white_to_play else -material_diff

    return material_diff_player_relative < 0

def get_piece_value(piece_type: int) -> int:
    return PIECE_VALUES.get(piece_type, 0)

def get_material_difference(fen: str) -> int:
    board = chess.Board(fen)
    acc = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is None:
            continue
        value = get_piece_value(piece.piece_type)
        acc += value if piece.color == chess.WHITE else -value
    return acc