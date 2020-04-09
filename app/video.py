import os
import subprocess
from logging import getLogger
from pathlib import Path
from json_minify import json_minify
import json
from datetime import datetime
import tzlocal
import pytz

from . import led


logger = getLogger()
config = json.loads(json_minify(
    open(Path.home() / 'data' / 'config.json', 'r+').read()))['video']

def main():
    light = led.sensor(17)

    light.on()

    output_file1 = Path.home() / 'data' / 'videos' / str(config['file1_name'])

    ffmpeg1 = subprocess.run([
        '/usr/bin/ffmpeg',
        "-f",
        "v4l2",
        "-r",
        "25",
        "-video_size",
        "1280x720",
        "-pixel_format",
        "yuv422p",
        "-input_format",
        "h264",
        '-i',
        '/dev/video0',
        '-c:v',
        'copy',
        '-r',
        '25',
        "-timestamp",
        "now",
        "-t",
        str(config['record_time']),
        "-y",
        str(output_file1)
    ],capture_output=True)

    logger.debug(f'ffmpeg1 STDOUT: {ffmpeg1.stdout.decode()}')

    light.off()

    output = subprocess.run(
        [
            "/usr/bin/ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format_tags=creation_time",
            "-of",
            "default=nw=1:nk=1",
            "-i",
            str(output_file1)
        ],
        capture_output=True
    ).stdout.decode()

    logger.debug("Got output %s", output)

    local_timezone = tzlocal.get_localzone()  # get pytz tzinfo
    d = output[:-9]
    d = d.replace("-", " ").replace("T", " ").replace(":", " ")
    print(d)

    starttime = datetime.strptime(d, "%Y %m %d %H %M %S")
    local_time = starttime.replace(tzinfo=pytz.utc).astimezone(local_timezone)
    offset = local_time.timestamp()
    logger.debug("Computed date offset %s", offset)
    d = local_time.strftime("%Y %m %d %H %M %S %z")
    filename = d.replace(" ", "-")

    # ffmpeg 3rd pass to add BITC and flip video !
    output_file3 = (
        Path.home() / 'data' / 'videos' / (filename + '_ext.mp4')
    )  # added _int to demark internal camera
    filter = (
        "drawtext=fontfile=" + config['font_path'] + ":fontsize=" +
        str(config['font_size']) + ":text='%{pts\:localtime\:"
        + str(offset)
        + "\\:%Y %m %d %H %M %S}': fontcolor=" +
        config['font_colour'] + "@1: x=10: y=10"
    )
    logger.debug("Using ffmpeg filter %s", filter)
    ffmpeg3 = subprocess.run(
        [
            "/usr/bin/ffmpeg",
            "-i",
            output_file1,
            "-vf",
            filter,
            "-c:v",
            "libx264",
            "-preset",
            "ultrafast",
            "-r",
            "25",
            "-y",
            output_file3,
        ],
        capture_output=True
    )

    logger.debug(f'ffmpeg3 STDOUT: {ffmpeg3.stdout.decode()}')
    logger.debug(f'ffmpeg3 STDERR: {ffmpeg3.stderr.decode()}')

    if ffmpeg3.returncode == 0:
        os.remove(output_file1)

if __name__ == "__main__":
    main()
