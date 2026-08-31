import cv2


def detect_scoreboard(frame):
    if frame is None:
        raise ValueError("Invalid frame provided.")

    height, width = frame.shape[:2]

    roi_height = int(height * 0.90)

    scoreboard = frame[:roi_height, :]

    if scoreboard.size == 0:
        raise ValueError("Unable to extract scoreboard region.")

    bbox = (0, 0, width, roi_height)

    return scoreboard, bbox