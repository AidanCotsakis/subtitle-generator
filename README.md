# Video Subtitle Generator

This project automates subtitle creation for video files, providing tools for audio extraction, transcription, and synchronized subtitle rendering. Using Python, the project integrates with Vosk for speech recognition, Pygame for live rendering, and MoviePy for final subtitle video production.

## Key Features

- **Audio Extraction**: Extracts audio from video files (e.g., `.mp4`, `.mkv`) and saves as `.wav` for processing.
- **Speech Recognition**: Transcribes audio into text with Vosk, providing word-level timestamps and confidence scores.
- **Real-Time Subtitle Rendering**: Uses Pygame to display subtitles, with live playback and on-screen editing.
- **Subtitle Video Generation**: Creates a video with embedded subtitles, allowing customizable text styles and animations.

## Setup

### Prerequisites

- **Python 3.8+**
- **Required Libraries**: Install dependencies using the following:
  ```bash
  pip install moviepy vosk pygame pydub pillow
  ```
- **Vosk Model**: Download a Vosk model ([vosk-model-en-us-0.42-gigaspeech](https://alphacephei.com/vosk/models)) and save it in the ```models/``` directory.

### Installation
- **Clone this repository**
- **Place audio file** in the output directory or select upon running ```audioExtract.py```.

## **Usage**
- **Audio Extraction**: Run ```audioExtract.py``` to extract audio from a video file:
    ```bash
    python audioExtract.py
    ```
    The extracted audio will be saved as ```output/audio.wav```.

- **Generate Subtitles**: Run ```subtitles1.py``` to transcribe the audio and output word timestamps:
    ```bash
    python subtitles1.py
    ```
- **Edit Subtitles**: Use ```subtitles2.py``` to display and edit subtitles in real-time:
    ```bash
    python subtitles2.py
    ```

- **Generate Subtitle Video**: Finally, run ```subtitles3.py``` to create the final video with embedded subtitles:
    ```bash
    python subtitles3.py
    ```
    The output will be saved as ```output/subtitles.mp4```.

## **Project Structure**
- **audioExtract.py**: Extracts audio from video files.
- **subtitles1.py**: Uses Vosk to transcribe audio and generate timestamps.
- **subtitles2.py**: Renders subtitles in real-time with Pygame, allowing edits.
- **subtitles3.py**: Creates the final video with embedded, animated subtitles.
- **subtitlesHelper.py**: Provides utility functions and classes for managing text boxes in ```subtitles2.py```.

## **Customization**
- **Subtitle Styling**: Modify font path, color, and size in subtitles2.py and subtitles3.py for custom appearances.
- **Frame Rate**: Adjust fps in subtitles1.py, subtitles2.py, and subtitles3.py to control subtitle timing.
