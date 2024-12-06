import os
import json
import logging
from typing import Optional

from query2clips.filepaths import (
    output_directory as default_output_directory,
    clips_directory as default_clips_directory,
    videos_directory as default_videos_directory,
)
from query2clips.video_utils import (
    extract_metadata,
    detect_cuts,
    adjust_time_frames_to_keyframes,
    timestamp_to_str,
)
from query2clips.pipeline.searcher import YoutubeSearcher
from query2clips.pipeline.downloader import YtDlpDownloader
from query2clips.pipeline.clipper import FFmpegClipper
from query2clips.pipeline.captioner import GeminiCaptioner


def get_logger(name):
    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    sf = logging.Formatter("[%(asctime)s] %(levelname)s - %(name)s: %(message)s")
    sh.setFormatter(sf)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        logger.addHandler(sh)
    return logger


def read_json(json_path: str):
    with open(json_path, "r") as f:
        d = json.load(f)
    return d


def write_json(d: any, json_path: str):
    with open(json_path, "w") as f:
        json.dump(d, f, default=str)


class Query2Clips:
    def __init__(
        self,
        searcher: str,
        downloader: str,
        clipper: str,
        captioner: Optional[str] = None,
        *,
        video_urls_output_dir: Optional[str] = None,
        video_output_dir: Optional[str] = None,
        clip_output_dir: Optional[str] = None,
        adjust_to_keyframes: bool = True,
        logger_name: str = "pipeline",
    ):
        self.video_urls_output_dir = video_urls_output_dir or default_output_directory
        self.video_output_dir = video_output_dir or default_videos_directory
        self.clip_output_dir = clip_output_dir or default_clips_directory
        self.adjust_to_keyframes = adjust_to_keyframes
        self.logger = get_logger(logger_name)

        self.set_searcher(searcher)
        self.set_downloader(downloader)
        self.set_clipper(clipper)
        if captioner is not None:
            self.set_captioner(captioner)
        else:
            self.captioner = None

    def set_searcher(self, name: str):
        if name == "youtube":
            self.searcher = YoutubeSearcher()
        else:
            raise ValueError(f"unknown searcher: {name}")

    def set_downloader(self, name: str):
        if name == "yt_dlp":
            self.downloader = YtDlpDownloader(logger=self.logger)
        else:
            raise ValueError(f"unknown downloader: {name}")

    def set_clipper(self, name: str):
        if name == "ffmpeg":
            self.clipper = FFmpegClipper(
                framerate=None,
                precision="keyframe_adjusted" if self.adjust_to_keyframes else "exact",
            )
        else:
            raise ValueError(f"unknown clipper: {name}")

    def set_captioner(self, name: str):
        if name == "gemini":
            self.captioner = GeminiCaptioner()
        else:
            raise ValueError(f"unknown captioner: {name}")

    def query_to_video_urls(self, query: str, search_limit: int, search_offset: int):
        video_urls = []
        for fetched_video_urls in self.searcher.search(
            query, limit=search_limit, offset=search_offset
        ):
            video_urls.extend(fetched_video_urls)
        if not os.path.exists(self.video_urls_output_dir):
            os.makedirs(self.video_urls_output_dir)
        dump_path = os.path.join(self.video_urls_output_dir, f"{query}.csv")
        with open(dump_path, "w") as f:
            for url in video_urls:
                f.write(f"{url}\n")
        return video_urls

    def video_urls_to_videos(
        self, video_urls: list[str], video_size: Optional[int] = None
    ):
        for video_url in video_urls:
            video_info = self.downloader.download(
                video_url,
                output_dir=self.video_output_dir,
                video_size=video_size,
            )
            yield video_info

    def video_to_clips(
        self,
        video_path: str,
        clips_dir: str,
        video_url: str,
    ):
        cuts = detect_cuts(video_path)
        time_frames = cuts["cuts_time_frames"]
        if self.adjust_to_keyframes:
            metadata = extract_metadata(video_path, extract_keyframes=True)
            keyframes = metadata["keyframe_timestamps"]
            time_frames = adjust_time_frames_to_keyframes(time_frames, keyframes)

        clip_paths = self.clipper.clip(
            video_path,
            clips_dir,
            time_frames,
        )

        for i, (clip_path, (start, end)) in enumerate(zip(clip_paths, time_frames)):
            output_path = clip_path
            info_path = clip_path.replace(".mp4", ".json")
            info = {
                "video_url": video_url,
                "ss": timestamp_to_str(int(start * 1000)),
                "to": timestamp_to_str(int(end * 1000)),
                "duration": (end - start),
                "size": os.path.getsize(output_path),
                "matching_score": 0,
                "caption": "",
            }
            if self.captioner is not None:
                caption, matching_score = self.captioner.caption(clip_path)
                info["matching_score"] = matching_score
                info["caption"] = caption
            write_json(info, info_path)
            yield {
                "output_path": output_path,
                "info_path": info_path,
                "info": info,
            }

    def __call__(
        self,
        query: str,
        search_limit: int,
        search_offset: int = 0,
        video_size: Optional[int] = None,
    ):
        self.logger.info(f"searching for {query}")

        video_urls = self.query_to_video_urls(query, search_limit, search_offset)
        self.logger.info(f"fetched {len(video_urls)} video urls")

        for video_index, video_info in enumerate(
            self.video_urls_to_videos(video_urls, video_size)
        ):
            video_path = video_info["requested_downloads"][0]["filepath"]
            video_url = video_info["original_url"]
            video_id = video_info["id"]
            self.logger.info(
                f"#{video_index} downloaded {video_url}"
                + (f" ({video_size}p)" if video_size is not None else "")
                + f" to {video_path}"
            )
            clips_dir = os.path.join(self.clip_output_dir, video_id)
            for clip_index, clip_info in enumerate(
                self.video_to_clips(video_path, clips_dir, video_url)
            ):
                self.logger.info(
                    f"- #{clip_index} generated clip: length {clip_info['info']['duration']:.2f}s"
                    + (
                        f" ({clip_info['info']['caption']})"
                        if clip_info["info"]["caption"] != ""
                        else ""
                    )
                )
                yield clip_info
