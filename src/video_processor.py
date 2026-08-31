import cv2
from pathlib import Path


def get_video_info(video_path):
    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        raise ValueError(f"Unable to open video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    duration = total_frames / fps if fps > 0 else 0

    cap.release()

    return {
        "fps": fps,
        "total_frames": total_frames,
        "width": width,
        "height": height,
        "duration": duration,
    }


def extract_frames(video_path, output_dir, frame_interval=30):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if frame_interval <= 0:
        raise ValueError("frame_interval must be greater than 0.")

    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        raise ValueError(f"Unable to open video: {video_path}")

    frame_count = 0
    saved_count = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        if frame_count % frame_interval == 0:
            frame_path = output_dir / f"frame_{saved_count:04d}.jpg"

            if not cv2.imwrite(str(frame_path), frame):
                cap.release()
                raise IOError(f"Failed to save frame: {frame_path}")

            saved_count += 1

        frame_count += 1

    cap.release()

    return saved_count