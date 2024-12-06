from abc import ABC, abstractmethod


class Captioner(ABC):
    @abstractmethod
    def caption(self, video_path: str) -> tuple[str, float]:
        """
        Caption a video and return the caption and the matching score.
        """
        ...
