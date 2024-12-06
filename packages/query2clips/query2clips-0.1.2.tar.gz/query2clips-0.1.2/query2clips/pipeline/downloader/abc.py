from typing import Optional
from abc import ABC, abstractmethod


class Downloader(ABC):
    @abstractmethod
    def download(
        self,
        video_url: str,
        output_dir: str,
        video_size: Optional[int] = None,
    ) -> dict:
        """
        Download a video and return the download info.
        """
        ...
