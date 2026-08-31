import re


ROW_TOLERANCE = 45
MIN_CONFIDENCE = 0.50


def clean_text(text):
    if not text:
        return ""

    text = str(text).strip()
    text = re.sub(r"\s+", " ", text)

    return text


def normalize_text(text):
    return clean_text(text).upper()


def is_valid_detection(item):
    if not isinstance(item, dict):
        return False

    text = clean_text(item.get("text", ""))
    confidence = float(item.get("confidence", 0))

    return bool(text) and confidence >= MIN_CONFIDENCE


def group_into_rows(ocr_data):
    rows = []

    detections = [
        item
        for item in ocr_data
        if is_valid_detection(item)
    ]

    detections.sort(
        key=lambda item: (
            int(item.get("y", 0)),
            int(item.get("x", 0))
        )
    )

    for item in detections:
        x = int(item.get("x", 0))
        y = int(item.get("y", 0))

        matched_row = None

        for row in rows:
            if abs(row["y"] - y) <= ROW_TOLERANCE:
                matched_row = row
                break

        if matched_row is None:
            matched_row = {
                "y": y,
                "items": []
            }

            rows.append(matched_row)

        matched_row["items"].append({
            "text": normalize_text(item["text"]),
            "x": x,
            "y": y,
            "confidence": float(
                item.get("confidence", 0)
            )
        })

    for row in rows:
        row["items"].sort(
            key=lambda item: item["x"]
        )

    rows.sort(
        key=lambda row: row["y"]
    )

    return rows


def is_probable_name(text):
    if not text:
        return False

    if not re.search(r"[A-Z]", text):
        return False

    if re.fullmatch(r"[XVTPLMJ]+", text):
        return False

    if re.search(r"\d", text):
        return False

    return 2 <= len(text) <= 20


def parse_scoreboard(ocr_data):
    if not ocr_data:
        return {
            "players": [],
            "rows": [],
            "raw_text": []
        }

    rows = group_into_rows(
        ocr_data
    )

    players = []

    for row in rows:
        for item in row["items"]:

            text = item["text"]

            if (
                item["y"] <= 80
                and is_probable_name(text)
            ):
                players.append({
                    "player": text,
                    "x": item["x"],
                    "y": item["y"],
                    "confidence": item["confidence"]
                })

    parsed_rows = []

    for row in rows:

        cells = []

        for item in row["items"]:
            cells.append({
                "text": item["text"],
                "x": item["x"],
                "y": item["y"],
                "confidence": item["confidence"]
            })

        parsed_rows.append({
            "y": row["y"],
            "cells": cells
        })

    raw_text = [
        clean_text(item.get("text", ""))
        for item in ocr_data
        if clean_text(item.get("text", ""))
    ]

    return {
        "players": players,
        "rows": parsed_rows,
        "raw_text": raw_text
    }