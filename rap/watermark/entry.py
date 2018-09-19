import os
import shutil
import threading

import click

from rap.common.utils import filesystem as fs
from rap.common.utils import timeutils as t
from rap.common.utils import parallel as p

from rap.watermark import config_setup as c
from rap.watermark import watermark as w

HELP = {
    "edit":    "Edit the configuration file.",
    "run":     "Run a watermarking task.",
    "reset":   "Reset the configuration files.",
    "verbose": "Show execution related informations."
}

WATERMARK_FORMATS  = ['jpg', 'jpeg', 'png']
WATERMARK_FORMATS += list(str.upper(format) for format in WATERMARK_FORMATS)

CONFIG_FILE    = "config.py"
WATERMARK_FILE = "watermark.png"
FONT_FILE      = "Roboto.ttf"

PACKAGE_CONFIG_FOLDER_PATH      = os.path.join(os.path.dirname(__file__), "defaults")
DEFAULT_WIN_CONFIG_FOLDER_PATH  = os.environ.get('USERPROFILE', None)
DEFAULT_CONFIG_FOLDER_PATH      = os.environ.get('HOME', DEFAULT_WIN_CONFIG_FOLDER_PATH)
CONFIG_FOLDER_PATH              = os.path.join(DEFAULT_CONFIG_FOLDER_PATH, ".config", "watermark")

PACKAGE_CONFIG_SRC    = os.path.abspath(os.path.join(PACKAGE_CONFIG_FOLDER_PATH, CONFIG_FILE))
PACKAGE_WATERMARK_SRC = os.path.abspath(os.path.join(PACKAGE_CONFIG_FOLDER_PATH, WATERMARK_FILE))
PACKAGE_FONT_SRC      = os.path.abspath(os.path.join(PACKAGE_CONFIG_FOLDER_PATH, FONT_FILE))

CONFIG_SRC    = os.path.join(CONFIG_FOLDER_PATH, CONFIG_FILE)
WATERMARK_SRC = os.path.join(CONFIG_FOLDER_PATH, WATERMARK_FILE)
FONT_SRC      = os.path.join(CONFIG_FOLDER_PATH, FONT_FILE)

LOG_LOCK = threading.RLock()

@click.group()
def cli():
    print("Welcome to watermark...")
    c.init([CONFIG_SRC, WATERMARK_SRC, FONT_SRC], [PACKAGE_CONFIG_SRC, PACKAGE_WATERMARK_SRC, PACKAGE_FONT_SRC])


@cli.command(help=HELP["edit"])
def edit():
    click.edit(filename=CONFIG_SRC)
    print("Finished editing configuration. Exiting.")


@cli.command(help=HELP["reset"])
def reset():
    click.confirm("Reset the configuration ?", abort=True)
    shutil.rmtree(CONFIG_FOLDER_PATH)
    c.init([CONFIG_SRC, WATERMARK_SRC, FONT_SRC], [PACKAGE_CONFIG_SRC, PACKAGE_WATERMARK_SRC, PACKAGE_FONT_SRC])
    print("Configuration files have been reset.")


@cli.command(help=HELP["run"])
@click.argument("directory", type=click.Path(exists=True))
@click.option("-v", "--verbose", is_flag=True, help=HELP["verbose"])
def run(directory, config=None, edit_config=None, verbose=None):
    print("This utility might be uninterruptible once started.")
    click.confirm("Apply a watermark to all images in \"{}\" and all subfolders ?".format(directory), abort=True)
    timespan, _ = t.timeit(run_task, directory, verbose)
    print("Done. Execution took {0:.2f} seconds.".format(timespan))


def run_task(directory, verbose):
    conf = c.get_config(CONFIG_FOLDER_PATH, "config")
    images = fs.absfiles(fs.walk_by_extensions(directory, WATERMARK_FORMATS))
    if verbose: print("Watermark image is located at:", conf.watermark)
    p.pexecute(process_image, images, conf, verbose)


def process_image(image_src, conf, verbose):
    if verbose:
        with LOG_LOCK:
            print("Applying watermark on image file:", image_src, "...")
    result = w.watermark(image_src, conf)
    result.save(image_src, quality=100)
