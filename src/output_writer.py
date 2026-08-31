import csv
import json
from pathlib import Path


def save_json(data, output_path):
    output_path = Path(output_path)

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )


def save_csv(scoreboard, output_path):
    output_path = Path(output_path)

    with open(
        output_path,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "player",
            "ball_1",
            "ball_2",
            "ball_3",
            "ball_4",
            "ball_5",
            "ball_6",
            "ball_7",
            "ball_8",
            "ball_9",
            "ball_10",
            "ttl"
        ])

        for player, data in scoreboard.items():
            balls = data.get(
                "balls",
                [None] * 10
            )

            writer.writerow([
                player,
                *balls,
                data.get("ttl")
            ])