# TikTok Captions

Add TikTok-style captions to your videos automatically using OpenAI's Whisper for transcription.

## Preview

<img src="https://i.imgur.com/nfldFkh.gif" alt="captions preview" height="300">

## Installation

```bash
pip install tiktokcaptions
```

## Usage

```python
from tiktokcaptions import add_captions_to_videofile

# whisper transcription (dict)
transcription = openai.audio.transcription.create(
    model="whisper-1",
    file=file,
    timestamp_granularities=["segment", "word"],
    response_format="verbose_json",
)
transcription = transcription.model_dump()

# Basic usage
add_captions_to_videofile("input.mp4", transcription=transcription, output_file="with_captions.mp4")

# With custom options
add_captions_to_videofile(
    "input.mp4",
    transcription=transcription,
    output_file="with_captions.mp4",

    # Font settings
    font="Montserrat-ExtraBold.ttf",  # or path to custom font
    font_size=50,
    font_color="white",

    # Stroke settings
    stroke_width=2,
    stroke_color="black",

    # Word highlighting
    highlight_current_word=True,
    highlight_color="#FF4500",
    highlight_padding=(10, 8),  # Horizontal and vertical padding around highlighted words in pixels
    highlight_radius=10,      # Border radius of the highlight box in pixels

    # Layout
    line_count=2,        # Maximum number of lines to show at once
    padding=50,          # Horizontal padding from video edges in pixels
    position="bottom",   # "top", "bottom", or "center"
    margin=200,          # Vertical margin from video edges in pixels (when using top/bottom position)

    # Shadow effects
    shadow_strength=1.0,
    shadow_blur=0.3,

    # Other
    verbose=False
)
```

## Features
- Automatic speech recognition using Whisper
- Customizable caption styling
- Support for multiple video formats
- Easy to use API

## Requirements
- Python 3.7+
- FFmpeg installed on your system

## License
MIT License - see LICENSE file for details.
