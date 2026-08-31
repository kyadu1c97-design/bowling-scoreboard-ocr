import cv2
from scoreboard_grid import split_grid_cells


def preprocess_scoreboard(image):
    if image is None or image.size == 0:
        raise ValueError("Invalid scoreboard image provided.")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    scale = 2

    resized = cv2.resize(
        gray,
        None,
        fx=scale,
        fy=scale,
        interpolation=cv2.INTER_CUBIC
    )

    denoised = cv2.GaussianBlur(
        resized,
        (3, 3),
        0
    )

    enhanced = cv2.equalizeHist(denoised)

    processed = cv2.adaptiveThreshold(
        enhanced,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        11
    )

    return processed