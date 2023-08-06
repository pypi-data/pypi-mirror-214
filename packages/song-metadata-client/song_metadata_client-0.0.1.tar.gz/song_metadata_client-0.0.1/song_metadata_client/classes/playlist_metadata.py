from dataclasses import dataclass
from typing import List

from song_metadata_client.classes import SongMetadata

__all__ = ["PlaylistMetadata"]


@dataclass
class PlaylistMetadata:
    name: str
    description: str
    author: str
    tracks: List[SongMetadata]
