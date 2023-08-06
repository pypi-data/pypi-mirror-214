from taipan_di import DependencyCollection

from song_metadata_client.classes import (
    SpotifyOptions,
    SpotifyMetadataClient,
    YTMusicMetadataClient,
)
from song_metadata_client.classes.handlers import *
from song_metadata_client.interfaces import BaseMetadataClient

__all__ = ["add_song_metadata_client"]


def add_song_metadata_client(services: DependencyCollection) -> DependencyCollection:
    services.register_singleton(SpotifyOptions)

    services.register_factory(SpotifyMetadataClient)
    services.register_factory(YTMusicMetadataClient)

    services.register_pipeline(BaseMetadataClient).add(SpotifyTrackHandler).add(
        SpotifyPlaylistHandler
    ).add(YTMusicTrackHandler).add(YTMusicPlaylistHandler).add(SpotifySearchHandler).add(
        YTMusicSearchHandler
    ).register()

    return services
