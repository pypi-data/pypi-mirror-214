import logging
from typing import List, Union

import click

from .mpdbg import MPDBG
from .wallpaper import WallpaperSetter


@click.group()
def cli():
    pass


@cli.command(help="run")
@click.option(
    "-w",
    "--wallpaper",
    "wallpaper",
    required=True,
    type=click.Path(exists=True, dir_okay=False, readable=True),
    help="The image file to use as wallpaper",
)
@click.option(
    "-s",
    "--wallpaper-setter",
    "wallpaper_setter",
    required=True,
    type=str,
    help="The wallpaper setter command. Use $image in command to insert quoted path to the image file.",
)
@click.option(
    "-e",
    "--effect",
    "effects",
    default=[],
    type=click.Choice(["blur", "grayscale"]),
    multiple=True,
    help="Effect to apply to wallpaper when displaying an album cover (multiple can be specified)",
)
@click.option(
    "-l",
    "--log-level",
    "log_level",
    default="info",
    type=click.Choice(["debug", "info", "warning", "error", "critical"]),
    help="Set log level.",
)
def run(wallpaper: str, wallpaper_setter: str, effects: List[str], log_level: str):
    setup_logging(log_level)

    config = {
        "wallpaper_filename": wallpaper,
        "wallpaper_setter": WallpaperSetter(wallpaper_setter),
        "effects": effects,
    }

    MPDBG(config).run()


def main():
    """Application main entrypoint"""
    cli()


def setup_logging(level: Union[int, str]) -> logging.Logger:
    """
    Configure "mpdbg" logger.
    :param level: either a integer logging level passed directly to logging.setLevel() or a string representing a level
    :return: the configured logger
    """
    if isinstance(level, str):
        level_map = {
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "warning": logging.WARNING,
            "error": logging.ERROR,
            "critical": logging.CRITICAL,
        }
        level = level_map[level]

    logger = logging.getLogger("mpdbg")
    logger.setLevel(level)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(console_handler)

    return logger
