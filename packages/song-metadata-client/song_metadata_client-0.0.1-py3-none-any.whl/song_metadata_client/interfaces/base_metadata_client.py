from typing import Union
from taipan_di import PipelineLink
from song_metadata_client.classes import SongMetadata, PlaylistMetadata

__all__ = ["BaseMetadataClient"]


BaseMetadataClient = PipelineLink[str, Union[SongMetadata, PlaylistMetadata]]
