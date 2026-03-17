import chess
import math
import numpy as np


def get_player_accuracy(moves_accuracy, weights, player="white"):
    remainder = 0 if player == "white" else 1
    player_accs = [a for i, a in enumerate(moves_accuracy) if i % 2 == remainder]
    player_weights = [w for i, w in enumerate(weights) if i % 2 == remainder]

    w_mean = weighted_mean(player_accs, player_weights)
    h_mean = harmonic_mean(player_accs)
    return (w_mean + h_mean) / 2

def calc_weights(moves_acc):
    window_size = min(8, max(2, round(len(moves_acc)/10)))
    half_window = round(window_size / 2)

    weights = []
    for i in range(len(moves_acc)):
        start_idx = max(0, i - half_window)
        end_idx = min(len(moves_acc), i + half_window)
        window = moves_acc[start_idx:end_idx]
        std = np.std(window)
        weight = np.clip(std, 0.5, 12)
        weights.append(weight)
    return weights

def weighted_mean(values, weights):
    values = np.array(values)
    weights = np.array(weights)
    if len(values) == 0:
        return 0.0
    return np.sum(values * weights) / np.sum(weights)

def harmonic_mean(values):
    values = np.array(values)
    if len(values) == 0:
        return 0.0
    return len(values) / np.sum(1.0/np.maximum(values, 10))  # replica getHarmonicMean

def get_move_accuracy(last_wp: float, current_wp: float, turn: chess.Color) -> float:
    if turn == chess.WHITE:
        win_diff = max(0, last_wp - current_wp)
    else:
        win_diff = max(0, current_wp - last_wp)
    raw_accuracy = (103.1668100711649* math.exp(-0.04354415386753951 * win_diff)- 3.166924740191411)
    return min(100, max(0, raw_accuracy + 1))