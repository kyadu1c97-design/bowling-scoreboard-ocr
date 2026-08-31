import cv2


COLUMN_RANGES = {
    1: (0, 145),        # Player / row label
    2: (145, 290),      # Ball 1
    3: (290, 440),      # Ball 2
    4: (440, 590),      # Ball 3
    5: (590, 740),      # Ball 4
    6: (740, 890),      # Ball 5
    7: (890, 1040),     # Ball 6
    8: (1040, 1190),    # Ball 7
    9: (1190, 1340),    # Ball 8
    10: (1340, 1490),   # Ball 9
    11: (1490, 1640),   # Ball 10
    12: (1640, 1824),   # TTL
}


ROW_RANGES = {
    "header": (0, 65),

    "j_action": (65, 135),
    "j_total": (135, 195),

    "v_action": (195, 255),
    "v_total": (255, 315),

    "p_action": (315, 375),
    "p_total": (375, 435),

    "t_action": (435, 500),
    "t_total": (500, 560),
}


def extract_grid_regions(frame):
    if frame is None or frame.size == 0:
        raise ValueError("Invalid scoreboard frame.")

    height, width = frame.shape[:2]

    grid = frame[
        0:min(height, 826),
        0:min(width, 1824)
    ]

    if grid.size == 0:
        raise ValueError(
            "Unable to extract scoreboard grid."
        )

    return grid


def split_grid_cells(grid):
    if grid is None or grid.size == 0:
        raise ValueError(
            "Invalid scoreboard grid."
        )

    cells = []

    for row_name, (y1, y2) in ROW_RANGES.items():

        y1 = max(0, y1)
        y2 = min(grid.shape[0], y2)

        if y2 <= y1:
            continue

        for column, (x1, x2) in COLUMN_RANGES.items():

            x1 = max(0, x1)
            x2 = min(grid.shape[1], x2)

            if x2 <= x1:
                continue

            cell = grid[y1:y2, x1:x2]

            if cell.size == 0:
                continue

            cells.append({
                "row": row_name,
                "column": column,
                "image": cell,
                "x1": x1,
                "x2": x2,
                "y1": y1,
                "y2": y2,
            })

    return cells


def save_grid_cells(grid, output_dir):
    cells = split_grid_cells(grid)

    saved = 0

    for cell in cells:

        filename = (
            f"{cell['row']}_"
            f"col_{cell['column']:02d}.jpg"
        )

        path = (
            str(output_dir)
            + "/"
            + filename
        )

        if cv2.imwrite(
            path,
            cell["image"]
        ):
            saved += 1

    return saved