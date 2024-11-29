# Video Audio Normalizer

A professional-grade tool for batch processing video files to normalize audio levels using FFmpeg. Perfect for content creators, video editors, and anyone dealing with inconsistent audio levels across multiple video files.

## Features

- 🎚️ Normalizes audio to broadcast standards (-14 LUFS)
- 🚀 Hardware-accelerated video processing
- 📁 Recursive directory processing
- 📊 Real-time progress tracking
- 🎯 Zero quality loss video passthrough
- 💪 Robust error handling
- 🎵 High-quality AAC audio output (192kbps)

## Requirements

- Python 3.6 or higher
- FFmpeg 4.0 or higher
- Windows/Linux/MacOS

## Installation

1. Clone this repository:

git clone https://github.com/yourusername/video-audio-normalizer.git

2. Install FFmpeg:

Windows: Download from FFmpeg Official Site (https://www.ffmpeg.org/download.html)
Linux: sudo apt install ffmpeg
MacOS: brew install ffmpeg
Update the FFMPEG_PATH in the script if needed

3. Usage:

python normalize.py

Enter the directory containing your videos when prompted

Choose whether to process subdirectories

## The script will:

Scan for video files (.mp4, .mkv, .avi, .mov, .wmv, .flv)
Process each file with normalized audio
Create new files prefixed with "normalized_"
Display real-time progress and statistics

## Technical Specifications

Target Loudness: -14 LUFS (streaming standard)
Loudness Range (LRA): 11
True Peak: -1.5 dB
Audio Codec: AAC
Audio Bitrate: 192kbps
Video Processing: Direct stream copy (no re-encoding)

## Contributing

Fork the repository
Create your feature branch (git checkout -b feature/AmazingFeature)
Commit your changes (git commit -m 'Add some AmazingFeature')
Push to the branch (git push origin feature/AmazingFeature)
Open a Pull Request

## License

This project is licensed under the MIT License - see below for details:

MIT License

Copyright (c) 2024 Jay Dee

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


Why Use This Tool?
Because life's too short for inconsistent audio levels. Your viewers' ears will thank you, and you'll never have to do the volume dance again - you know, that awkward shuffle between the volume up and down buttons while binge-watching.

Why did the audio normalizer go to therapy?
It had too many ups and downs in life! 🎢
