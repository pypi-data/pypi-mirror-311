import os
import sys

if getattr(sys, "frozen", False):
    program_directory = os.path.dirname(os.path.abspath(sys.executable))
else:
    program_directory = os.getcwd()

ffmpeg_directory = os.path.join(os.path.dirname(__file__), "ffmpeg")
if sys.platform == "win32":
    ffmpeg_executable = os.path.join(ffmpeg_directory, "ffmpeg.exe")
else:
    ffmpeg_executable = os.path.join(ffmpeg_directory, "ffmpeg")

if sys.platform == "win32":
    ffprobe_executable = os.path.join(ffmpeg_directory, "ffprobe.exe")
else:
    ffprobe_executable = os.path.join(ffmpeg_directory, "ffprobe")
