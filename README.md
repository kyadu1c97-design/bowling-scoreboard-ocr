# Bowling Scoreboard Extraction System

A computer vision and OCR based system for extracting scoreboard information from a bowling video.

The project processes a video, extracts frames, detects the scoreboard region, prepares the image for OCR, performs text recognition, applies multi-frame cell consensus, and exports the extracted information in JSON and CSV formats.

## Features

- Video metadata extraction
- Frame extraction using OpenCV
- Scoreboard region detection
- Scoreboard grid extraction
- Grid cell segmentation
- Image preprocessing for OCR
- EasyOCR based text recognition
- Multi-frame OCR processing
- Confidence-based filtering
- Spatial and cell-level consensus
- Structured scoreboard generation
- JSON output
- CSV output

## Project Structure

```text
scoreboard-extraction/
│
├── input/
│   └── bowling_scoreboard.mp4
│
├── output/
│   ├── frames/
│   ├── cells/
│   ├── grid_cells/
│   ├── detected_scoreboard.jpg
│   ├── scoreboard_grid.jpg
│   ├── preprocessed_scoreboard.jpg
│   ├── extracted_data.json
│   └── extracted_data.csv
│
├── src/
│   ├── main.py
│   ├── video_processor.py
│   ├── scoreboard_detector.py
│   ├── scoreboard_grid.py
│   ├── image_preprocessor.py
│   ├── ocr_processor.py
│   ├── scoreboard_parser.py
│   ├── multi_frame_processor.py
│   └── output_writer.py
│
├── requirements.txt
└── README.md

## Processing Pipeline

Input Video
     |
     v
Video Information
     |
     v
Frame Extraction
     |
     v
Scoreboard Detection
     |
     v
Scoreboard Grid Extraction
     |
     v
Grid Cell Segmentation
     |
     v
Image Preprocessing
     |
     v
EasyOCR
     |
     v
Multi-Frame Consensus
     |
     v
Scoreboard Parser
     |
     v
JSON / CSV Output

Technologies Used
Python
OpenCV
EasyOCR
PyTorch
NumPy
Pillow
Requirements

Python 3.9 or newer is recommended.

Install the required packages using:

pip install -r requirements.txt
Input

Place the input video inside the input directory:

input/bowling_scoreboard.mp4

The current test video contains:

FPS: 30
Resolution: 1920 × 1080
Total frames: 1735
Duration: approximately 57.83 seconds
How to Run

Activate the virtual environment:

Windows PowerShell
.\venv\Scripts\Activate.ps1

Run the application:

python src/main.py
Output

The application generates intermediate and final files inside the output directory.

Detected Scoreboard
output/detected_scoreboard.jpg

Contains the detected scoreboard region.

Scoreboard Grid
output/scoreboard_grid.jpg

Contains the extracted scoreboard table/grid.

Preprocessed Image
output/preprocessed_scoreboard.jpg

Contains the image prepared for OCR.

Extracted JSON
output/extracted_data.json

Stores structured extraction results including:

Video information
Detected players
OCR text
Multi-frame consensus
Scoreboard data
Extracted CSV
output/extracted_data.csv

Stores scoreboard information in tabular format.

OCR

EasyOCR is used for text recognition.

The OCR pipeline:

Reads the preprocessed image.
Detects text regions.
Extracts text.
Calculates confidence values.
Stores the text position and confidence.
Filters low-confidence detections.

The system runs on CPU when GPU acceleration is unavailable.

Multi-Frame Processing

Instead of relying on only one frame, the project processes multiple sampled frames.

The current testing configuration uses a small number of frames to reduce CPU processing time during development.

Repeated OCR results are grouped using:

Scoreboard row
Scoreboard column
OCR confidence
Text voting

This helps identify values that remain consistent across multiple frames.

Scoreboard Grid

The scoreboard is divided into multiple rows and columns.

The current logical structure is:

Player | Ball 1 | Ball 2 | Ball 3 | ... | Ball 10 | TTL

The grid is segmented before cell-level OCR is performed.

Configuration

Important settings are available in src/main.py.

Example:

FRAME_INTERVAL = 30
TEST_FRAME_LIMIT = 2

FRAME_INTERVAL controls how frequently frames are sampled from the video.

TEST_FRAME_LIMIT controls how many extracted frames are processed during testing.

For a full processing run, the test frame limit can be increased after validating the pipeline.

Error Handling

The application checks for:

Missing input video
Invalid video files
Failed frame extraction
Invalid image data
Failed scoreboard detection
Failed grid extraction
OCR failures
Invalid output files

Errors are reported in the terminal.

Current Limitations

The project successfully implements the complete video-to-OCR processing pipeline.

However, scoreboard cell-level recognition can be affected by:

Small text size
Image resolution
OCR character confusion
Scoreboard cell alignment
Combined characters in some cells
Partial or low-confidence detections

For this reason, some scoreboard values may be missing or incorrectly recognized in the current prototype.

The system therefore preserves raw OCR results and confidence information along with the structured output.

Future Improvements

Possible future improvements include:

YOLO based automatic scoreboard detection
Better perspective correction
Automatic grid-line detection
More advanced cell segmentation
OCR ensemble using multiple OCR engines
GPU acceleration
Temporal tracking of scoreboard cells
Improved player-name recognition
Automatic validation of score totals
Higher accuracy JSON/CSV extraction
Automated test coverage
Example Terminal Output
BOWLING SCOREBOARD EXTRACTION SYSTEM

Video Information
FPS          : 30.00
Total Frames : 1735
Resolution   : 1920 x 1080
Duration     : 57.83 seconds

Frame Extraction
Frames saved : 58

Scoreboard Detection
Bounding Box : (0, 0, 1920, 972)

Scoreboard Grid
Grid cells   : 108

Single-Frame OCR
Loading EasyOCR model...

Multi-Frame Cell Processing
Successfully processed test frames.

Multi-Frame Cell Consensus
...

Pipeline completed successfully.
Project Status

The current implementation successfully demonstrates:

Video processing
Frame extraction
Scoreboard region extraction
Grid segmentation
OCR integration
Multi-frame processing
Confidence filtering
Consensus generation
Structured JSON/CSV export

The main remaining area for improvement is the accuracy of individual scoreboard cell recognition.

Author

Bowling Scoreboard Extraction System

License

This project is intended for educational and project demonstration purposes.


Save karne ke liye PowerShell:

```powershell
code README.md

