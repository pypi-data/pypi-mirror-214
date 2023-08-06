import logging
import time

import PIL
from PIL import Image, ImageOps, ImageFilter


class CreateWallpaperException(Exception):
    """Creating wallpaper image failed"""



def create_wallpaper_image(
        wallpaper_path: str, cover: Image, blur: bool = False, grayscale: bool = False,
        cover_border_size: int = 10, cover_relative_size: float = 0.75, wallpaper_blur_radius: int = 20
) -> Image:
    """
    Create wallpaper image by drawing cover image on top of wallpaper image.
    :param wallpaper_path: wallpaper file path
    :param cover_data: encoded image data
    :param blur: blur background image
    :param grayscale: convert background image to grayscale
    :param cover_border_size: how thick border to draw
    :param cover_relative_size: size of the cover
    :param wallpaper_blur_radius: blur radius
    :return: resulting wallpaper image
    :raise CreateWallpaperException: creating the image failed
    """
    logger = logging.getLogger("mpdbg")

    start_time = time.perf_counter_ns()

    try:
        with open(wallpaper_path, "rb") as file:
            wallpaper = Image.open(file).convert("RGB")
    except (FileNotFoundError, PIL.UnidentifiedImageError) as err:
        raise CreateWallpaperException(f"Failed to open image file {wallpaper_path}: {err}") from err

    cover = cover.convert("RGB")

    # resize cover
    cover_scale = min(
        wallpaper.width / cover.width * cover_relative_size,
        wallpaper.height / cover.height * cover_relative_size,
    )
    cover = cover.resize(
        (int(cover.width * cover_scale), int(cover.height * cover_scale))
    )

    # add border to cover
    cover = ImageOps.expand(cover, cover_border_size, 0)

    if grayscale:
        # convert wallpaper to grayscale
        wallpaper = ImageOps.grayscale(wallpaper).convert("RGB")

    if blur:
        # blur wallpaper
        wallpaper = wallpaper.filter(ImageFilter.GaussianBlur(radius=wallpaper_blur_radius))

    # draw cover on wallpaper
    x_pos = (wallpaper.width - cover.width) // 2
    y_pos = (wallpaper.height - cover.height) // 2
    wallpaper.paste(cover, (x_pos, y_pos))

    time_taken = time.perf_counter_ns() - start_time
    logger.debug("creating wallpaper image took %.3f seconds", time_taken / 1000 / 1000 / 1000)

    return wallpaper
