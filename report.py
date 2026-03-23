import pandas as pd
import json
from datetime import datetime

# --- Impostazioni ---
PLAYER = "rastone98"
INPUT_FILE = "rastone98.json"
OUTPUT_FILE = "Report_rastone98.md"

# --- Caricamento dataset ---
with open(INPUT_FILE) as f:
    games = json.load(f)

# --- Inizializza contatori ---
total_wins = total_draws = total_losses = 0
white_wins = white_draws = white_losses = 0
black_wins = black_draws = black_losses = 0
dates = []

# --- KPI mosse ---
move_types = ["Splendid", "Perfect", "Best", "Excellent", "Good",
              "Opening", "Inaccuracy", "Mistake", "Blunder", "Forced"]
# Dizionari per sommare le mosse totali e per colore
moves_total = {k: 0 for k in move_types}
moves_white = {k: 0 for k in move_types}
moves_black = {k: 0 for k in move_types}
moves_counts_total = moves_counts_white = moves_counts_black = 0  # contatore mosse totali

# --- Loop sulle partite ---
for g in games:
    if g["white"] == PLAYER:
        color = "white"
    elif g["black"] == PLAYER:
        color = "black"
    else:
        continue

    dates.append(datetime.strptime(g["date"], "%Y.%m.%d"))

    result = g["result"]
    # Totale risultati
    if (color == "white" and result == "1-0") or (color == "black" and result == "0-1"):
        total_wins += 1
        if color == "white":
            white_wins += 1
        else:
            black_wins += 1
    elif (color == "white" and result == "0-1") or (color == "black" and result == "1-0"):
        total_losses += 1
        if color == "white":
            white_losses += 1
        else:
            black_losses += 1
    elif result == "1/2-1/2":
        total_draws += 1
        if color == "white":
            white_draws += 1
        else:
            black_draws += 1

    # --- Conta mosse ---
    player_moves = []
    for i, m in enumerate(g["moves"], start=1):
        move_player = "white" if i % 2 != 0 else "black"
        if move_player == color:
            player_moves.append(m["classification"])

    moves_counts_total += len(player_moves)
    if color == "white":
        moves_counts_white += len(player_moves)
    else:
        moves_counts_black += len(player_moves)

    for mtype in move_types:
        moves_total[mtype] += sum(c == mtype for c in player_moves)
        if color == "white":
            moves_white[mtype] += sum(c == mtype for c in player_moves)
        else:
            moves_black[mtype] += sum(c == mtype for c in player_moves)

# --- Percentuali ---
def pct(n, total):
    return n / total * 100 if total > 0 else 0

# --- Periodo ---
period = f"{min(dates).strftime('%Y-%m-%d')} -> {max(dates).strftime('%Y-%m-%d')}" if dates else "N/A"

# --- Creazione Markdown ---
with open(OUTPUT_FILE, "w") as f:
    f.write(f"# Analisi Partite: {PLAYER}\n\n")
    f.write(f"- Numero di partite analizzate: {total_wins + total_draws + total_losses}\n")
    f.write(f"- Periodo di tempo: {period}\n\n")

    f.write("## Win Rate Totale e per colore\n\n")
    f.write("| Tipo | Win | Draw | Loss |\n")
    f.write("|------|-----|------|------|\n")
    f.write(f"| **Totale** | {total_wins} ({pct(total_wins,total_wins+total_draws+total_losses):.1f}%) | "
            f"{total_draws} ({pct(total_draws,total_wins+total_draws+total_losses):.1f}%) | "
            f"{total_losses} ({pct(total_losses,total_wins+total_draws+total_losses):.1f}%) |\n")
    f.write(f"| **Bianco** | {white_wins} ({pct(white_wins,white_wins+white_draws+white_losses):.1f}%) | "
            f"{white_draws} ({pct(white_draws,white_wins+white_draws+white_losses):.1f}%) | "
            f"{white_losses} ({pct(white_losses,white_wins+white_draws+white_losses):.1f}%) |\n")
    f.write(f"| **Nero** | {black_wins} ({pct(black_wins,black_wins+black_draws+black_losses):.1f}%) | "
            f"{black_draws} ({pct(black_draws,black_wins+black_draws+black_losses):.1f}%) | "
            f"{black_losses} ({pct(black_losses,black_wins+black_draws+black_losses):.1f}%) |\n\n")

    # --- Tabella mosse trasposta ---
    f.write("## Percentuali mosse per tipo (numero e % pesata per numero mosse del giocatore)\n\n")

    # Header: prima colonna vuota + tipi di mosse
    f.write("| Colore | " + " | ".join(move_types) + " |\n")
    f.write("|--------|" + "|".join(["------"] * len(move_types)) + "|\n")

    # Riga Totale
    f.write("| **Totale** | " + " | ".join(
        f"{moves_total[m]} ({pct(moves_total[m], moves_counts_total):.1f}%)" for m in move_types
    ) + " |\n")

    # Riga Bianco
    f.write("| **Bianco** | " + " | ".join(
        f"{moves_white[m]} ({pct(moves_white[m], moves_counts_white):.1f}%)" for m in move_types
    ) + " |\n")

    # Riga Nero
    f.write("| **Nero** | " + " | ".join(
        f"{moves_black[m]} ({pct(moves_black[m], moves_counts_black):.1f}%)" for m in move_types
    ) + " |\n")

print(f"Report generato: {OUTPUT_FILE}")