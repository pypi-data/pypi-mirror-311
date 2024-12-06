import subprocess
import os
from typing import List, Literal

def concat_videos(video_paths: List[str], output_path: str, direction: Literal['horizontal', 'vertical'] = 'horizontal') -> None:
    """
    Concatenate multiple videos either horizontally or vertically using FFmpeg.

    Args:
        video_paths (List[str]): List of paths to input video files.
        output_path (str): Path to save the concatenated video.
        direction (Literal['horizontal', 'vertical']): Direction of concatenation. Defaults to 'horizontal'.

    Raises:
        ValueError: If less than 2 video paths are provided or if an invalid direction is specified.
        subprocess.CalledProcessError: If FFmpeg command fails.
    """
    if len(video_paths) < 2:
        raise ValueError("At least 2 video paths are required for concatenation.")

    if direction not in ['horizontal', 'vertical']:
        raise ValueError("Invalid direction. Choose either 'horizontal' or 'vertical'.")

    filter_complex = []
    for i, video in enumerate(video_paths):
        filter_complex.append(f"[{i}:v]")

    if direction == 'horizontal':
        filter_complex.append(f"hstack=inputs={len(video_paths)}")
    else:
        filter_complex.append(f"vstack=inputs={len(video_paths)}")

    filter_complex = ''.join(filter_complex)

    input_args = []
    for video in video_paths:
        input_args.extend(['-i', video])

    ffmpeg_command = [
        'ffmpeg',
        *input_args,
        '-filter_complex', filter_complex,
        '-c:v', 'libx264',
        '-crf', '23',
        '-preset', 'medium',
        output_path
    ]

    try:
        subprocess.run(ffmpeg_command, check=True, capture_output=True, text=True)
        print(f"Videos concatenated successfully. Output saved to: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while concatenating videos: {e.stderr}")
        raise
