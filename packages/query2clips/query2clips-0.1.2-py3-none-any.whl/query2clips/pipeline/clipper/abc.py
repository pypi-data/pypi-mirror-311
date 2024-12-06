from abc import ABC, abstractmethod


class Clipper(ABC):
    @abstractmethod
    def clip(
        self,
        video_path: str,
        output_dir: str,
        time_frames: list[tuple[float, float]],
    ) -> list[str]:
        """
        Clip a video into multiple clips and return the paths of the clips.
        """
        ...
