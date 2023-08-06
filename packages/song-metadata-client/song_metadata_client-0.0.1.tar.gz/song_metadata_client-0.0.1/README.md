# Song Metadata Client

**Get metadata about your favorite songs and playlists !**

## Features

 - Automatic metadata fetching from different services
   - Currently supported : Spotify, Youtube Music
 - Metadata fetching from an URL or a query
 - Supports playlist URLs
 - Easy to use, straightforward interface
 - Possible to use via DI integration

## Installation

### Pip

```
pip install song-metadata-client
```

### Poetry

[Poetry](https://python-poetry.org/) is a Python dependency management and packaging tool. I actually use it for this project.

```
poetry add song-metadata-client
```

## Usage

There are 2 ways to use this library : using the SongMetadataClient object or via the DI.

### Using SongMetadataClient

The library exposes the SongMetadata class. This class has 1 methods : `search`.

This method fetches the metadata corresponding to the request you give it, whether it is an URL or a query. It returns the result as a `SongMetadata` object or a `PlaylistMetadata` object.

**Example :**

```python
from song_metadata_client import SongMetadataClient

client = SongMetadataClient()
result = client.search("in the end - linkin park")

title = result.title # In The End
```

### Using DI

The library also exposes a `BaseMetadataClient` interface and a `add_song_metadata_client` function for [Taipan-DI](https://github.com/Billuc/Taipan-DI).

In this function, the clients are registered as a Pipeline. All you need to do is to resolve the pipeline and execute it.

**Example :**

```python
from song_metadata_client import BaseMetadataClient, add_song_metadata_client
from taipan_di import DependencyCollection

services = DependencyCollection()
add_song_metadata_client(services)

provider = services.build()
client = provider.resolve(BaseMetadataClient)

result = client.exec("in the end - linkin park")
title = result.title # In The End
```

## Inspirations

This library is partially based on spotDL's [spotify-downloader](https://github.com/spotDL/spotify-downloader).
