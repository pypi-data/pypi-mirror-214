import logging
import os

import tempfile
import time
from string import Template
import subprocess

from PIL import Image

from . import shell


class WallpaperSetter:
    """Represents a command line tool to set wallpaper image"""

    def __init__(self, command: str):
        """
        Represents a command line tool to set wallpaper image.

        Command string should contain "$image" which will be replaced with actual path to image file when executing
        the command.

        :param command: command template string
        """
        self.logger = logging.getLogger("mpdbg")
        self.command_template = Template(command)

    def set_wallpaper_from_file(self, wallpaper_path: str):
        """
        Set the desktop wallpaper from image file.

        :param wallpaper_path: wallpaper image file path
        :raise subprocess.CalledProcessError: executing wallpaper setter returned non-zero
        """

        start_time = time.perf_counter_ns()
        command_line = self.command_template.safe_substitute(image=shell.quote(wallpaper_path))
        subprocess.run(command_line, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        time_taken = time.perf_counter_ns() - start_time
        self.logger.debug("setting wallpaper took %.3f seconds", time_taken / 1000 / 1000 / 1000)

    def set_wallpaper_from_image(self, image: Image):
        """
        Set the desktop wallpaper from Image object.

        :param image: wallpaper Image object
        :raise subprocess.CalledProcessError: executing wallpaper setter returned non-zero
        :raise OSError: problem with creating/writing temporary image file
        """

        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as image_file:
            image.save(image_file, "jpeg")

        try:
            self.set_wallpaper_from_file(image_file.name)
        finally:
            try:
                os.remove(image_file.name)
            except OSError as err:
                self.logger.error("failed to remove temporary image file %s: %s", image_file.name, err)
