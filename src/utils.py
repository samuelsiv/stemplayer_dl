import requests
import logging
import os
from exceptions import InvalidStatusCode
from pydub import AudioSegment

AudioSegment.ffmpeg = '{}/ffmpeg.exe'.format(os.getcwd())

API_URL = "https://api.stemplayer.com/"
BASE_FOLDER = "songs"
MERGE_SONGS = True
FORMAT = "wav"
DEVICE_ID = "002800273330510139323636"

files = {}


def merge(album, title):
    PATH = f"{os.getcwd()}/songs/{album}/{title}"

    for file in os.scandir(PATH):
        if not file.is_file():
            continue

        file_name = "{}.{}".format(
            "_".join(file.name.split("_")[:-1]), file.name.split(".")[1]
        )

        if file_name not in files:
            files[file_name] = []

        logging.debug(f"       merger: path is {file.path}")

        files[file_name].append(AudioSegment.from_file(file.path))

    for file in files:
        logging.debug(f"stem_merger: Merging file {file}")
        stems = files[file]
        song = stems[0]

        for stem in stems[1:]:
            song = song.overlay(stem)

        PATH = '{}/songs/{}/{}.flac'.format(os.getcwd(), album, title)

        song.export(PATH, format="flac")


def save_file(url, path):
    r = requests.get(url).content
    with open(path, "wb") as f:
        f.write(r)


def download_stems(data, album, track):
    logging.debug("      download_stems: initialized")

    PATH = f"{os.getcwd()}/{BASE_FOLDER}/{album}/{track}"
    if not os.path.exists(PATH):
        os.makedirs(PATH)

    for url in data:
        match (url):
            case "1":
                save_file(
                    data[url], f"{PATH}/instrumental.{FORMAT}"
                )
            case "2":
                save_file(
                    data[url], f"{PATH}/vocals.{FORMAT}"
                )
            case "3":
                save_file(
                    data[url], f"{PATH}/drums.{FORMAT}"
                )
            case "4":
                save_file(
                    data[url], f"{PATH}/bass.{FORMAT}"
                )
            case _:
                logging.info("      download_stems: Unsupported stem?")

    if MERGE_SONGS:
        logging.info(f"      download_stems: merging track {track}")
        merge(album, track)

    logging.debug("      download_stems: finished")


def get_albums():
    logging.debug("request: Getting list of albums from the Kano API")
    r = requests.get(API_URL + "content/albums")

    if r.status_code != 200:
        raise InvalidStatusCode

    x = r.json()["data"]

    return x


def get_track(track_id, version=1):
    logging.debug("      request: Getting track by id {} with codec {}".format(
            track_id, FORMAT
        )
    )

    params = {
        "track_id": track_id,
        "version": version,
        "codec": FORMAT,
        "device_id": DEVICE_ID
    }

    url = API_URL + "content/stems"

    r = requests.get(url, params=params)
    if r.status_code != 200:
        raise InvalidStatusCode

    x = r.json()["data"]

    return x
