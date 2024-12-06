import typer
import os
from datetime import datetime
from json import dumps
from typing import Dict, Any

import librosa
import pyloudnorm as pyln
import numpy as np
from mutagen.wave import WAVE

import typer
from typing_extensions import Annotated


def get_peak_db(file_path):
    # Load audio
    audio_data, sample_rate = librosa.load(file_path)

    # Find peak amplitude
    peak_amplitude = np.max(np.abs(audio_data))

    # Convert peak amplitude to dB
    peak_db = 20 * np.log10(peak_amplitude)

    return np.float32(peak_db).item()


def get_lkfs(file_path):
    # load file from path
    y, sr = librosa.load(file_path)

    # create meter of loudness
    meter = pyln.Meter(sr)  # 创建响度计

    # collect integrated loudness, LKFS
    loudness = meter.integrated_loudness(y)
    mean_lkfs = loudness.mean()

    return np.float64(mean_lkfs).item()


def parse_wav(file_path: str) -> Dict[str, Any]:
    # extension of file
    ext = os.path.splitext(file_path)[1]

    # file update date
    file_mtime = os.path.getmtime(file_path)
    updated_date = datetime.fromtimestamp(file_mtime)

    # load wav file
    audio = WAVE(file_path)

    # length (sec)
    length_sec = audio.info.length

    # channels
    channels = audio.info.channels

    # sample rate
    sample_rate = audio.info.sample_rate

    # bit rate
    bit_rate = audio.info.bitrate

    # peak db
    peak_db = get_peak_db(file_path)

    # mean lkfs
    mean_lkfs = get_lkfs(file_path)

    return {
        "ext": ext,
        "updated_date": updated_date.isoformat(),
        "length_sec": length_sec,
        "channels": channels,
        "bit_rate": bit_rate,
        "sample_rate": sample_rate,
        "peak_db": peak_db,
        "mean_lkfs": mean_lkfs,
    }


def info(
        file: Annotated[str, typer.Argument(help="File path")],
        pretty: Annotated[bool, typer.Option(help="Pretty print")] = False,
):
    result = parse_wav(file)

    if pretty:
        print(dumps(result, indent=4))
    else:
        print(dumps(result))


app = typer.Typer()
app.command()(info)

def run():
    try:
        app()
    except Exception as e:
        print(dumps({"error": str(e)}))


if __name__ == "__main__":
    run()
