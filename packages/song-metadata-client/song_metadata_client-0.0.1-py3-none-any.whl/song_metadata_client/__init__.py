from .classes import (
    SongMetadata,
    PlaylistMetadata,
    SpotifyOptions,
    SpotifyMetadataClient,
    YTMusicMetadataClient,
)
from .di import add_song_metadata_client
from .errors import MetadataClientError
from .interfaces import BaseMetadataClient
from .main import SongMetadataClient

__all__ = [
    "add_song_metadata_client",
    "SongMetadataClient",
    "BaseMetadataClient",
    "MetadataClientError",
    "SongMetadata",
    "PlaylistMetadata",
    "SpotifyOptions",
    "SpotifyMetadataClient",
    "YTMusicMetadataClient",
]
