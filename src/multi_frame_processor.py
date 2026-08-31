from pathlib import Path

import cv2

from scoreboard_detector import detect_scoreboard
from scoreboard_grid import extract_grid_regions, split_grid_cells
from ocr_processor import extract_text


PLAYER_ROWS = [
    "j_action",
    "v_action",
    "p_action",
    "t_action",
]

BALL_COLUMNS = list(range(2, 12))
TTL_COLUMN = 12


def clean_value(text):
    if text is None:
        return ""

    text = str(text).strip().upper()

    replacements = {
        "—": "-",
        "–": "-",
        "_": "-",
        "|": "/",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text


def is_valid_value(text):
    text = clean_value(text)

    if not text:
        return False

    if text in {
        "NULL",
        "NONE",
        "TT",
        "TTL",
        "TtL",
    }:
        return False

    return True


def process_cell(cell, output_dir, frame_number):
    image = cell.get("image")

    if image is None or image.size == 0:
        return None

    output_dir = Path(output_dir)
    cell_dir = output_dir / "cells"

    cell_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    row = cell.get("row", "")
    column = int(cell.get("column", 0))

    filename = (
        f"frame_{frame_number:04d}_"
        f"{row}_col_{column:02d}.jpg"
    )

    cell_path = cell_dir / filename

    if not cv2.imwrite(
        str(cell_path),
        image
    ):
        return None

    try:
        results = extract_text(
            str(cell_path)
        )
    except Exception as exc:
        print(
            f"OCR failed for {filename}: {exc}"
        )
        return None

    if not results:
        return None

    valid_results = []

    for result in results:
        text = clean_value(
            result.get("text", "")
        )

        confidence = float(
            result.get("confidence", 0)
        )

        if not is_valid_value(text):
            continue

        valid_results.append({
            "text": text,
            "confidence": confidence
        })

    if not valid_results:
        return None

    best = max(
        valid_results,
        key=lambda item: item["confidence"]
    )

    return {
        "row": row,
        "column": column,
        "text": best["text"],
        "confidence": best["confidence"],
    }


def collect_frame_results(
    frames_dir,
    output_dir,
    max_frames=None
):
    frames_dir = Path(frames_dir)
    output_dir = Path(output_dir)

    frame_paths = sorted(
        frames_dir.glob("frame_*.jpg")
    )

    if max_frames is not None:
        frame_paths = frame_paths[:max_frames]

    if not frame_paths:
        raise FileNotFoundError(
            f"No frames found in: {frames_dir}"
        )

    results = []

    for frame_number, frame_path in enumerate(
        frame_paths,
        start=1
    ):
        print(
            f"\nProcessing frame "
            f"{frame_number}/{len(frame_paths)}: "
            f"{frame_path.name}"
        )

        frame = cv2.imread(
            str(frame_path)
        )

        if frame is None:
            print("Skipping unreadable frame.")
            continue

        try:
            scoreboard, bbox = detect_scoreboard(
                frame
            )

            if (
                scoreboard is None
                or scoreboard.size == 0
            ):
                print(
                    "Scoreboard detection failed."
                )
                continue

            grid = extract_grid_regions(
                scoreboard
            )

            if (
                grid is None
                or grid.size == 0
            ):
                print(
                    "Grid extraction failed."
                )
                continue

            all_cells = split_grid_cells(
                grid
            )

            selected_cells = [
                cell
                for cell in all_cells
                if (
                    cell.get("row") in PLAYER_ROWS
                    and (
                        cell.get("column") in BALL_COLUMNS
                        or cell.get("column") == TTL_COLUMN
                    )
                )
            ]

            frame_ocr = []

            for cell in selected_cells:
                result = process_cell(
                    cell,
                    output_dir,
                    frame_number
                )

                if result is not None:
                    frame_ocr.append(
                        result
                    )

            results.append({
                "frame": frame_path.name,
                "bbox": bbox,
                "ocr": frame_ocr,
            })

            print(
                f"Cell OCR results: "
                f"{len(frame_ocr)}"
            )

        except Exception as exc:
            print(
                f"Frame processing failed: "
                f"{frame_path.name}"
            )
            print(
                f"Reason: {exc}"
            )

    return results


def build_consensus(
    results,
    min_confidence=0.50,
    min_votes=2
):
    grouped = {}

    for result in results:

        for item in result.get(
            "ocr",
            []
        ):
            confidence = float(
                item.get(
                    "confidence",
                    0
                )
            )

            if confidence < min_confidence:
                continue

            row = item.get(
                "row",
                ""
            )

            column = int(
                item.get(
                    "column",
                    0
                )
            )

            text = clean_value(
                item.get(
                    "text",
                    ""
                )
            )

            if not is_valid_value(text):
                continue

            key = (
                row,
                column
            )

            if key not in grouped:
                grouped[key] = {}

            if text not in grouped[key]:
                grouped[key][text] = []

            grouped[key][text].append(
                confidence
            )

    consensus = []

    for (
        row,
        column
    ), text_options in grouped.items():

        if not text_options:
            continue

        best_text, scores = max(
            text_options.items(),
            key=lambda item: (
                len(item[1]),
                sum(item[1])
            )
        )

        votes = len(scores)

        if votes < min_votes:
            continue

        average_confidence = (
            sum(scores) / votes
        )

        consensus.append({
            "row": row,
            "column": column,
            "text": best_text,
            "votes": votes,
            "confidence": round(
                average_confidence,
                3
            ),
        })

    consensus.sort(
        key=lambda item: (
            PLAYER_ROWS.index(item["row"]),
            item["column"]
        )
    )

    return consensus


def build_scoreboard(consensus):
    scoreboard = {
        "J": {
            "balls": [None] * 10,
            "ttl": None,
        },
        "V": {
            "balls": [None] * 10,
            "ttl": None,
        },
        "P": {
            "balls": [None] * 10,
            "ttl": None,
        },
        "T": {
            "balls": [None] * 10,
            "ttl": None,
        },
    }

    row_to_player = {
        "j_action": "J",
        "v_action": "V",
        "p_action": "P",
        "t_action": "T",
    }

    for item in consensus:

        row = item.get("row", "")
        column = int(
            item.get("column", 0)
        )

        text = clean_value(
            item.get("text", "")
        )

        player = row_to_player.get(row)

        if player is None:
            continue

        if not is_valid_value(text):
            continue

        if 2 <= column <= 11:

            ball_index = column - 2

            scoreboard[player]["balls"][
                ball_index
            ] = text

        elif column == TTL_COLUMN:

            scoreboard[player]["ttl"] = text

    return scoreboard


def print_cell_diagnostics(results):
    print("\nCell OCR Diagnostics")
    print("-" * 40)

    if not results:
        print("No frame results available.")
        return

    for result in results:

        print(
            f"\nFrame: "
            f"{result.get('frame', 'unknown')}"
        )

        ocr_items = result.get(
            "ocr",
            []
        )

        if not ocr_items:
            print("  No valid cell OCR results.")
            continue

        for item in ocr_items:

            print(
                f"row={item.get('row', ''):<9} "
                f"col={int(item.get('column', 0)):02d} "
                f"text={item.get('text', ''):<12} "
                f"confidence="
                f"{float(item.get('confidence', 0)):.2f}"
            )