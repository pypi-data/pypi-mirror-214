from typing import Union
from taipan_di import DependencyCollection

from song_metadata_client.classes import SongMetadata, PlaylistMetadata, SpotifyOptions
from song_metadata_client.di import add_song_metadata_client
from song_metadata_client.interfaces import BaseMetadataClient


class SongMetadataClient:
    def __init__(self, spotify_options: SpotifyOptions = None):
        services = DependencyCollection()
        add_song_metadata_client(services)

        if spotify_options is not None:
            services.register_singleton_instance(SpotifyOptions, spotify_options)

        self._client = services.build().resolve(BaseMetadataClient)

    def search(self, url_or_query: str) -> Union[SongMetadata, PlaylistMetadata]:
        return self._client.exec(url_or_query)
