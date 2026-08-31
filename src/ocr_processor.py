import cv2
import easyocr


_reader = None


def get_reader():
    global _reader

    if _reader is None:
        print("Loading EasyOCR model...")

        _reader = easyocr.Reader(
            ["en"],
            gpu=False,
            verbose=False
        )

    return _reader


def extract_text(image_path):
    image = cv2.imread(str(image_path))

    if image is None:
        raise ValueError(
            f"Unable to read image: {image_path}"
        )

    height, width = image.shape[:2]

    max_width = 1200

    if width > max_width:
        scale = max_width / width

        width = int(width * scale)
        height = int(height * scale)

        image = cv2.resize(
            image,
            (width, height),
            interpolation=cv2.INTER_AREA
        )

    reader = get_reader()

    results = reader.readtext(
        image,
        detail=1,
        paragraph=False
    )

    extracted_text = []

    for detection in results:
        bbox = detection[0]
        text = detection[1].strip()
        confidence = float(detection[2])

        if not text or confidence < 0.20:
            continue

        x_values = [
            point[0]
            for point in bbox
        ]

        y_values = [
            point[1]
            for point in bbox
        ]

        extracted_text.append({
            "text": text,
            "confidence": confidence,
            "x": int(min(x_values)),
            "y": int(min(y_values))
        })

    return extracted_text