import atexit
import io
import logging
import signal
import subprocess
import sys
import time
from typing import Any, Dict, List, Optional

import mpd
import PIL
from PIL import Image

from . import image
from . import mpd_utils
from . import wallpaper


class MPDBG:
    def __init__(self, config: Dict[str, Any]):
        self.logger = logging.getLogger("mpdbg")
        self.wallpaper_filename: str = config["wallpaper_filename"]
        self.setter: wallpaper.WallpaperSetter = config["wallpaper_setter"]
        self.effects: List[str] = config["effects"]
        self.current_wallpaper_id: Optional[str] = None
        self.client: Optional[mpd.MPDClient] = None

    def run(self):
        signal.signal(signal.SIGINT, self.on_signal)
        signal.signal(signal.SIGTERM, self.on_signal)

        atexit.register(self.try_reset_wallpaper)

        try:
            self.setter.set_wallpaper_from_file(self.wallpaper_filename)
        except subprocess.CalledProcessError as err:
            self.logger.error("failed to set wallpaper: %s", err.output.decode())

        while True:
            try:
                self.client = mpd_utils.connect()
            except mpd_utils.ConnectException as err:
                self.logger.error("failed to connect to MPD: %s", err)
                time.sleep(5)
                continue

            self.logger.info("connected to MPD")

            try:
                self.main_loop()

                # should not happen
                self.logger.critical("_main_loop() exited (this is a bug)")
                sys.exit(1)
            except (mpd.MPDError, IOError) as err:
                self.logger.error("error in main loop: %s", err)
                self.try_reset_wallpaper()
                try:
                    self.client.disconnect()
                except (mpd.MPDError, IOError):
                    # ignore
                    pass
                time.sleep(5)

    def main_loop(self):
        song = {}
        state: str = "stop"

        while True:
            old_song = song
            # pylint: disable-next=no-member
            song = self.client.currentsong()

            old_state = state
            # pylint: disable-next=no-member
            state = self.client.status()["state"]

            if old_state == "play":
                # change from play ...
                if state == "play":
                    # ... to play
                    if song != old_song:
                        self.try_set_wallpaper(song)
                else:
                    # ... to stop or pause
                    self.try_reset_wallpaper()
            else:
                # change from stop or pause ...
                if state == "play":
                    # ... to play
                    self.try_set_wallpaper(song)
                else:
                    # ... to stop or pause
                    # do nothing
                    pass

            # pylint: disable-next=no-member
            self.client.idle()

    def on_signal(self, sig, _):
        """
        Signal handler which exits the application if signal is SIGINT or SIGTERM.
        """
        if sig not in [signal.SIGINT, signal.SIGTERM]:
            return

        sys.exit(0)

    def try_reset_wallpaper(self):
        """
        Try setting wallpaper back to original image. Doesn't throw exceptions on error.
        """

        if self.current_wallpaper_id is None:
            return

        try:
            self.setter.set_wallpaper_from_file(self.wallpaper_filename)
            self.current_wallpaper_id = None
        except subprocess.CalledProcessError as err:
            self.logger.error("failed to reset wallpaper: %s", err.output.decode())

    def try_set_wallpaper(self, song: Optional[Dict[str, any]]):
        """
        Try setting wallpaper. Calls try_reset_wallpaper() on error,

        :param song: song to get cover art from
        :raise mpd.MPDError: readpicture command failed
        :raise IOError: readpicture command failed with I/O error
        """

        if song is None:
            new_wallpaper_id = None
        elif mpd_utils.song_is_stream(song):
            new_wallpaper_id = None
        else:
            new_wallpaper_id = song["file"] if "file" in song else None

        if self.current_wallpaper_id == new_wallpaper_id:
            return

        if new_wallpaper_id is None:
            self.try_reset_wallpaper()
            return

        try:
            cover_data = mpd_utils.read_picture(self.client, song)
        except (mpd.MPDError, IOError) as err:
            self.try_reset_wallpaper()
            raise err

        if cover_data is None:
            self.try_reset_wallpaper()
            return

        try:
            cover_image = Image.open(io.BytesIO(cover_data))
        except (FileNotFoundError, PIL.UnidentifiedImageError) as err:
            self.logger.error("failed to open cover image: %s", err)
            self.try_reset_wallpaper()
            return

        blur = "blur" in self.effects
        grayscale = "grayscale" in self.effects
        try:
            img = image.create_wallpaper_image(self.wallpaper_filename, cover_image, blur, grayscale)
        except image.CreateWallpaperException as err:
            self.logger.error("failed to create wallpaper image: %s", err)
            self.try_reset_wallpaper()
            return

        try:
            self.setter.set_wallpaper_from_image(img)
            self.current_wallpaper_id = new_wallpaper_id
        except subprocess.CalledProcessError as err:
            self.logger.error("failed to set wallpaper: %s", err.output.decode())
            self.try_reset_wallpaper()
        except OSError as err:
            self.logger.error("failed to write temporary wallpaper file: %s", err)
            self.try_reset_wallpaper()
