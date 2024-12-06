from abc import ABC, abstractmethod
from typing import Generator


class Searcher(ABC):
    @abstractmethod
    def search(
        self,
        query: str,
        limit: int,
        offset: int,
    ) -> Generator[list[str], None, None]:
        """
        Search for videos and return a generator of lists of video urls.
        """
        ...
