import pandas as pd
import json

PLAYER = "rastone98"

with open("rastone98.json") as f:
    games = json.load(f)

records = []

for g in games:

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

    player_moves = []
    for i, m in enumerate(g["moves"], start=1):
        move_player = "white" if i % 2 != 0 else "black"
        if move_player == player_color:
            player_moves.append(m["classification"])

    num_moves = len(player_moves)

    records.append({
        "game_id": g["game_id"],
        "num_moves": num_moves,
        "accuracy": player_accuracy,
        "rating": player_rating,
        "splendid": sum(c == "Splendid" for c in player_moves),
        "perfect": sum(c == "Perfect" for c in player_moves),
        "best": sum(c == "Best" for c in player_moves),
        "excellent": sum(c == "Excellent" for c in player_moves),
        "good": sum(c == "Good" for c in player_moves),
        "opening": sum(c == "Opening" for c in player_moves),
        "inaccuracy": sum(c == "Inaccuracy" for c in player_moves),
        "mistakes": sum(c == "Mistake" for c in player_moves),
        "blunders": sum(c == "Blunder" for c in player_moves),
        "forced": sum(c == "Forced" for c in player_moves),
    })

games_df = pd.DataFrame(records)

# salva dataset
games_df.to_parquet("games_dataset.parquet", index=False)

print("Dataset salvato.")
print(games_df.head())