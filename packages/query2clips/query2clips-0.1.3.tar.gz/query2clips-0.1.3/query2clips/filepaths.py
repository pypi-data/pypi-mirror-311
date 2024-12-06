import os
import sys

if getattr(sys, "frozen", False):
    program_directory = os.path.dirname(os.path.abspath(sys.executable))
else:
    program_directory = os.getcwd()

output_directory = os.path.join(program_directory, "outputs")
videos_directory = os.path.join(output_directory, "videos")
clips_directory = os.path.join(output_directory, "clips")

ffmpeg_directory = os.path.join(os.path.dirname(__file__), "ffmpeg")
if sys.platform == "win32":
    ffmpeg_executable = os.path.join(ffmpeg_directory, "ffmpeg.exe")
else:
    ffmpeg_executable = os.path.join(ffmpeg_directory, "ffmpeg")

if sys.platform == "win32":
    ffprobe_executable = os.path.join(ffmpeg_directory, "ffprobe.exe")
else:
    ffprobe_executable = os.path.join(ffmpeg_directory, "ffprobe")
