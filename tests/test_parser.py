import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.scoreboard_parser import parse_scoreboard


def test_parse_scoreboard_tracks_frame_totals():
    sample = [
        "9 0",
        "5 5",
        "7 /",
        "X",
        "8 2",
        "0 /",
        "X",
        "X",
        "9 /",
        "X 1",
    ]

    scoreboard = parse_scoreboard(sample)

    assert scoreboard["total"] == 157
    assert scoreboard["frames"][0]["cumulative_total"] == 9
    assert scoreboard["frames"][1]["cumulative_total"] == 19
    assert scoreboard["frames"][2]["cumulative_total"] == 36
    assert scoreboard["frames"][3]["cumulative_total"] == 54
    assert scoreboard["frames"][4]["cumulative_total"] == 64
    assert scoreboard["frames"][5]["cumulative_total"] == 74
    assert scoreboard["frames"][6]["cumulative_total"] == 94
    assert scoreboard["frames"][7]["cumulative_total"] == 114
    assert scoreboard["frames"][8]["cumulative_total"] == 133
    assert scoreboard["frames"][9]["cumulative_total"] == 157
