"""extracts basic video compression metadata."""

import json
import subprocess


def extract_metadata(video_path: str, *, extract_keyframes: bool = False):
    command = [
        "ffprobe",
        "-v",
        "quiet",
        "-print_format",
        "json",
        "-show_format",
        "-show_streams",
        video_path,
    ]

    if extract_keyframes:
        command.extend(
            [
                "-select_streams",
                "v:0",
                "-show_entries",
                "packet=pts_time,flags",
            ]
        )

    process = subprocess.run(command, capture_output=True, text=True, check=True)
    video_metadata = json.loads(process.stdout)

    if extract_keyframes:
        keyframe_info = [
            entry
            for entry in video_metadata["packets"]
            if "K" in entry.get("flags", "")
        ]
        keyframe_timestamps = [float(entry["pts_time"]) for entry in keyframe_info]
        if "duration" in video_metadata["format"]:
            duration = float(video_metadata["format"]["duration"])
            keyframe_timestamps.append(duration)
        video_metadata["keyframe_timestamps"] = keyframe_timestamps
        video_metadata.pop("packets")  # Don't need it anymore
    return video_metadata
