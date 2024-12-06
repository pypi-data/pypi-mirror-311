import time
import logging
from typing import Optional

import yt_dlp

from query2clips.pipeline.downloader.abc import Downloader
from query2clips.filepaths import (
    videos_directory,
    ffmpeg_directory,
)


SLEEP_TIME_AFTER_BOT_DETECTED = 30


class YtDlpDownloader(Downloader):
    def __init__(
        self,
        *,
        logger: logging.Logger = logging.getLogger(__name__),
        only_extract_info: bool = False,
        postprocessors: list[dict] = [],
    ):
        self.logger = logger
        self.only_extract_info = only_extract_info
        self.postprocessors = postprocessors

    def handle_known_error(self, video_url: str, e: yt_dlp.utils.DownloadError):
        self.logger.warning(f"Known error while downloading {video_url}: {str(e)}")

    def handle_unknown_error(self, video_url: str, e: Exception):
        self.logger.error(f"Unknown error while downloading {video_url}: {str(e)}")
        raise e

    def handle_bot_detected(self, video_url: str):
        self.logger.warning(f"Bot detected while downloading {video_url}")
        time.sleep(SLEEP_TIME_AFTER_BOT_DETECTED)

    def handle_no_space_left(self, video_url: str):
        self.logger.error(f"No space left on device while downloading {video_url}")
        # shutil.rmtree(videos_directory)

    def download(
        self,
        video_url: str,
        output_dir: str,
        video_size: Optional[int] = None,
    ) -> dict:
        if video_size is not None:
            video_format_string = (
                f"wv*[height>={video_size}][ext=mp4]+ba[ext=mp4]/"
                f"w[height>={video_size}][ext=mp4]+ba[ext=mp4]/"
                f"bv[ext=mp4]+ba[ext=mp4]/"
                f"b[ext=mp4]+ba[ext=mp4]"
            )
        else:
            video_format_string = None

        ydl_opts = dict(
            outtmpl={
                "default": f"%(id)s.%(ext)s",
            },
            format=video_format_string,
            postprocessors=self.postprocessors,
            logger=self.logger,
            progress_hooks=[],
            dump_single_json=False,
            verbose=False,
            ffmpeg_location=ffmpeg_directory,
            paths=dict(
                home=output_dir,
            ),
        )

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=not self.only_extract_info)
            return info
        except yt_dlp.utils.DownloadError as e:
            msg = str(e.msg)
            known_errors = [
                "Private video",
                "Video unavailable",
                "timed out",
                "violating YouTube's Community Guidelines",
                "Sign in to confirm your age",
            ]
            if any(known_error in msg for known_error in known_errors):
                self.handle_known_error(video_url, e)

            bot_detected_errors = [
                "Sign in to confirm you’re not a bot.",
                "Video unavailable. This content isn’t available.",
            ]
            if any(
                bot_detected_error in msg for bot_detected_error in bot_detected_errors
            ):
                self.handle_bot_detected(video_url)
            else:
                self.handle_unknown_error(video_url, e)
        except Exception as e:
            if "No space left on device" in str(e):
                if video_url is not None:
                    self.handle_no_space_left(video_url)
            else:
                if video_url is not None:
                    self.handle_unknown_error(video_url, e)
