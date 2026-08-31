# Bowling Scoreboard OCR

An end-to-end Computer Vision and OCR pipeline for extracting bowling scoreboard information from video.

## Project Overview

This project processes a bowling video, extracts representative frames, detects the scoreboard region, preprocesses the scoreboard image, and prepares it for OCR-based information extraction.

The goal is to convert scoreboard information from an unstructured video into structured data such as:

* Runs
* Wickets
* Overs
* Other scoreboard fields

## Pipeline

```text
Bowling Video
      ↓
Video Frame Extraction
      ↓
Scoreboard Detection
      ↓
Image Preprocessing
      ↓
OCR
      ↓
Scoreboard Parsing
      ↓
Validation
      ↓
JSON / CSV
```

##  Project Structure

```text
bowling-scoreboard-ocr/
│
├── src/
│   ├── main.py
│   ├── video_processor.py
│   ├── scoreboard_detector.py
│   ├── image_preprocessor.py
│   ├── ocr_processor.py
│   ├── scoreboard_parser.py
│   └── utils.py
│
├── input/
│   └── bowling_scoreboard.mp4
│
├── output/
│   ├── frames/
│   ├── extracted_data.json
│   ├── extracted_data.csv
│   ├── detected_scoreboard.jpg
│   └── preprocessed_scoreboard.jpg
│
├── tests/
│   └── test_parser.py
│
├── docs/
│   └── screenshots/
│
├── requirements.txt
├── README.md
└── .gitignore
```

## Screenshots

### Input Video Frame

![Input Frame](docs/screenshots/input_frame.png)

### Scoreboard Detection

![Detected Scoreboard](docs/screenshots/detected_scoreboard.png)

### Image Preprocessing

![Preprocessed Scoreboard](docs/screenshots/preprocessed_scoreboard.png)

## Technologies

* Python
* OpenCV
* NumPy
* Pandas
* Pillow
* PaddleOCR
* PaddlePaddle
* Ultralytics YOLO

## Current Implementation

The current pipeline supports:

1. Loading the input video.
2. Reading video metadata.
3. Extracting representative frames.
4. Detecting an initial scoreboard region.
5. Preprocessing the scoreboard image for OCR.
6. Saving intermediate outputs for visual inspection.

### Video Processing

The system reads the video frame-by-frame instead of loading the complete video into memory.

Representative frames are extracted using configurable frame intervals.

Example:

```python
extract_frames(
    VIDEO_PATH,
    FRAME_OUTPUT_DIR,
    frame_interval=30
)
```

### Scoreboard Detection

The current implementation uses an initial region-based approach to identify the scoreboard area.

This component is designed to be replaceable with a more robust object-detection approach such as YOLO if required by the video characteristics.

### Image Preprocessing

The preprocessing stage currently performs:

* Grayscale conversion
* Image upscaling
* Gaussian denoising
* Otsu thresholding

The processed image is saved as:

```text
output/preprocessed_scoreboard.jpg
```

## Running the Project

### 1. Clone the repository

```bash
git clone https://github.com/kyadu1c97-design/bowling-scoreboard-ocr.git
cd bowling-scoreboard-ocr
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate on Windows:

```powershell
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add the input video

Place the bowling video at:

```text
input/bowling_scoreboard.mp4
```

### 5. Run the pipeline

```bash
python src/main.py
```

## Output

The current implementation generates intermediate processing results inside the `output/` directory.

Example:

```text
output/
├── frames/
├── detected_scoreboard.jpg
└── preprocessed_scoreboard.jpg
```

These files are used to verify frame extraction, scoreboard localization, and preprocessing quality.

## Development Roadmap

### Phase 1 — Video Processing

* [ ] Video loading
* [ ] Video metadata extraction
* [ ] Frame sampling

### Phase 2 — Scoreboard Detection

* [ ] Initial scoreboard region detection
* [ ] Robust scoreboard localization
* [ ] YOLO-based detection evaluation

### Phase 3 — OCR

* [ ] OCR integration
* [ ] OCR confidence handling
* [ ] Numeric text normalization

### Phase 4 — Scoreboard Parsing

* [ ] Runs extraction
* [ ] Wickets extraction
* [ ] Overs extraction
* [ ] Structured field mapping

### Phase 5 — Validation

* [ ] Invalid OCR detection
* [ ] Temporal consistency
* [ ] Score progression validation
* [ ] Confidence-based field selection

### Phase 6 — Final Output

* [ ] JSON generation
* [ ] CSV generation
* [ ] Final result validation
* [ ] Test coverage

## Engineering Considerations

The system is designed as a modular pipeline so that individual components can be improved independently.

For example:

```text
video_processor
       ↓
scoreboard_detector
       ↓
image_preprocessor
       ↓
ocr_processor
       ↓
scoreboard_parser
       ↓
validation
```

This makes the system easier to test, debug, and extend.

## Testing

Parser-specific tests are maintained in:

```text
tests/test_parser.py
```

Tests will be expanded as scoreboard parsing and validation logic are implemented.

## Limitations

The current scoreboard detector uses an initial region-based strategy and is not yet a fully trained object detector.

OCR and structured scoreboard parsing are currently under development.

## Future Improvements

Potential improvements include:

* YOLO-based scoreboard detection
* Multi-frame OCR aggregation
* OCR confidence scoring
* Temporal consistency checks
* Automatic correction of common OCR errors
* Better handling of changing scoreboard layouts
* Robust validation of scoreboard values

## Author

**kyadu1c97-design**

Repository:

https://github.com/kyadu1c97-design/bowling-scoreboard-ocr
