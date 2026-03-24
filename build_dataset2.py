import pandas as pd
import json

PLAYER = "rastone98"

with open("rastone98.json") as f:
    games = json.load(f)

# --- Dataset delle partite ---
games_records = []

# --- Dataset delle mosse ---
moves_records = []

for g in games:
    # determina il colore del player e rating/accuracy
    if g["white"] == PLAYER:
        player_color = "white"
        player_accuracy = g.get("white_accuracy", 0)
        player_rating = g.get("white_rating", 0)
    elif g["black"] == PLAYER:
        player_color = "black"
        player_accuracy = g.get("black_accuracy", 0)
        player_rating = g.get("black_rating", 0)
    else:
        continue

    # conteggio mosse per classificazione (totale, senza distinguere fase)
    counts_total = {k.lower(): 0 for k in ["Splendid", "Perfect", "Best", "Excellent",
                                           "Good", "Opening", "Inaccuracy", "Mistake",
                                           "Blunder", "Forced"]}
    num_moves = 0

    for i, m in enumerate(g["moves"], start=1):
        move_player = "white" if i % 2 != 0 else "black"
        if move_player != player_color:
            continue

        num_moves += 1
        classification = m.get("classification", "Unknown")
        counts_total[classification.lower()] = counts_total.get(classification.lower(), 0) + 1

        # aggiungi riga per moves dataset
        moves_records.append({
            "game_id": g["game_id"],
            "move_number": i,
            "phase": m.get("phase", "unknown").lower(),
            "classification": classification,
            "time_spent": m.get("time_spent"),
            "san": m.get("san")
        })

    # aggiungi riga per games dataset
    record = {
        "game_id": g["game_id"],
        "white": g["white"],
        "black": g["black"],
        "rating": player_rating,
        "accuracy": player_accuracy,
        "result": g.get("result"),
        "opening_name": g.get("opening"),
        "engine": g.get("engine"),
        "depth": g.get("depth"),
        "pv": g.get("pv"),
        "date": g.get("date"),
        "num_moves": num_moves,
    }
    record.update(counts_total)
    games_records.append(record)

# crea dataframe
games_df = pd.DataFrame(games_records)
moves_df = pd.DataFrame(moves_records)

# salva su file parquet
games_df.to_parquet("games_dataset.parquet", index=False)
moves_df.to_parquet("moves_dataset.parquet", index=False)

print("Dataset completo salvato:")
print("Partite:")
print(games_df.head())
print("\nMosse:")
print(moves_df.head())