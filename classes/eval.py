from dataclasses import dataclass
from typing import Optional, List

@dataclass
class LineEval:
    pv: List[str]
    cp: Optional[int] = None
    mate: Optional[int] = None
    depth: int = 0
    multi_pv: int = 1

@dataclass
class PositionEval:
    best_move: Optional[str] = None
    move_classification: Optional[str] = None
    opening: Optional[str] = None
    lines: List[LineEval] = None

@dataclass
class Accuracy:
    white: int
    black: int