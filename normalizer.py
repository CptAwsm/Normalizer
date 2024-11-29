#!/usr/bin/env python3
"""
Video Audio Normalizer
=====================

A professional-grade tool for batch processing video files to normalize audio levels using FFmpeg.
Provides robust handling of video files with detailed progress metrics and error handling.

Features:
    - Recursive directory processing
    - Hardware-accelerated video processing
    - Detailed progress tracking
    - Comprehensive error handling
    - Audio normalization to broadcast standards

Technical Specifications:
    - Audio Target Levels: -14 LUFS
    - LRA (Loudness Range): 11
    - True Peak: -1.5 dB
    - Output Audio Codec: AAC @ 192kbps

Dependencies:
    - FFmpeg >= 4.0
    - Python >= 3.6
    - pathlib
    - subprocess
    
Author: Jay Dee
License: MIT
Version: 1.0.0
"""

import os
import subprocess
from pathlib import Path
import sys
import time
from datetime import timedelta

# System Configuration
FFMPEG_PATH = r"C:\Program Files\ffmpeg\bin\ffmpeg.exe"

def get_file_size(file_path: str) -> float:
    """
    Calculate and return the file size in megabytes.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        float: File size in megabytes
    """
    return os.path.getsize(file_path) / (1024 * 1024)

def format_time(seconds: float) -> str:
    """
    Convert seconds to human-readable time format (HH:MM:SS).
    
    Args:
        seconds (float): Time duration in seconds
        
    Returns:
        str: Formatted time string
    """
    return str(timedelta(seconds=int(seconds)))

def get_video_files(directory: str, recursive: bool = False) -> list:
    """
    Retrieve all video files from specified directory.
    
    Args:
        directory (str): Base directory to search
        recursive (bool): If True, include subdirectories
    
    Returns:
        list: List of Path objects for each video file
        
    Note:
        Supported formats: .mp4, .mkv, .avi, .mov, .wmv, .flv
    """
    video_extensions = ('.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv')
    directory_path = Path(directory)
    
    if recursive:
        return [f for f in directory_path.rglob('*') if f.suffix.lower() in video_extensions]
    return [f for f in directory_path.glob('*') if f.suffix.lower() in video_extensions]

def get_video_duration(video_path: str) -> float:
    """
    Get video duration in seconds using FFmpeg with fallback method.
    
    Args:
        video_path (str): Path to video file
        
    Returns:
        float: Duration in seconds
        
    Note:
        Uses two-step approach:
        1. Quick probe of video stream
        2. Falls back to full file analysis if initial probe fails
    """
    # Primary method - video stream probe
    cmd = [
        FFMPEG_PATH,
        '-i', str(video_path),
        '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        duration = float(result.stdout.strip())
        return duration
    except (ValueError, subprocess.SubprocessError):
        # Fallback method - full file analysis
        cmd = [
            FFMPEG_PATH,
            '-i', str(video_path),
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1'
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        try:
            return float(result.stdout.strip())
        except ValueError:
            return 0.0

def process_video(video_path: Path, current_file: int, total_files: int) -> None:
    """
    Process a single video file for audio normalization.
    
    Args:
        video_path (Path): Path to input video file
        current_file (int): Current file number in batch
        total_files (int): Total number of files to process
        
    Raises:
        subprocess.CalledProcessError: If FFmpeg processing fails
        Exception: For other processing errors
        
    Note:
        Output file is prefixed with 'normalized_'
        Uses hardware acceleration when available
    """
    start_time = time.time()
    print(f"\nProcessing: {video_path}")
    video_path = Path(video_path)
    output_path = video_path.parent / f"normalized_{video_path.name}"
    
    input_size = get_file_size(video_path)
    duration = get_video_duration(video_path)
    print(f"Input file size: {input_size:.2f} MB")
    
    # FFmpeg command configuration
    extract_cmd = [
        FFMPEG_PATH,
        '-hwaccel', 'auto',          # Hardware acceleration
        '-hide_banner',              # Clean output
        '-i', str(video_path),
        '-map', '0',                 # Maintain all streams
        '-threads', 'auto',          # Optimal thread usage
        '-c:v', 'copy',             # Stream copy video
        '-c:s', 'copy',             # Stream copy subtitles
        '-c:a', 'aac',              # AAC audio codec
        '-b:a', '192k',             # Audio bitrate
        '-af', 'loudnorm=I=-14:LRA=11:TP=-1.5',  # EBU R128 normalization
        '-stats',
        '-v', 'info',
        '-y',                        # Overwrite output
        str(output_path)
    ]

    # Main processing loop
    try:
        print(f"\nFile {current_file} of {total_files}")
        print("Starting FFmpeg processing...\n")
        
        process = subprocess.Popen(
            extract_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            bufsize=1,
            shell=False
        )

        # Real-time progress monitoring
        while process.poll() is None:
            line = process.stderr.readline()
            if line and ('frame=' in line or 'time=' in line):
                print(f"\r{line.strip()}", end='', flush=True)

        if process.returncode != 0:
            error_message = process.stderr.read()
            print(f"\nFFmpeg error: {error_message}")
            raise Exception(error_message)

        # Process completion statistics
        end_time = time.time()
        process_time = end_time - start_time
        output_size = get_file_size(output_path)
        average_speed = input_size / process_time if process_time > 0 else 0
        
        print("\nProcessing completed successfully!")
        print(f"Time taken: {format_time(process_time)}")
        print(f"Average speed: {average_speed:.2f} MB/s")
        print(f"Output file size: {output_size:.2f} MB")

    except subprocess.CalledProcessError as e:
        print(f"\nFFmpeg process error: {e.output}")
        raise

def main():
    """
    Main execution function.
    Handles user input, directory scanning, and batch processing.
    """
    video_directory = input("Enter the directory path containing videos: ")
    recursive = input("Process subdirectories? (y/n): ").lower() == 'y'
    
    video_directory = os.path.abspath(video_directory)
    
    print(f"\nScanning directory: {video_directory}")
    video_files = get_video_files(video_directory, recursive)
    
    total_files = len(video_files)
    print(f"Found {total_files} video files")
    
    for index, video_path in enumerate(video_files, 1):
        try:
            process_video(video_path, index, total_files)
        except Exception as e:
            print(f"Error processing {video_path}: {str(e)}")
            print(f"Full error details: {sys.exc_info()}")

if __name__ == "__main__":
    main()
