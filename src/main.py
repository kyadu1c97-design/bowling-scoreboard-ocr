from pathlib import Path

import cv2

from video_processor import get_video_info, extract_frames
from scoreboard_detector import detect_scoreboard
from image_preprocessor import preprocess_scoreboard
from ocr_processor import extract_text
from scoreboard_parser import parse_scoreboard
from multi_frame_processor import (
    collect_frame_results,
    build_consensus,
    print_cell_diagnostics,
    build_scoreboard,
)
from scoreboard_grid import (
    extract_grid_regions,
    save_grid_cells,
)
from output_writer import save_json, save_csv


BASE_DIR = Path(__file__).resolve().parent.parent

VIDEO_PATH = BASE_DIR / "input" / "bowling_scoreboard.mp4"

OUTPUT_DIR = BASE_DIR / "output"
FRAME_OUTPUT_DIR = OUTPUT_DIR / "frames"
GRID_CELLS_DIR = OUTPUT_DIR / "grid_cells"

SCOREBOARD_OUTPUT = OUTPUT_DIR / "detected_scoreboard.jpg"
GRID_OUTPUT = OUTPUT_DIR / "scoreboard_grid.jpg"
PREPROCESSED_OUTPUT = OUTPUT_DIR / "preprocessed_scoreboard.jpg"

JSON_OUTPUT = OUTPUT_DIR / "extracted_data.json"
CSV_OUTPUT = OUTPUT_DIR / "extracted_data.csv"

FRAME_INTERVAL = 30
TEST_FRAME_LIMIT = 2


def setup_directories():
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    FRAME_OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    GRID_CELLS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


def validate_video():
    if not VIDEO_PATH.exists():
        raise FileNotFoundError(
            f"Input video not found: {VIDEO_PATH}"
        )


def save_image(image, output_path):
    if image is None or image.size == 0:
        raise ValueError(
            "Cannot save an empty image."
        )

    if not cv2.imwrite(
        str(output_path),
        image
    ):
        raise IOError(
            f"Failed to save image: {output_path}"
        )


def print_ocr_results(ocr_results):
    print("\nOCR Result")
    print("-" * 40)

    if not ocr_results:
        print("No text detected.")
        return

    for index, item in enumerate(
        ocr_results,
        start=1
    ):
        text = item.get(
            "text",
            ""
        )

        x = item.get(
            "x",
            0
        )

        y = item.get(
            "y",
            0
        )

        confidence = float(
            item.get(
                "confidence",
                0
            )
        )

        print(
            f"{index:02d}. "
            f"{text} "
            f"(x={x}, "
            f"y={y}, "
            f"confidence="
            f"{confidence:.2f})"
        )


def print_parsed_scoreboard(parsed_data):
    print("\nParsed Scoreboard")
    print("-" * 40)

    if not isinstance(
        parsed_data,
        dict
    ):
        print(parsed_data)
        return

    players = parsed_data.get(
        "players",
        []
    )

    if players:
        print("Players")

        for index, player in enumerate(
            players,
            start=1
        ):
            name = player.get(
                "player",
                "Unknown"
            )

            x = player.get("x")
            y = player.get("y")
            confidence = player.get(
                "confidence"
            )

            if (
                x is not None
                and y is not None
            ):
                print(
                    f"{index:02d}. "
                    f"Player: {name} "
                    f"(x={x}, y={y})"
                )
            elif y is not None:
                print(
                    f"{index:02d}. "
                    f"Player: {name} "
                    f"(y={y})"
                )
            else:
                print(
                    f"{index:02d}. "
                    f"Player: {name}"
                )

            if confidence is not None:
                print(
                    f"    confidence="
                    f"{float(confidence):.2f}"
                )

    else:
        print("No player names detected.")

    rows = parsed_data.get(
        "rows",
        []
    )

    if rows:
        print("\nDetected Rows")
        print("-" * 40)

        for index, row in enumerate(
            rows,
            start=1
        ):
            cells = row.get(
                "cells",
                []
            )

            row_text = " | ".join(
                cell.get("text", "")
                for cell in cells
            )

            print(
                f"Row {index:02d} "
                f"(y={row.get('y', 0)}): "
                f"{row_text}"
            )

    raw_text = parsed_data.get(
        "raw_text",
        []
    )

    if raw_text:
        print("\nRaw OCR Text")
        print("-" * 40)

        for index, text in enumerate(
            raw_text,
            start=1
        ):
            print(
                f"{index:02d}. "
                f"{text}"
            )


def print_consensus(consensus):
    print("\nMulti-Frame Cell Consensus")
    print("-" * 40)

    if not consensus:
        print(
            "No reliable cell values found."
        )
        return

    for index, item in enumerate(
        consensus,
        start=1
    ):
        print(
            f"{index:02d}. "
            f"row={item.get('row', '')}, "
            f"column={item.get('column', 0)}, "
            f"text={item.get('text', '')}, "
            f"votes={item.get('votes', 0)}, "
            f"confidence="
            f"{float(item.get('confidence', 0)):.2f}"
        )


def print_final_scoreboard(scoreboard):
    print("\nFinal Scoreboard")
    print("-" * 40)

    if not scoreboard:
        print(
            "No structured scoreboard data found."
        )
        return

    for player, data in scoreboard.items():
        print(
            f"\nPlayer: {player}"
        )

        print(
            f"Balls : "
            f"{data.get('balls', [])}"
        )

        print(
            f"TTL   : "
            f"{data.get('ttl')}"
        )


def main():
    print("=" * 60)
    print(
        "       BOWLING SCOREBOARD "
        "EXTRACTION SYSTEM"
    )
    print("=" * 60)

    setup_directories()
    validate_video()

    print("\nVideo Information")
    print("-" * 40)

    video_info = get_video_info(
        str(VIDEO_PATH)
    )

    print(
        f"FPS          : "
        f"{video_info['fps']:.2f}"
    )

    print(
        f"Total Frames : "
        f"{video_info['total_frames']}"
    )

    print(
        f"Resolution   : "
        f"{video_info['width']} x "
        f"{video_info['height']}"
    )

    print(
        f"Duration     : "
        f"{video_info['duration']:.2f} seconds"
    )

    print("\nFrame Extraction")
    print("-" * 40)

    saved_frames = extract_frames(
        str(VIDEO_PATH),
        str(FRAME_OUTPUT_DIR),
        frame_interval=FRAME_INTERVAL,
    )

    print(
        f"Frames saved : "
        f"{saved_frames}"
    )

    if saved_frames == 0:
        raise RuntimeError(
            "No frames were extracted."
        )

    first_frame_path = (
        FRAME_OUTPUT_DIR /
        "frame_0000.jpg"
    )

    if not first_frame_path.exists():
        raise FileNotFoundError(
            f"First frame not found: "
            f"{first_frame_path}"
        )

    frame = cv2.imread(
        str(first_frame_path)
    )

    if frame is None:
        raise ValueError(
            "Unable to read the first extracted frame."
        )

    print("\nScoreboard Detection")
    print("-" * 40)

    scoreboard, bbox = detect_scoreboard(
        frame
    )

    if (
        scoreboard is None
        or scoreboard.size == 0
    ):
        raise RuntimeError(
            "Scoreboard detection failed."
        )

    save_image(
        scoreboard,
        SCOREBOARD_OUTPUT
    )

    print(
        f"Bounding Box : {bbox}"
    )

    print(
        f"Saved        : "
        f"{SCOREBOARD_OUTPUT}"
    )

    print("\nScoreboard Grid")
    print("-" * 40)

    grid = extract_grid_regions(
        scoreboard
    )

    if (
        grid is None
        or grid.size == 0
    ):
        raise RuntimeError(
            "Scoreboard grid extraction failed."
        )

    save_image(
        grid,
        GRID_OUTPUT
    )

    print(
        f"Grid saved   : "
        f"{GRID_OUTPUT}"
    )

    cell_count = save_grid_cells(
        grid,
        GRID_CELLS_DIR
    )

    print(
        f"Grid cells   : "
        f"{cell_count}"
    )

    print(
        f"Cell folder  : "
        f"{GRID_CELLS_DIR}"
    )

    print("\nImage Preprocessing")
    print("-" * 40)

    processed_scoreboard = preprocess_scoreboard(
        scoreboard
    )

    if (
        processed_scoreboard is None
        or processed_scoreboard.size == 0
    ):
        raise RuntimeError(
            "Image preprocessing failed."
        )

    save_image(
        processed_scoreboard,
        PREPROCESSED_OUTPUT
    )

    print(
        f"Saved        : "
        f"{PREPROCESSED_OUTPUT}"
    )

    print("\nSingle-Frame OCR")
    print("-" * 40)

    ocr_text = extract_text(
        str(PREPROCESSED_OUTPUT)
    )

    print_ocr_results(
        ocr_text
    )

    parsed_data = parse_scoreboard(
        ocr_text
    )

    print_parsed_scoreboard(
        parsed_data
    )

    print("\nMulti-Frame Cell Processing")
    print("-" * 40)

    multi_frame_results = (
        collect_frame_results(
            FRAME_OUTPUT_DIR,
            OUTPUT_DIR,
            max_frames=TEST_FRAME_LIMIT,
        )
    )

    print(
        f"\nSuccessfully processed "
        f"{len(multi_frame_results)} "
        f"of {TEST_FRAME_LIMIT} "
        f"test frames."
    )

    print_cell_diagnostics(
        multi_frame_results
    )

    consensus = build_consensus(
        multi_frame_results
    )

    print_consensus(
        consensus
    )

    scoreboard_data = build_scoreboard(
        consensus
    )

    print_final_scoreboard(
        scoreboard_data
    )

    final_data = {
        "video": VIDEO_PATH.name,
        "fps": video_info["fps"],
        "total_frames": video_info["total_frames"],
        "resolution": {
            "width": video_info["width"],
            "height": video_info["height"],
        },
        "duration_seconds": round(
            video_info["duration"],
            2
        ),
        "frames_sampled": saved_frames,
        "test_frames_processed": len(
            multi_frame_results
        ),
        "scoreboard": scoreboard_data,
        "players_detected": parsed_data.get(
            "players",
            []
        ),
        "raw_ocr": parsed_data.get(
            "raw_text",
            []
        ),
        "consensus": consensus,
    }

    save_json(
        final_data,
        JSON_OUTPUT
    )

    save_csv(
        scoreboard_data,
        CSV_OUTPUT
    )

    print("\nOutput Files")
    print("-" * 40)

    print(
        f"JSON : "
        f"{JSON_OUTPUT}"
    )

    print(
        f"CSV  : "
        f"{CSV_OUTPUT}"
    )

    print("\n" + "=" * 60)
    print(
        "Pipeline completed successfully."
    )
    print("=" * 60)


if __name__ == "__main__":
    main()