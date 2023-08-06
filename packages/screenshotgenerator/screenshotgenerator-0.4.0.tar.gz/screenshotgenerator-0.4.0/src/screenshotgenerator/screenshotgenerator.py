from __future__ import annotations
import click
from datetime import datetime

from .click_enum_type import EnumType
from .common import write_pool_report
from .defaults import Defaults
from .generate import generate
from .portrait_preference import PortraitPreference
from .screenshot import Screenshot

@click.command()
@click.option("--end-time",
              type=click.DateTime(formats=[Defaults.TIME_FORMAT]),
              default=Defaults.END_TIME,
              show_default=False,
              help="The time at which to stop taking screenshots. Defaults to 95% of the video duration, to exclude credits.")
@click.option("--ffmpeg-path",
              type=str,
              default=Defaults.FFMPEG_PATH,
              show_default=True,
              help="The path to ffmpeg.")
@click.option("--models-directory",
              type=str,
              default=Defaults.MODELS_DIRECTORY,
              show_default=True,
              help="The path to the directory containing the autogluon models. If the directory doesn't exist, the pretrained models will be downloaded to this location.")
@click.option("--pool-directory",
              type=str,
              default=Defaults.POOL_DIRECTORY,
              show_default=True,
              help="The directory in which to store the screenshot pool.")
@click.option("--pool-report-path",
              type=str,
              default=None,
              show_default=True,
              help="A JSON file detailing the screenshot pool, sorted by descending preference.")
@click.option("--pool-size",
              type=int,
              default=Defaults.POOL_SIZE,
              show_default=True,
              help="The size of the pool from which to select screenshots.")
@click.option("--portrait-preference",
              type=EnumType(PortraitPreference),
              default=Defaults.PORTRAIT_PREFERENCE.value,
              show_default=True,
              help="Preference regarding portrait screenshots.")
@click.option("--screenshot-count",
              type=int,
              default=Defaults.SCREENSHOT_COUNT,
              show_default=True,
              help="The number of screenshots to select.")
@click.option("--screenshot-directory",
              type=str,
              required=True,
              help="The directory into which to copy the selected screenshots.")
@click.option("--silent",
              is_flag=True,
              default=Defaults.SILENT,
              show_default=True,
              help="Suppress ffmpeg and autogluon output.")
@click.option("--start-time",
              type=click.DateTime(formats=[Defaults.TIME_FORMAT]),
              default=Defaults.START_TIME,
              show_default=True,
              help="The time at which to start taking screenshots.")
@click.option("--video-path",
              type=str,
              required=True,
              help="The path to the video for which to generate screenshots.")

def main(end_time: datetime, ffmpeg_path: str, models_directory: str, pool_directory: str, pool_report_path: str, pool_size: int, portrait_preference: PortraitPreference,
         screenshot_count: int, screenshot_directory: str, silent: bool, start_time: datetime, video_path: str):
    sorted_screenshots = generate(
        end_time=end_time,
        ffmpeg_path=ffmpeg_path,
        models_directory=models_directory,
        pool_directory=pool_directory,
        pool_size=pool_size,
        portrait_preference=portrait_preference,
        screenshot_count=screenshot_count,
        screenshot_directory=screenshot_directory,
        silent=silent,
        start_time=start_time,
        video_path=video_path)

    write_pool_report(pool_report_path, sorted_screenshots)

if __name__ == "__main__":
    main()