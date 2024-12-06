import os
import shutil
import glob
import tempfile
from typing import Optional

import ffmpeg

from query2clips.filepaths import ffmpeg_executable as default_ffmpeg_executable
from query2clips.video_utils import split_time_frame
from query2clips.pipeline.clipper.abc import Clipper


class FFmpegClipper(Clipper):
    def __init__(
        self,
        *,
        ffmpeg_executable: Optional[str] = None,
        framerate: Optional[float] = None,
        time_frame_unit: str = "s",  # "s" or "ms"
        precision: str = "exact",  # "exact" or "keyframe_adjusted"
    ):
        self.ffmpeg_executable = ffmpeg_executable or default_ffmpeg_executable
        self.framerate = framerate
        self.time_frame_unit = time_frame_unit
        self.precision = precision

    def clip(
        self,
        video_path: str,
        output_dir: str,
        time_frames: list[tuple[float, float]],
    ) -> list[str]:
        clips = []
        for s, e in time_frames:
            if self.time_frame_unit == "s":
                clips += split_time_frame(s, e)
            elif self.time_frame_unit == "ms":
                clips += split_time_frame(s / 1000, e / 1000)

        start_0 = clips[0][0] == 0.0

        ind = 1 + int(not start_0)
        s_p, e_p = clips[0]
        splits = (not start_0) * [s_p] + [e_p]
        take_inds = [int(not start_0)]

        for s, e in clips[1:]:
            if s == e_p:  # situations like [0, 1], [1, 2], [2, 3] -> 1, 2
                splits += [e]
                take_inds.append(ind)
                ind += 1
            else:
                splits += [s, e]
                take_inds.append(ind + 1)
                ind += 2
            e_p = e

        segment_times = ",".join([str(spl) for spl in splits])
        kwargs = {
            "map": 0,
            "f": "segment",
            "segment_times": segment_times,
            "acodec": "copy",
            "reset_timestamps": 1,
        }

        if self.precision == "keyframe_adjusted":
            kwargs["vcodec"] = "copy"
        elif self.precision == "exact":
            kwargs["vcodec"] = "libx264"
            kwargs["preset"] = "ultrafast"
            kwargs["force_key_frames"] = segment_times

        if self.framerate is not None:
            kwargs["r"] = self.framerate

        output_paths = []
        os.makedirs(output_dir, exist_ok=True)
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                (
                    ffmpeg.input(video_path)
                    .output(os.path.join(tmpdir, f"clip_%d.mp4"), **kwargs)
                    .global_args("-hwaccel_device", "auto")
                    .global_args("-hwaccel", "auto")
                    .run(
                        cmd=self.ffmpeg_executable,
                        capture_stdout=True,
                        capture_stderr=True,
                    )
                )
            except ffmpeg.Error as e:
                stdout = e.stdout.decode("utf8")
                stderr = e.stderr.decode("utf8")
                raise Exception(f"ffmpeg error:\nstdout={stdout}\nstderr={stderr}")

            stream_clips = glob.glob(os.path.join(tmpdir, f"clip*.mp4"))
            stream_clips.sort(key=lambda x: int(x.split("_")[-1].split(".")[0]))

            i = 0
            for ind in take_inds:
                i += 1
                output_name = f"{i:04d}.mp4"
                output_path = os.path.join(output_dir, output_name)
                shutil.move(stream_clips[ind], output_path)
                output_paths.append(output_path)
        return output_paths
