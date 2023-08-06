import logging
import os
from typing import Any, Dict, Optional

import mpd


class ConnectException(Exception):
    """Connecting to MPD failed"""


def connect() -> mpd.MPDClient:
    """
    Connect to Music Player Daemon.

    Uses the MPD_HOST and MPD_PORT environment variables.

    :return: the MPD client
    :raise ConnectException: connecting failed
    """

    logger = logging.getLogger("mpdbg")

    host: str = "localhost"
    port: int = 6600
    password: Optional[str] = None

    host_env = os.getenv("MPD_HOST", None)
    if host_env is not None:
        host_env_split = host_env.split("@", maxsplit=1)
        if len(host_env_split) == 2:
            password, host = host_env_split
        else:
            host = host_env

    port_env = os.getenv("MPD_PORT", None)
    if port_env is not None:
        try:
            port = int(port_env)
        except ValueError:
            logger.warning("invalid value in MPD_PORT environment variable (ignoring)")

    client = mpd.MPDClient()

    try:
        client.connect(host, port)
    except (IOError, mpd.MPDError) as err:
        raise ConnectException(f"Could not connect to {host}: {err}") from err

    if password is not None:
        try:
            # pylint: disable-next=no-member
            client.password(password)
        except (mpd.CommandError, mpd.MPDError, IOError) as err:
            raise ConnectException(
                f"Could not connect to {host}: password command failed: {err}"
            ) from err

    return client


def read_picture(client: mpd.MPDClient, song: Optional[Dict[str, Any]]) -> Optional[bytes]:
    """
    Executes the readpicture command with some extra functionality.

    Checks also if the song dict represents a stream and if so, returns None.

    :param client: MPD client to use
    :param song: song dict retrieved from MPDClient.currentsong()
    :return: cover image data or None if the song file doesn't have a cover image embedded
    :raise mpd.MPDError: command failed
    :raise IOError: IO error happened
    """

    logger = logging.getLogger("mpdbg")

    if song is None:
        logger.debug("read_picture(): song == None")
        return None

    # it seems sometimes when MPD is starting to play stream, currentsong() returns song without "file"
    if "file" not in song:
        logger.debug("read_picture(): no 'file' in song")
        return None

    # don't try to do readpicture for streams
    if song_is_stream(song):
        return None

    image_data = client.readpicture(song["file"])
    if (image_data is None) or ("binary" not in image_data.keys()):
        return None

    return image_data["binary"]


def song_is_stream(song: Optional[Dict[str, Any]]) -> bool:
    if song is None:
        return False

    if "file" not in song:
        return False

    stream_protocols = ["http:", "https:"]

    for protocol in stream_protocols:
        if song["file"].lower().startswith(protocol):
            return True

    return False
